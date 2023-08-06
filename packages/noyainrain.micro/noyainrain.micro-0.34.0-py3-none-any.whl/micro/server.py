# micro
# Copyright (C) 2018 micro contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=abstract-method; Tornado handlers define a semi-abstract data_received()
# pylint: disable=arguments-differ; Tornado handler arguments are defined by URLs
# pylint: disable=missing-docstring; Tornado handlers are documented globally

"""Server components."""

from asyncio import CancelledError, Task, get_event_loop, ensure_future
from collections import Mapping
import http.client
import json
from logging import getLogger
import os
import re
from signal import SIGINT
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Type, Union, cast
from urllib.parse import urlparse

from mypy_extensions import VarArg
from tornado.httpserver import HTTPServer
from tornado.template import DictLoader, Loader, filter_whitespace
from tornado.web import Application, HTTPError, RequestHandler, StaticFileHandler

from . import micro, templates, error
from .micro import (Activity, AuthRequest, Collection, JSONifiable, Object, User, InputError,
                    AuthenticationError, CommunicationError, PermissionError)
from .resource import NoResourceError, ForbiddenResourceError, BrokenResourceError
from .util import str_or_none, parse_slice, check_polyglot

LIST_LIMIT = 100
SLICE_URL = r'(?:/(\d*:\d*))?'

_CLIENT_ERROR_LOG_TEMPLATE = """\
Client error occurred
%s%s
Stack:
%s
URL: %s
User: %s
Device info: %s"""

_LOGGER = getLogger(__name__)

Handler = Union[Tuple[str, Type[RequestHandler]],
                Tuple[str, Type[RequestHandler], Dict[str, object]]]

class Server:
    """Server for micro apps.

    .. attribute:: app

       Underlying :class:`micro.Application`.

    .. attribute:: handlers

       Table of request handlers.

       It is a list of tuples, mapping a URL regular expression pattern to a
       :class:`tornado.web.RequestHandler` class.

    .. attribute:: port

       See ``--port`` command line option.

    .. attribute:: url

       See ``--url`` command line option.

    .. attributes:: client_path

       Client location from where static files and templates are delivered.

    .. attribute:: client_service_path

       Location of client service worker script. Defaults to the included micro service worker.

    .. attribute:: client_map_service_key

       See ``--client-map-service-key`` command line option.

    .. attribute:: debug

       See ``--debug`` command line option.

    .. deprecated:: 0.21.0

       Constructor options as positional arguments. Use keyword arguments instead.
    """

    def __init__(
            self, app: micro.Application, handlers: Sequence[Handler], port: int = 8080,
            url: str = None, client_path: str = 'client', client_modules_path: str = '.',
            client_service_path: str = None, debug: bool = False, *,
            client_map_service_key: str = None) -> None:
        url = url or 'http://localhost:{}'.format(port)
        try:
            urlparts = urlparse(url)
        except ValueError:
            raise ValueError('url_invalid')
        not_allowed = {'username', 'password', 'path', 'params', 'query', 'fragment'}
        if not (urlparts.scheme in {'http', 'https'} and urlparts.hostname and
                not any(cast(object, getattr(urlparts, k)) for k in not_allowed)):
            raise ValueError('url_invalid')

        self.app = app
        self.port = port
        self.url = url
        self.client_path = client_path
        self.client_modules_path = client_modules_path
        self.client_service_path = (
            client_service_path or
            os.path.join(client_modules_path, '@noyainrain/micro/service.js'))
        self.client_map_service_key = client_map_service_key
        self.debug = debug

        self.app.email = 'bot@' + urlparts.hostname
        self.app.render_email_auth_message = self._render_email_auth_message

        def get_activity(*args: str) -> Activity:
            # pylint: disable=unused-argument; part of API
            return self.app.activity
        self.handlers = [
            # UI
            (r'/log-client-error$', _LogClientErrorEndpoint),
            (r'/(?!api/).*$', _UI),
            # API
            (r'/api/login$', _LoginEndpoint),
            (r'/api/users/([^/]+)$', _UserEndpoint),
            (r'/api/users/([^/]+)/set-email$', _UserSetEmailEndpoint),
            (r'/api/users/([^/]+)/finish-set-email$', _UserFinishSetEmailEndpoint),
            (r'/api/users/([^/]+)/remove-email$', _UserRemoveEmailEndpoint),
            (r'/api/settings$', _SettingsEndpoint),
            # Compatibility with non-object Activity (deprecated since 0.14.0)
            make_activity_endpoint(r'/api/activity/v2', get_activity),
            *make_list_endpoints(r'/api/activity(?:/v1)?', get_activity),
            (r'/api/activity/stream', ActivityStreamEndpoint,
             {'get_activity': cast(object, get_activity)}),
            *handlers
        ]

        self._server = HTTPServer(Application(
            self.handlers, compress_response=True, template_path=self.client_path,
            static_path=self.client_path, static_handler_class=_Static, debug=self.debug,
            server=self))
        self._empty_trash_task = None # type: Optional[Task[None]]
        self._message_templates = DictLoader(templates.MESSAGE_TEMPLATES, autoescape=None)
        self._micro_templates = Loader(os.path.join(self.client_path, self.client_modules_path,
                                                    '@noyainrain/micro'))

    def start(self) -> None:
        """Start the server."""
        self.app.update() # type: ignore
        self._empty_trash_task = self.app.start_empty_trash()
        self._server.listen(self.port)

    async def stop(self) -> None:
        """Stop the server."""
        self._server.stop()
        if self._empty_trash_task:
            try:
                self._empty_trash_task.cancel()
                await self._empty_trash_task
            except CancelledError:
                pass

    def run(self) -> None:
        """Start the server and run it continuously."""
        self.start()
        loop = get_event_loop()
        def _on_sigint() -> None:
            async def _stop() -> None:
                await self.stop()
                loop.stop()
            ensure_future(_stop())
        loop.add_signal_handler(SIGINT, _on_sigint)
        loop.run_forever()

    def _render_email_auth_message(self, email, auth_request, auth):
        template = self._message_templates.load('email_auth')
        msg = template.generate(email=email, auth_request=auth_request, auth=auth, app=self.app,
                                server=self).decode()
        return '\n\n'.join([filter_whitespace('oneline', p.strip()) for p in
                            re.split(r'\n{2,}', msg)])

