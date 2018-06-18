"""
Class defenitions here
"""
import time
from code.cache import Cache
from code.configs import CACHE_CONFIGS


class TaskManager:
    def __init__(self):
        self._tasks_pool = []
        self._cache = Cache(CACHE_CONFIGS)

    def get_tasks(self):
        t = time.time()
        self._tasks_pool = []   # just to fill

class Task:
    def __init__(self):
        pass

    def __add__(self, other):
        pass
