"""
Classes defenition here
"""

import json
import time
import asyncio
import threading
import logging
import multiprocessing
import flask
import ssl
import vkbot
import aiohttp
from code.configs import *
import weakref

try:
    import Queue
except ImportError:
    import queue as Queue

logging.basicConfig(level=logging.DEBUG, filename='classes_log.txt')

"""
TaskManager class
Manipulates with tasks from various amount of users
TODO:
Add iterable dunder-method
"""


class TaskManager:
    def __init__(self):
        self._task_pool = []
        pass

    def __len__(self):
        return len(self._task_pool)

    def get(self):
        pass

    def add(self, task):
        self._task_pool.append(task)


"""
Basic Task class
"""


# TODO: add checkkey function
# TODO: add insertedId key usage

class Task:
    """
    :param day: integer repr.of day
    :param time: tuple with integer(H, M)
    :param name: string Name of task
    :param description: multi - lined description of assigned task
    """

    #  _time field should contain tuple - (hour, min)
    def __init__(self, day, time, name, description, json_data=None):
        if json_data:
            for key, val in json_data.items():
                try:
                    setattr(self, str(key), val)
                except AttributeError as e:
                    logging.critical("%s occurred while trying to set(%s, %s) in Task.__init__()" % (str(e), str(key),
                                                                                                     str(val)))
                    return
        if not self.check(day, time):
            logging.critical("Wrong day/time format Error occurred with %s.%s" % (day, ":".join(time)))
            return
        self._time = time
        self._day = day
        self._name = name
        self._description = description

    def set_value(self, key, value):
        if self.check_key(key):
            setattr(self, key, value)
        else:
            raise Exception('Wrong key format!')

    def __repr__(self):
        return self._name + "/n" + self._description

    @staticmethod
    def check(day, time_):
        c_t = time.time()  # parse it to (month, day, time) format
        # copy this from Buisbot proj.
        return True

    @staticmethod
    def check_key(key):
        return True

    def json(self):
        print(json.dumps(self.__dict__))
        return json.dumps(self.__dict__)


"""
Base class for storing running Bot instances
ToDo:
- think over some memory\database instances, that may be the issue of "memory race"
"""


class WorkProcess:
    def __init__(self):
        self.process = multiprocessing.Process()

    def run(self):
        pass

    def stop(self):
        pass


"""
Base class for future webserver & webhook
Todo:
+ rewrite for Flask
+ rewrite for aiohttp
+ get stop function in aiohttp server
- debug this(Flask) & this(aiohttp) shit
"""


class BaseServer:
    def __init__(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass

    def reboot(self):
        self.stop()
        self.run()



class FlaskServer(BaseServer):
    def __init__(self, bot):
        self.app = flask.Flask(__name__)

        @self.app.route('/', methods=['GET', 'HEAD'])
        def index():
            return ''

        @self.app.route(WEBHOOK_URL_PATH, methods=['POST'])
        def webhook():
            if flask.request.headers.get('content-type') == 'application/json':
                json_string = flask.request.get_data().decode('utf-8')
                update = vkbot.vkinterface.decode_json(json_string)
                bot.process_new_updates([update])
                return ''
            else:
                flask.abort(403)
                return 'Error 403'

        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            self.shutdown_server()

        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))

    @staticmethod
    def shutdown_server():
        pass

    def start(self):
        self.app.run(host=WEBHOOK_LISTEN,
                     port=WEBHOOK_PORT,
                     ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
                     debug=True)

    def stop(self):
        self.app.shutdown()


class AioHttpServer(BaseServer):
    def __init__(self, bot):
        self.app = aiohttp.web.Application()

        self.app['websockets'] = weakref.WeakSet()

        #  it's should be async function
        def handle(request):
            if request.match_info.get('token') == bot.token:
                # must be like:
                '''request_body_dict = await request.json()'''
                # but in Python 3.5.+ , so that means
                request_body_dict = request.json()
                update = vkbot.vkinterface.decode_json(request_body_dict)
                bot.process_new_updates([update])
                return aiohttp.web.Response()
            else:
                return aiohttp.web.Response(status=403)

        def websocket_handler(request):
            ws = aiohttp.web.WebSocketResponse()
            # await ws.prepare(request)
            ws.prepare(request)
            request.app['websockets'].add(ws)
            try:
                # async for msg in ws:
                ...
            finally:
                request.app['websockets'].discard(ws)

            return ws

        def on_shutdown(app):
            for ws in set(self.app['websockets']):
                # await ws.close(code=WSCloseCode.GOING_AWAY,message='Server shutdown')
                ws.close(code=aiohttp.WSCloseCode.GOING_AWAY, message='Server shutdown')

        self.app.router.add_post('/{token}/', handle)

        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    def start(self):
        aiohttp.web.run_app(self.app, host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, ssl_context=context)

    def stop(self):
        # may be it works
        self.app.on_shutdown.append(on_shutdown)


"""
WorkThread class: basic class for separating some parts of bot instance
"""


class WorkThread(threading.Thread):
    def __init__(self):
        pass

    def run(self):
        pass

    def put(self):
        pass

    def stop(self):
        pass


class ThreadPool:
    def __init__(self):
        pass

    def put(self):
        pass

    def close(self):
        pass


"""
Basic class for starting async tasks
Need to look through Github: aioprocessing for better understanding
Todo:
- rewrite special func for aiohttp for requests
- think over other instances, that may need async tasks
- check possibility for running async connection with each user, stored in sessions
"""


class AsyncTask:
    def __init__(self):
        pass

    def _run(self):
        pass

    def wait(self):
        pass


"""
Session class, that provides saving user information & connecting multiply accounts from different messengers & sn
Todo:
- rewrite some methods with dunder-functions
"""


class Session:
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        self.data = {} if not kwargs else dict(kwargs)

    def pause(self, device):
        pass

    def new(self, device):
        pass

    def remove(self, device):
        pass
