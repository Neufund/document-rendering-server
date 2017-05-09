import unittest

import auth


def fake_verify_jwt(*args, **kwargs):
    def dec(f):
        return f

    return dec


auth.verify_jwt = fake_verify_jwt


# TODO
class PrivateKeyServerTest(unittest.TestCase):
    def setUp(self):
        from server import app
        self.app = app.test_client()
