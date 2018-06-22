"""
Classes defenition here
"""

import json
import asyncio
import threading
import logging
import multiprocessing
try:
    import Queue
except ImportError:
    import queue as Queue



logging.log(level=logging.DEBUG, file='classes_log.txt')

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
# TODO: write tests for json serializers and deserializers
# TODO: add checkkey function
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
        if not self.check(day, time):
            logging.critical("Wrong day/time format Error occurred with %s.%s" % (day, ":".join(time)))
            self._time = time
            self._day = day
            self._name = name
            self._description = description

    def set_value(self, key, value):
        if (checkkey(key)):
            setattr(self, key, value)
        else:
            raise Exception('Wrong key format!')
    
    def __repr__(self):
        return self._name + "/n" + self._description

    @staticmethod
    def check(day, time):
        c_t = time.time()  # parse it to (month, day, time) format
        # copy this from Buisbot proj.
        return True

    def json(self):
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
- rewrite for Flask
"""
class BaseServer:
	def __init__(self):
		pass

	def run(self):
		pass

	def stop(self):
		pass

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
