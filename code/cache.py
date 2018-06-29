from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ExecutionTimeout, InvalidName
from code.configs import CACHE_CONFIGS, DB_CONFIGS
import psycopg2 as pg
import logging

logging.basicConfig(level=logging.DEBUG, filename='cache_log.txt')


# TODO: add insertedId key usage
class Cache:
    def __init__(self):
        try:
            self.__cache = MongoClient(*CACHE_CONFIGS)['taskmanagerdb']['tasks']  # memcache init. here
        except ConnectionFailure as e:
            logging.critical("%s occurred while connecting Mongodb")
            self.__cache = None
        self._tasks = 0

    def __len__(self):
        return self._tasks

    def conn(self):
        logging.info("A protected field accessed")
        return self.__cache

    def set(self, task, user_id):
        try:
            res = self.__cache.insert_one({'uid': str(user_id), 'task': str(task.json())})
            if res:
                self._tasks += 1
                return res.inserted_id
        except ExecutionTimeout as e:
            logging.critical("%s occurred with setting(%s: %s)" % (str(e), str(user_id), str(task.json())))

    def get(self, user_id):
        try:
            res = self.__cache.find_one({'uid': str(user_id)})
        except (InvalidName, TypeError) as e:
            logging.critical("%s occurred with getting %s" % (str(e), str(user_id)))
            return None
        return res

    def pop(self, user_id, ):
        try:
            res = self.__cache.find_one({'uid': str(user_id)})
            self.__cache.remove({'uid': str(user_id)})
        except (InvalidName, ExecutionTimeout, TypeError) as e:
            logging.critical("%s occurred with popping %s" % (str(e), str(user_id)))
            return None
        return res
