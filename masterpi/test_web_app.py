import unittest
from flask import url_for, request

from app import app, db

from app.cars.models import Car, CarReport, CarLocation

# import app.cars.view
class testCarsFunction(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client()


    def tearDown(self):
        pass
    

    ################################
    ######### TEST CARS ############
    ################################

    def test_car_details(self):
        with self.app.test_request_context():
            ''' Test get detail infomation about car
            '''
            car = Car.query.filter_by(id=1).first()
            _path = url_for('cars.details', id=1)
            response = self.client.get(_path)
            self.assertIn(car.id, response.data)
            self.assertIn(car.make, response.data)
            self.assertIn(car.color, response.data)
            self.assertEqual(response.status, '200 OK')


    def test_get_all_available_car(self):
        with self.app.test_request_context():
            ''' Test get detail infomation about all availble car
            '''
            _path = url_for('cars.index')
            response = self.client.get(_path)
            self.assertEqual(response.status, '200 OK')

class testBookingsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client()


    def tearDown(self):
        pass

    ################################
    ######### TEST BOOKINGS ########
    ################################

    def test_book_car(self):
        with self.app.test_request_context():
            ''' Test book car function
            '''
            _path = url_for('bookings.book')
            response = self.client.post(_path, data=dict(car_id=1, duration=1))
            self.assertEqual(response.status, '200 OK')


    def test_unlock_car(self):
        with self.app.test_request_context():
            ''' Test unlock car function
            '''
            _path = url_for('bookings.unlock')
            response = self.client.post(_path, data=dict(car_id=1))
            self.assertEqual(response.status, '200 OK')


    def test_cancel_book_car(self):
        with self.app.test_request_context():
            ''' Test cancel booking function
            '''
            _path = url_for('bookings.cancel')
            response = self.client.post(_path, data=dict(car_id=2))
            self.assertEqual(response.status, '200 OK')


    def test_return_car(self):
        with self.app.test_request_context():
            ''' Test return car function
            '''
            _path = url_for('bookings.return_')
            response = self.client.post(_path, data=dict(car_id=1))
            self.assertEqual(response.status, '200 OK')


class testUserLogin(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client()


    def tearDown(self):
        pass

    ################################
    ######### TEST USER ############
    ################################


    ######### TEST HELPERS #########
    
    def register(self, email, username, 
                first_name, last_name, password):
        ''' This function will sent a HTTP POST methods to register a new user
        '''
        _path = url_for('users.register')
        return self.app.post(
            _path,
            data=dict(email=email, 
                    username=username, 
                    first_name=first_name, 
                    last_name=last_name,
                    password=password),
            follow_redirects=True
        )

    def login(self, username, password):
        ''' This function will send a HTTP POST methods to login
        '''
        _path = url_for('users.login')
        return self.app.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        '''This function send HTTP POST method to logout
        '''
        _path = url_for('users.logout')
        return self.app.get(
            _path,
            follow_redirects=True
        )


    ######### TEST REGISTER #########


    def test_valid_user_register(self):
        '''Test valid register function
        '''
        with self.app.test_request_context():
            response = self.register("tminhquang00@gmail.com", "quangtran276", "Quang", "Tran", "123456")
            self.assertEqual(response.status_code, '200')

    

    def test_duplicate_user_register(self):
        '''Test register function in case duplicate user name
        '''
        with self.app.test_request_context():
            response = self.register("tminhquang00@gmail.com", "quangtran276", "Quang", "Tran", "123456")
            response = self.register("tminhquang00@gmail.com", "quangtran276", "123", "1233123", "123333333")
            self.assertNotEqual(response.status_code, '200')
            self.assertIn(b'Username or email is taken.', response.data)

    ######### TEST LOGIN #########

    def test_valid_user_login(self):
        '''Test valid login function
        '''
        with self.app.test_request_context():
            response = self.login('admin', 'admin')
            self.assertEqual(response.status_code, '200')


    def test_invalid_user_login(self):
        '''Test invalid login function
        '''
        with self.app.test_request_context():
            response = self.login('admin', 'Admin')
            self.assertNotEqual(response.status_code, '200')
            self.assertIn(b'Wrong username or password', response.data)


    def test_login_redirect_as_user(self):
        '''test redirect when login as user
        '''
        with self.app.test_request_context():
            r = self.login('user', 'user')
            self.assertEqual(r.request.path, url_for('users.home'))


    def test_login_redirect_as_engineer(self):
        '''test redirect when login as engineer
        '''
        with self.app.test_request_context():
            r = self.login('engineer', 'engineer')
            self.assertEqual(r.request.path, url_for('users.engineer_reports'))


    def test_login_redirect_as_manager(self):
        '''test redirect when login as manager
        '''
        with self.app.test_request_context():
            r = self.login('manager', 'manager')
            self.assertEqual(r.request.path, url_for('users.dashboard'))


    def test_login_redirect_as_admin(self):
        '''test redirect when login as admin
        '''
        with self.app.test_request_context():
            r = self.login('admin', 'admin')
            self.assertEqual(r.request.path, url_for('users.admin_pages'))


    ######### TEST LOGOUT #########


    def test_logout_function(self):
        '''Test logout
        '''
        with self.app.test_request_context():
            login = self.login('admin', 'admin')
            r = self.logout_user()
            self.assertEqual(r.status_code, '200')


    
if __name__ == "__main__":
    unittest.main()