import os
import tempfile
import unittest

from FRA import app, db
from FRA.models import User

class BaseTestCase(unittest.TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        db.app = app
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User(username='user', password=User.hash_password('password')))
        db.session.commit()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FRATestCase(BaseTestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'login' in response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
                '/login',
                data=dict(username="user", password="password"),
                follow_redirects=True
            )
        self.assertIn(b'logout', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid username or password', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post(
                '/login',
                data=dict(username="user", password="password"),
                follow_redirects=True
            )
        self.assertIn(b'Requested Features', response.data)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'login', response.data)


    # Ensure list_features redirects to login if not authenticated
    def test_list_feature_unauth(self):
        tester = app.test_client(self)
        response = tester.get('/list', follow_redirects=True)
        self.assertIn(b'login', response.data)


    # Ensure list_features loads
    def test_list_features(self):
        tester = app.test_client(self)
        response = tester.post(
                '/login',
                data=dict(username="user", password="password"),
                follow_redirects=True
            )#login
        response = tester.get('/list', follow_redirects=True)
        self.assertIn(b'Requested Features', response.data)
    
    # Ensure request feature redirects to login if not authenticated
    def test_request_feature_unauth(self):
        tester = app.test_client(self)
        response = tester.get('/request', follow_redirects=True)
        self.assertIn(b'login', response.data)

    # Ensure request feature works
    def test_creat_feature(self):
        tester = app.test_client(self)
        response = tester.post(
                '/login',
                data=dict(username="user", password="password"),
                follow_redirects=True
            )#login
        response = tester.post('/request', 
            data=dict(
                title='test', description='test description',
                                 product_area='test', target_date='2019-02-01', client='client',
                                 client_priority='[1]'),follow_redirects=True)
        self.assertIn(b'was added successfully', response.data)

    # Ensure request feature reorders priority
    def test_reordering_of_priority(self):
        tester = app.test_client(self)
        response = tester.post(
                '/login',
                data=dict(username="user", password="password"),
                follow_redirects=True
            )#login
        response = tester.post('/request', 
            data=dict(
                title='test', description='test description',
                                 product_area='test', target_date='2019-02-01', client='client',
                                 client_priority='[1]'),follow_redirects=True)
        self.assertIn(b'was added successfully', response.data)
        response = tester.post('/request', 
            data=dict(
                title='test2', description='test2 description',
                                 product_area='test', target_date='2019-02-01', client='client',
                                 client_priority='[1, "test"]'),follow_redirects=True)
        self.assertIn(b'was added successfully', response.data)

    # Ensure request client priority list is returned
    def test_client_priority_list(self):
        tester = app.test_client(self)
        response = tester.get('/c_priority',query_string={'client':'client'},follow_redirects=True)
        self.assertIn(b'[]', response.data)


if __name__ == '__main__':
    unittest.main()