import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

def check_basic_success(self, url, http_method):
    res = http_method(url)
    data = json.loads(res.data)
    self.assertTrue(data['success'])
    self.assertEqual(res.status_code,200)
    return data

def check_basic_failure(self, url, code, http_method):
    res = http_method(url)
    data = json.loads(res.data)
    self.assertFalse(data['success'])
    self.assertEqual(res.status_code, code)
    return data

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'Blue84paired.', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_GET_trivia_questions(self):
        data = check_basic_success(self, '/questions', self.client().get)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) <= 10)

    def test_GET_categories(self):
        data = check_basic_success(self, '/categories',self.client().get)
        self.assertTrue(data['categories'])
    
    def test_GET_trivia_questions_fail(self):
        data = check_basic_failure(self, '/questions?page=1000', 404, self.client().get)

    # def test_DELETE_trivia_question_success(self):
    #     # If testing this multiple times, change the id it deletes.
    #     data = check_basic_success(self, '/questions/5', self.client().delete)
    #     self.assertTrue(data['deleted'])
    #     self.assertTrue(data['total_questions'])

    # def test_DELETE_trivia_question_fail(self):
    #     data = check_basic_failure(self, '/questions/1000', 404, self.client().delete)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()