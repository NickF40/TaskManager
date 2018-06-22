import pytest
import datetime.datetime as datetime
import code.cache as cache
from code.classes import Task


# TODO: finish when all methods will be defined
class TestCache:
    def connection(self):
        assert cache.Cache().conn() is not None

    def get_and_set(self):
        mem = cache.Cache()
        t_now = datetime.timetuple(datetime.now())
        task = Task(t_now.tm_mday, (t_now.tm_hour, t_now.tm_min), "Commit changes", "")
        mem.set(task.json(), 1)
        assert mem.get(1) == task.json()