class Endpoint(RequestHandler):
    """JSON REST API endpoint.

    .. attribute:: server

       Context server.

    .. attribute:: app

       Context :class:`Application`.

    .. attribute:: args

       Dictionary of JSON arguments passed by the client.
    """

    current_user = None # type: Optional[User]

    def initialize(self, **args: object) -> None:
        # pylint: disable=unused-argument; part of subclass API
        server = self.application.settings['server']
        assert isinstance(server, Server)
        self.server = server
        self.app = self.server.app
        self.args = {} # type: Dict[str, object]

    def prepare(self):
        self.app.user = None
        auth_secret = self.get_cookie('auth_secret')
        if auth_secret:
            self.current_user = self.app.authenticate(auth_secret)

        if self.request.body:
            try:
                self.args = json.loads(self.request.body.decode())
            except ValueError:
                raise HTTPError(http.client.BAD_REQUEST)
            if not isinstance(self.args, Mapping):
                raise HTTPError(http.client.BAD_REQUEST)

        if self.request.method in {'GET', 'HEAD'}:
            self.set_header('Cache-Control', 'no-cache')

    def patch(self, *args, **kwargs):
        try:
            op = getattr(self, 'patch_{}'.format(self.args.pop('op')))
        except KeyError:
            raise HTTPError(http.client.BAD_REQUEST)
        except AttributeError:
            raise HTTPError(http.client.UNPROCESSABLE_ENTITY)
        # Pass through future to support async methods
        return op(*args, **kwargs)

    def write_error(self, status_code: int, **kwargs: object) -> None:
        e = cast(Tuple[Type[BaseException], BaseException, object], kwargs['exc_info'])[1]
        if isinstance(e, KeyError):
            self.set_status(http.client.NOT_FOUND)
            self.write({'__type__': 'NotFoundError'})
        elif isinstance(e, AuthenticationError):
            self.set_status(http.client.BAD_REQUEST)
            self.write({'__type__': type(e).__name__})
        elif isinstance(e, PermissionError):
            self.set_status(http.client.FORBIDDEN)
            self.write({'__type__': type(e).__name__})
        elif isinstance(e, InputError):
            self.set_status(http.client.BAD_REQUEST)
            self.write({
                '__type__': type(e).__name__,
                'code': e.code,
                'errors': e.errors
            })
        elif isinstance(e, CommunicationError):
            self.set_status(http.client.BAD_GATEWAY)
            self.write({'__type__': type(e).__name__, 'message': str(e)})
        elif isinstance(e, error.Error):
            status = {
                error.ValueError: http.client.BAD_REQUEST,
                NoResourceError: http.client.NOT_FOUND,
                ForbiddenResourceError: http.client.FORBIDDEN,
                BrokenResourceError: http.client.BAD_REQUEST
            }
            self.set_status(status[type(e)])
            self.write(e.json())
        else:
            super().write_error(status_code, **kwargs)

    def log_exception(self, typ, value, tb):
        # These errors are handled specially and there is no need to log them as exceptions
        if issubclass(
                typ,
                (KeyError, AuthenticationError, PermissionError, CommunicationError, error.Error)):
            return
        super().log_exception(typ, value, tb)

    def check_args(self, type_info):
        """Check *args* for their expected type.

        *type_info* maps argument names to :class:`type` s. If multiple types are valid for an
        argument, a tuple can be given. The special keyword ``'opt'`` marks an argument as optional.
        ``None`` is equvialent to ``type(None)``. An example *type_info* could look like::

            {'name': str, 'pattern': (str, 'opt')}

        If any argument has an unexpected type, an :exc:`InputError` with ``bad_type`` is raised. If
        an argument is missing but required, an :exc:`InputError` with ``missing`` is raised.

        A filtered subset of *args* is returned, matching those present in *type_info*. Thus any
        excess argument passed by the client can safely be ignored.
        """
        args = {k: v for k, v in self.args.items() if k in type_info.keys()}

        e = InputError()
        for arg, types in type_info.items():
            # Normalize
            if not isinstance(types, tuple):
                types = (types, )
            types = tuple(type(None) if t is None else t for t in types)

            # Check
            if arg not in args:
                if 'opt' not in types:
                    e.errors[arg] = 'missing'
            else:
                types = tuple(t for t in types if isinstance(t, type))
                # NOTE: We currently do not handle types being empty (e.g. it contained only
                # keywords)
                if not isinstance(args.get(arg), types):
                    e.errors[arg] = 'bad_type'
        e.trigger()

        return args

