import os
import unittest
from main import *
from consolemenu import *
from consolemenu.items import *
import requests
from facial_recognition.train_model import train_model

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from pisocket import client

class TestMenu(unittest.TestCase):
    def test_user_menu(self):
        self.assertEqual(
            create_user_menu().__class__, 
            ConsoleMenu
        )

    def test_engineer_menu(self):
        self.assertEqual(
            create_engineer_menu().__class__, 
            ConsoleMenu
        )

    def test_main_menu(self):
        user_menu = create_user_menu()
        engineer_menu = create_engineer_menu()
        self.assertEqual(
            create_main_menu(user_menu, engineer_menu).__class__, 
            ConsoleMenu
        )

class TestPisocket(unittest.TestCase):
    def test_send_credentials(self):
        action = 1
        car_id = 1
        username = 'trungngo'
        password = 'trungngo'
        res_dict = client.send_credentials(action, 
            car_id, 
            username, 
            password
        )
        self.assertTrue(res_dict != 0)

class TestTrainFacialRecognitionModel(unittest.TestCase):
    def test_train_model(self):
        model_path = os.path.join(os.getcwd(), 
            'facial_recognition/output/recognizer.pickle'
        )
        label_encoder_path = os.path.join(os.getcwd(), 
            'facial_recognition/output/le.pickle'
        )
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(label_encoder_path))
        
if __name__ == '__main__':
    unittest.main()