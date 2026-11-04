import unittest
from http import HTTPStatus

from .. import create_app
from ..config.config import config_dict
from ..utils import db


class LoginRequiredTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()

    # Protected endpoints must answer 401 when no token is sent, not crash with a 500
    def test_protected_endpoints_require_a_token(self):
        for path in ("/student/students", "/course/courses"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
