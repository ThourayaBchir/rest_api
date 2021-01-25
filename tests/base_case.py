import unittest
from app.models import Account, Mall, Unit
from app import app, db
import os
from urllib.parse import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'rest_app_test.db'),
    TESTING=True)


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        db.create_all()
        self.populate_db()

    def populate_db(self):
        db.session().add(Account(name='test_account_1'))
        db.session().add(Account(name='test_account_2'))

        db.session().add(Mall(name='test_mall_1', account_id=1))
        db.session().add(Mall(name='test_mall_2', account_id=1))

        db.session().add(Unit(name='test_unit_1', mall_id=1))
        db.session().add(Unit(name='test_unit_2', mall_id=2))
        db.session().commit()

    def _is_url(self, result):
        url = urlparse(result)
        return all([url.scheme, url.netloc])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        return
