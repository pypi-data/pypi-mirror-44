from mock import patch
from contextlib import contextmanager

from eppzy.session import session


class MockTransport:
    def __init__(self, respond, greeting=None):
        self._respond = respond
        self._response = greeting

    def send(self, body):
        self._response = self._respond(body)

    def recv(self):
        return self._response


@contextmanager
def mock_connection(checks):
    yield MockTransport(checks)


@contextmanager
def mocked_session(checks, objs, extns=[]):
    with patch('eppzy.session.connection', return_value=mock_connection(checks)):
        with patch('eppzy.session._login_and_greet'):
            with session(objs, extns, 'ahost', 123, 'clid', 'pwd') as s:
                yield s