class CollectionEndpoint(Endpoint):
    """API endpoint for a :class:`Collection`.

    .. attribute:: get_collection

       Function of the form *get_collection(*args: str) -> Collection*, responsible for retrieving
       the underlying collection. *args* are the URL arguments.
    """

    def initialize(self, **args: object) -> None:
        super().initialize(**args)
        get_collection = args.get('get_collection')
        if not callable(get_collection):
            raise TypeError()
        self.get_collection = get_collection # type: Callable[[VarArg(str)], Collection[Object]]

    def get(self, *args: str) -> None:
        collection = self.get_collection(*args)
        try:
            slc = parse_slice(self.get_query_argument('slice', ':'), limit=LIST_LIMIT)
        except ValueError:
            raise micro.ValueError('bad_slice_format')
        self.write(collection.json(restricted=True, include=True, slc=slc))

class ActivityStreamEndpoint(Endpoint):
    """Event stream API endpoint for :class:`Activity`.

    .. attribute:: get_activity

       Function of the form ``get_activity(*args)``, responsible for retrieving the activity. *args*
       are the URL arguments.
    """

    def initialize(self, **args: object) -> None:
        super().initialize(**args)
        get_activity = args.get('get_activity')
        if not callable(get_activity):
            raise TypeError()
        self.get_activity = get_activity # type: Callable[[VarArg(str)], Activity]
        self._stream = None # type: Optional[Activity.Stream]

    async def get(self, *args: str) -> None:
        activity = self.get_activity(*args)
        self._stream = activity.stream()
        self.set_header('Content-Type', 'text/event-stream')
        self.flush()
        async for event in self._stream:
            self.app.user = self.current_user
            data = json.dumps(event.json(restricted=True, include=True)) # type: ignore
            self.write('data: {}\n\n'.format(data))
            self.flush()

    def on_connection_close(self) -> None:
        if self._stream:
            ensure_future(self._stream.aclose())

def make_list_endpoints(
        url: str, get_list: Callable[[VarArg(str)], Sequence[JSONifiable]]) -> List[Handler]:
    """Make the API endpoints for a list with support for slicing.

    *url* is the URL of the list.

    *get_list* is a hook of the form *get_list(*args)*, responsible for retrieving the underlying
    list. *args* are the URL arguments.
    """
    return [(url + r'(?:/(\d*:\d*))?$', _ListEndpoint, {'get_list': get_list})]

