import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from sqlalchemy import desc


class TriviaTestCase(unittest.TestCase):
    
    def setUp(self):
    
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "{}://{}:{}@{}/{}".format('postgresql','postgres','0820','localhost:5432', 'trivia_test')
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            
            self.db.create_all()
    
    def tearDown(self):
        
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

#----------------------------------------------------------------------------#
# General Availability Test
#----------------------------------------------------------------------------#
    
    def test_available_endpoint(self):
        
        res = self.client().get('/DoesNotExist')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

#----------------------------------------------------------------------------#
# Tests for GET endpoint on /categories/<string:category_id>/questions 
#----------------------------------------------------------------------------#
    
    def test_get_questions_from_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(data['current_category'], '1')

    def test_400_get_questions_from_category(self):
        res = self.client().get('/categories/14125412/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'No questions with category 14125412 found.')

if __name__ == "__main__":
    unittest.main()