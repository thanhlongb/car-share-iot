import unittest
from flask import url_for, request
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import app, db

from app.cars.models import Car, CarReport, CarLocation

# import app.cars.view
class testCarsFunction(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()


    def tearDown(self):
        pass
    
    ######### TEST HELPERS #########
    

    def login(self, username, password):
        ''' This function will send a HTTP POST methods to login
        '''
        _path = url_for('users.login')
        return self.client.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )


    ################################
    ######### TEST CARS ############
    ################################

    def test_car_details(self):
        with self.app.test_request_context():
            ''' Test get detail infomation about car
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            car = Car.query.filter_by(id=1).first()
            _path = url_for('cars.details', id=1)
            response = self.client.get(_path)
            self.assertEqual(response.status, '200 OK')


    def test_get_all_available_car(self):
        with self.app.test_request_context():
            ''' Test get detail infomation about all availble car
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('cars.index')
            response = self.client.get(_path)
            self.assertEqual(response.status, '200 OK')


class testBookingsAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()



    def tearDown(self):
        pass
    ######### TEST HELPERS #########
    

    def login(self, username, password):
        ''' This function will send a HTTP POST methods to login
        '''
        _path = url_for('users.login')
        return self.client.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )


    ################################
    ######### TEST BOOKINGS ########
    ################################

    def test_book_car(self):
        with self.app.test_request_context():
            ''' Test book car function
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('bookings.book')
            response = self.client.post(_path, data=dict(car_id=1, duration=1))
            self.assertEqual(response.status, '200 OK')


    def test_unlock_car(self):
        with self.app.test_request_context():
            ''' Test unlock car function
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('bookings.unlock')
            response = self.client.post(_path, data=dict(booking_id=1))
            self.assertEqual(response.status, '200 OK')


    def test_cancel_book_car(self):
        with self.app.test_request_context():
            ''' Test cancel booking function
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('bookings.cancel')
            response = self.client.post(_path, data=dict(booking_id=2))
            self.assertEqual(response.status, '200 OK')


    def test_return_car(self):
        with self.app.test_request_context():
            ''' Test return car function
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('bookings.return_')
            response = self.client.post(_path, data=dict(booking_id=1))
            self.assertEqual(response.status, '200 OK')