def make_trashable_endpoints(url, get_object):
    """Make API endpoints for a :class:`Trashable` object.

    *url* is the URL of the object.

    *get_object* is a function of the form *get_object(*args)*, responsible for retrieving the
    object. *args* are the URL arguments.
    """
    return [
        (url + r'/trash$', _TrashableTrashEndpoint, {'get_object': get_object}),
        (url + r'/restore$', _TrashableRestoreEndpoint, {'get_object': get_object})
    ]

def make_orderable_endpoints(url, get_collection):
    """Make API endpoints for a :class:`Orderable` collection.

    *url* and *get_collection* are equivalent to the arguments of :func:`make_list_endpoints`.
    """
    return [(url + r'/move$', _OrderableMoveEndpoint, {'get_collection': get_collection})]

def make_activity_endpoint(url: str, get_activity: Callable[[VarArg(str)], Activity]) -> Handler:
    """Make an API endpoint for an :class:`Activity` at *url*.

    *get_activity* is a function of the form *get_activity(*args)*, responsible for retrieving the
    activity. *args* are the URL arguments.
    """
    return (r'{}{}$'.format(url, SLICE_URL), _ActivityEndpoint, {'get_activity': get_activity})

class _Static(StaticFileHandler):
    def set_extra_headers(self, path):
        if self.get_cache_time(path, self.modified, self.get_content_type()) == 0:
            self.set_header('Cache-Control', 'no-cache')
        if path == self.application.settings['server'].client_service_path:
            self.set_header('Service-Worker-Allowed', '/')

class _UI(RequestHandler):
    def initialize(self) -> None:
        server = self.application.settings['server']
        assert isinstance(server, Server)
        self._server = server
        # pylint: disable=protected-access; Server is a friend
        self._templates = self._server._micro_templates
        if self._server.debug:
            self._templates.reset()

    def get_template_namespace(self) -> Dict[str, object]:
        return {
            **super().get_template_namespace(),
            'modules_path': self._server.client_modules_path,
            'service_path': self._server.client_service_path,
            'map_service_key': self._server.client_map_service_key
        }

    def get(self):
        self.set_header('Cache-Control', 'no-cache')
        self.render(
            'index.html', micro_dependencies=self._render_micro_dependencies,
            micro_boot=self._render_micro_boot, micro_templates=self._render_micro_templates)

    def _render_micro_dependencies(self) -> bytes:
        return self._templates.load('dependencies.html').generate(**self.get_template_namespace())

    def _render_micro_boot(self) -> bytes:
        return self._templates.load('boot.html').generate(**self.get_template_namespace())

    def _render_micro_templates(self) -> bytes:
        return self._templates.load('templates.html').generate(**self.get_template_namespace())

class _LogClientErrorEndpoint(Endpoint):
    def post(self):
        args = self.check_args({
            'type': str,
            'stack': str,
            'url': str,
            'message': (str, None, 'opt')
        })
        e = micro.InputError()
        if str_or_none(args['type']) is None:
            e.errors['type'] = 'empty'
        if str_or_none(args['stack']) is None:
            e.errors['stack'] = 'empty'
        if str_or_none(args['url']) is None:
            e.errors['url'] = 'empty'
        e.trigger()

        message = str_or_none(args.get('message'))
        message_part = ': ' + message if message else ''
        user = '{} ({})'.format(self.app.user.name, self.app.user.id) if self.app.user else '-'
        _LOGGER.error(
            _CLIENT_ERROR_LOG_TEMPLATE, args['type'], message_part, args['stack'].strip(),
            args['url'], user, self.request.headers.get('user-agent', '-'))
        self.write({})

class _ListEndpoint(Endpoint):
    def initialize(self, get_list):
        super().initialize()
        self.get_list = get_list

    def get(self, *args):
        seq = self.get_list(*args)
        slice = parse_slice(args[-1] or ':', limit=LIST_LIMIT)
        self.write(json.dumps([i.json(restricted=True, include=True) if isinstance(i, Object) else i
                               for i in seq[slice]]))

class _TrashableTrashEndpoint(Endpoint):
    def initialize(self, get_object):
        super().initialize()
        self.get_object = get_object

    def post(self, *args):
        obj = self.get_object(*args)
        obj.trash()
        self.write(obj.json(restricted=True, include=True))

