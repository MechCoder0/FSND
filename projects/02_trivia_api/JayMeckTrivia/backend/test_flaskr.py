import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

def check_basic_success(self, url, http_method):
    return basic_check(self, url, http_method, self.assertTrue)

def check_basic_failure(self, url, code, http_method):
    return basic_check(self, url, http_method, self.assertFalse, code)

def basic_check(self, url, http_method, assert_method, code=200):
    res = http_method(url)
    data = json.loads(res.data)
    assert_method(data['success'])
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

        self.new_question = {
            'question': 'new_question',
            'answer': 'new_answer',
            'category': 4,
            'difficulty': 4
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_GET_trivia_questions(self):
        data = check_basic_success(self, '/questions', self.client().get)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) <= 10)

    def test_GET_categories(self):
        data = check_basic_success(self, '/categories',self.client().get)
        self.assertTrue(data['categories'])
    
    def test_GET_trivia_questions_fail(self):
        data = check_basic_failure(self, '/questions?page=1000', 404, self.client().get)

    def test_DELETE_trivia_question_success(self):
        # If testing this multiple times, change the id it deletes.
        data = check_basic_success(self, '/questions/1', self.client().delete)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_questions'])

    def test_DELETE_trivia_question_fail(self):
        data = check_basic_failure(self, '/questions/1000', 404, self.client().delete)

    def test_POST_trivia_questions(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_POST_trivia_questions_fail(self):
        check_basic_failure(self, '/questions', 400, self.client().post)

    def test_POST_search_question(self):
        res = self.client().post('/questions/search', json={'searchTerm':'question'})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])

    def test_GET_questions_by_category(self):
        data = check_basic_success(self, 'categories/1/questions', self.client().get)
        self.assertEqual(1, data['current_category'])

    def test_GET_questions_by_category_fail(self):
        check_basic_failure(self, 'categories/1000/questions', 404, self.client().get)

    def test_POST_question_for_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category':{'id':1}})
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_POST_question_for_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions':[], 'quiz_category':{'id':0}})
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_POST_question_for_quiz_fail(self):
        check_basic_failure(self,'/quizzes', 400, self.client().post)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()