class testUserLogin(unittest.TestCase):

    def setUp(self):
        # app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        # app.config['CSRF_ENABLED'] = False
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
        return self.client.post(
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
        return self.client.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        '''This function send HTTP POST method to logout
        '''
        _path = url_for('users.logout')
        return self.client.get(
            _path,
            follow_redirects=True
        )


    # ######### TEST REGISTER #########


    def test_valid_user_register(self):
        '''Test valid register function
        '''
        with self.app.test_request_context():
            response = self.register("tminhquang00@gmail.com", "quangtran276", "Quang", "Tran", "123456")
            self.assertEqual(response.status_code, 200)

    

    def test_duplicate_user_register(self):
        '''Test register function in case duplicate user name
        '''
        with self.app.test_request_context():
            response = self.register("tminhquang00@gmail.com", "quangtran276", "123", "1233123", "123333333")
            self.assertEqual(response.status_code, 200)

    ######### TEST LOGIN #########

    def test_valid_user_login(self):
        '''Test valid login function
        '''
        with self.app.test_request_context():
            response = self.login('admin', 'admin')
            self.assertEqual(response.status_code, 200)


    def test_invalid_user_login(self):
        '''Test invalid login function
        '''
        with self.app.test_request_context():
            response = self.login('admin', 'Admin')
            self.assertEqual(response.status_code, 404)


    def test_login_redirect_as_user(self):
        '''test redirect when login as user
        '''
        with self.app.test_request_context():
            r = self.login('user', 'user')
            self.assertEqual(r.status_code, 200)



    def test_login_redirect_as_engineer(self):
        '''test redirect when login as engineer
        '''
        with self.app.test_request_context():
            r = self.login('engineer', 'engineer')
            self.assertEqual(r.status_code, 200)


    def test_login_redirect_as_manager(self):
        '''test redirect when login as manager
        '''
        with self.app.test_request_context():
            r = self.login('manager', 'manager')
            self.assertEqual(r.status_code, 200)


    def test_login_redirect_as_admin(self):
        '''test redirect when login as admin
        '''
        with self.app.test_request_context():
            r = self.login('admin', 'admin')
            self.assertEqual(r.status_code, 200)


    # ######### TEST LOGOUT #########


    def test_logout_function(self):
        '''Test logout
        '''
        with self.app.test_request_context():
            login = self.login('admin', 'admin')
            r = self.logout_user()
            self.assertIsNotNone(r.status_code)


class testApiForAdmin(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()



    def tearDown(self):
        pass
    
    ######### TEST HELPERS #########
    

    def login(self, username, password):
        ''' This function will send a HTTP POST methods to login
        '''
        _path = url_for('users.login')
        return self.client.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )


    ################################
    ######### TEST CAR API #########
    ################################

    def test_admin_car_page_valid_request(self):
        with self.app.test_request_context():
            ''' Test admin access to admin car page
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_cars')
            response = self.client.get(_path)
            self.assertEqual(response.status, '200 OK')


    def test_admin_car_page_invalid_request(self):
        with self.app.test_request_context():
            ''' Test other access to admin car page
            '''
            self.assertEqual(self.login('engineer', 'engineer').status_code, 200)
            _path = url_for('users.admin_cars')
            response = self.client.get(_path)
            self.assertEqual(response.data, b'503 Not sufficent permission')


    def test_admin_cars_create_api(self):
        with self.app.test_request_context():
            ''' Test create car api
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_cars_create')
            response = self.client.post(_path, 
                                        data=dict(make='vinfast', color='red',           body_type='A123', seats=5, cost_per_hour=10))
            self.assertEqual(response.status_code, 302)
    

    def test_admin_cars_delete_api(self):
        with self.app.test_request_context():
            ''' Test delete car api
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_cars_delete')
            response = self.client.post(_path, data=dict(car_id=4))
            self.assertEqual(True)


    def test_admin_cars_report_api(self):
        with self.app.test_request_context():
            ''' Test report car api
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_cars_report')
            response = self.client.post(_path, data=dict(car_id=7))
            self.assertEqual(response.status_code, 200)

    ################################
    ######### TEST USER API #########
    ################################

    def test_admin_users_page_valid_request(self):
        with self.app.test_request_context():
            ''' Test admin access to admin user page
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_users')
            response = self.client.get(_path)
            self.assertEqual(response.status, '200 OK')


    def test_admin_users_create_api(self):
        with self.app.test_request_context():
            ''' Test create car api
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_users_create')
            response = self.client.post(_path, 
                                        data=dict(
                                            email='tmq2706@gmail.com',
                                            username='QuangTran',
                                            password='123456',
                                            first_name='Tran',
                                            last_name='Quang',
                                            role=1,
                                            bluetooth_MAC='60:57:18:a6:39:22'
                                        ))
            self.assertEqual(response.status_code, 302)
    

    def test_admin_users_delete_api(self):
        with self.app.test_request_context():
            ''' Test delete users api
            '''
            self.assertEqual(self.login('admin', 'admin').status_code, 200)
            _path = url_for('users.admin_users_delete')
            response = self.client.post(_path, data=dict(user_id=9))
            self.assertEqual(True)


class testManagerApi(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()



    def tearDown(self):
        pass
    
    ######### TEST HELPERS #########
    

    def login(self, username, password):
        ''' This function will send a HTTP POST methods to login
        '''
        _path = url_for('users.login')
        return self.client.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    ######### TEST API FOR MANAGER #########
    def test_report_page_valid_request(self):
        with self.app.test_request_context():
            ''' Test manager access to reports page
            '''
            self.assertEqual(self.login('manager', 'manager').status_code, 200)
            _path = url_for('users.manager_reports')
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)


    def test_manager_reports_assign(self):
        with self.app.test_request_context():
            ''' Test manager assign function
            '''
            self.assertEqual(self.login('manager', 'manager').status_code, 200)
            _path = url_for('users.manager_reports_assign')
            response = self.client.post(_path, data=dict(engineer_id=1))
            self.assertEqual(response.status_code, 200)


class testEngineerApi(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app
        self.client = app.test_client()



    def tearDown(self):
        pass
    
    ######### TEST HELPERS #########
    

    def login(self, username, password):
        ''' This function will send a HTTP POST methods to login
        '''
        _path = url_for('users.login')
        return self.client.post(
            _path,
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    ######### TEST API FOR ENGINEER #########
    def test_report_page_valid_request(self):
        with self.app.test_request_context():
            ''' Test Engineer access to reports page
            '''
            self.assertEqual(self.login('engineer', 'engineer').status_code, 200)
            _path = url_for('users.engineer_reports')
            response = self.client.get(_path)
            self.assertEqual(response.status_code, 200)


    def test_engineer_reports_fixed(self):
        with self.app.test_request_context():
            ''' Test engineer report function
            '''
            self.assertEqual(self.login('engineer', 'engineer').status_code, 200)
            _path = url_for('users.engineer_reports_fixed')
            response = self.client.post(_path, data=dict(report_id=1))
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    # suite = loader.loadTestsFromTestCase(testUserLogin)
    suite = loader.loadTestsFromTestCase(testApiForAdmin)

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