class _TrashableRestoreEndpoint(Endpoint):
    def initialize(self, get_object):
        super().initialize()
        self.get_object = get_object

    def post(self, *args):
        obj = self.get_object(*args)
        obj.restore()
        self.write(obj.json(restricted=True, include=True))

class _OrderableMoveEndpoint(Endpoint):
    def initialize(self, get_collection):
        super().initialize()
        self.get_collection = get_collection

    def post(self, *args):
        collection = self.get_collection(*args)
        args = self.check_args({'item_id': str, 'to_id': (str, None)})
        try:
            args['item'] = collection[args.pop('item_id')]
        except KeyError:
            raise micro.ValueError('item_not_found')
        args['to'] = args.pop('to_id')
        if args['to'] is not None:
            try:
                args['to'] = collection[args['to']]
            except KeyError:
                raise micro.ValueError('to_not_found')

        collection.move(**args)
        self.write(json.dumps(None))

class _LoginEndpoint(Endpoint):
    def post(self):
        args = self.check_args({'code': (str, 'opt')})
        user = self.app.login(**args)
        self.write(user.json(restricted=True))

class _UserEndpoint(Endpoint):
    def get(self, id):
        self.write(self.app.users[id].json(restricted=True))

    def post(self, id):
        user = self.app.users[id]
        args = self.check_args({'name': (str, 'opt')})
        user.edit(**args)
        self.write(user.json(restricted=True))

    async def patch_enable_notifications(self, id):
        # pylint: disable=missing-docstring; private
        user = self.app.users[id]
        args = self.check_args({'push_subscription': str})
        await user.enable_device_notifications(**args)
        self.write(user.json(restricted=True))

    def patch_disable_notifications(self, id: str) -> None:
        # pylint: disable=missing-docstring; private
        user = self.app.users[id]
        user.disable_device_notifications(self.current_user)
        self.write(user.json(restricted=True))

class _UserSetEmailEndpoint(Endpoint):
    def post(self, id):
        user = self.app.users[id]
        args = self.check_args({'email': str})
        auth_request = user.set_email(**args)
        self.write(auth_request.json(restricted=True))

class _UserFinishSetEmailEndpoint(Endpoint):
    def post(self, id):
        user = self.app.users[id]
        args = self.check_args({'auth_request_id': str, 'auth': str})
        args['auth_request'] = self.app.get_object(args.pop('auth_request_id'), None)
        if not isinstance(args['auth_request'], AuthRequest):
            raise micro.ValueError('auth_request_not_found')
        user.finish_set_email(**args)
        self.write(user.json(restricted=True))

class _UserRemoveEmailEndpoint(Endpoint):
    def post(self, id):
        user = self.app.users[id]
        user.remove_email()
        self.write(user.json(restricted=True))

class _SettingsEndpoint(Endpoint):
    def get(self):
        self.write(self.app.settings.json(restricted=True, include=True))

    def post(self):
        args = self.check_args({
            'title': (str, 'opt'),
            'icon': (str, None, 'opt'),
            'icon_small': (str, None, 'opt'),
            'icon_large': (str, None, 'opt'),
            'provider_name': (str, None, 'opt'),
            'provider_url': (str, None, 'opt'),
            'provider_description': (dict, 'opt'),
            'feedback_url': (str, None, 'opt'),
            # Compatibility for favicon (deprecated since 0.13.0)
            'favicon': (str, None, 'opt')
        })
        if 'provider_description' in args:
            try:
                check_polyglot(args['provider_description'])
            except ValueError:
                raise micro.ValueError('provider_description_bad_type')

        settings = self.app.settings
        settings.edit(**args)
        self.write(settings.json(restricted=True, include=True))

class _ActivityEndpoint(Endpoint):
    def initialize(self, get_activity):
        super().initialize()
        self.get_activity = get_activity

    def get(self, *args):
        activity = self.get_activity(*args)
        slice = parse_slice(args[-1] or ':', limit=LIST_LIMIT)
        self.write(activity.json(restricted=True, include=True, slice=slice))

    def patch_subscribe(self, *args):
        # pylint: disable=missing-docstring; private
        activity = self.get_activity(*args)
        activity.subscribe()
        self.write(activity.json(restricted=True, include=True))

    def patch_unsubscribe(self, *args):
        # pylint: disable=missing-docstring; private
        activity = self.get_activity(*args)
        activity.unsubscribe()
        self.write(activity.json(restricted=True, include=True))
