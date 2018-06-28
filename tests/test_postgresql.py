import pytest
from code import base


class TestCase:
    def test_add_user(self):
        base.add_user('TestUser', 'tg', 1)

