import unittest
from flask import url_for, request

from app import app, db

from app.cars.models import Car, CarReport, CarLocation

# import app.cars.view


class WebAppTest(unittest.TestCase):

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

    ################################
    ######### TEST USERS ########
    ################################



if __name__ == "__main__":
    unittest.main()