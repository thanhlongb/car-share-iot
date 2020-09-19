import os
import unittest

from app import app, db, mail

TEST_DB = "test.db"

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['_basedir'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)


    def tearDown(self):
        pass

    ################################
    ################################
    ######### TEST BOOKING #########
    ################################
    ################################


if __name__ == "__main__":
    unittest.main()