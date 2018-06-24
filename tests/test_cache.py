import pytest
import json
import sys
sys.path.append('../')

from code import cache, classes


class TestCase:
    def test_connection(self):
        assert (cache.Cache().conn() is not None)

    def test_set_and_get(self):
        task = classes.Task(30, (12, 00), 'Commit changes', 'Description')
        ch = cache.Cache()
        ch.set(task, 1)
        assert json.loads(task.json()) == json.loads(ch.pop(1)['task'])

