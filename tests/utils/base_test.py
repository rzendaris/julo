"""
Base class for testing
"""
import os
from builtins import isinstance, dict

from flask_testing import TestCase
from app import create_app, db


class BaseTest(TestCase):

    def set_up_extra(self):
        pass

    def create_app(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        return self.app

    def setUp(self):
        from sqlalchemy_utils import create_database, database_exists
        if not database_exists(os.getenv('TEST_DATABASE_URI')):
            create_database(os.getenv('TEST_DATABASE_URI'))

        db.drop_all()
        db.create_all()
        self.set_up_extra()

    def tearDown(self):
        db.session.remove()

    def assert_equal_dict(self, source, target):
        for key in source:
            self.assertIn(key, target)
            if isinstance(source[key], dict):
                self.assert_equal_dict(source[key], target[key])
            else:
                self.assertEqual(source[key], target[key])

