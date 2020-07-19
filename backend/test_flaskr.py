import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db
from models import Question
from models import Category
from sqlalchemy import desc
from config import db_type
from config import db_username
from config import db_password
from config import db_host
from config import db_port
from config import db_test_name


class TriviaTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "{}://{}:{}@{}:{}/{}".format(
            db_type,
            db_username,
            db_password,
            db_host,
            db_port,
            db_test_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()

    def tearDown(self):

        pass

    """
    TODO(Done): Write at least one test for each test
    for successful operation and for expected errors.
    """

# ----------------------------------------------------------------------------#
# General Availability Test
# ----------------------------------------------------------------------------#

    def test_available_endpoint(self):

        res = self.client().get('/DoesNotExist')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Resource Not Found')

# ----------------------------------------------------------------------------#
# Tests for GET endpoint on /categories/<string:category_id>/questions
# ----------------------------------------------------------------------------#

    def test_get_questions_from_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            len(data['questions']) > 0)
        self.assertTrue(
            data['total_questions'] > 0)
        self.assertEqual(
            data['current_category'], '1')

    def test_400_get_questions_from_category(
            self):
        res = self.client().get(
            '/categories/1234567890/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(
            data['message'],
            'No questions with category 1234567890 found.')

# ----------------------------------------------------------------------------#
# Tests for POST endpoint on /questions
# ----------------------------------------------------------------------------#

    def test_create_question(self):

        json_create_question = {
            'question': 'Is this a test question?',
            'answer': 'Yes it is!',
            'category': '1',
            'difficulty': 1}

        res = self.client().post(
            '/questions',
            json=json_create_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            data['total_questions'] > 0)

    def test_error_create_question(self):

        json_create_question_error = {
            'question': 'Is this a test question?',
            'answer': 'Yes it is!',
            'difficulty': 1}

        res = self.client().post(
            '/questions',
            json=json_create_question_error)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Fill Category Field')

    def test_search_question(self):

        json_search_question = {
            'searchTerm': 'test',
            }

        res = self.client().post(
            '/questions',
            json=json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            len(data['questions']) > 0)
        self.assertTrue(
            data['total_questions'] > 0)

    def test_error_404_search_question(self):

        json_search_question = {
            'searchTerm': '~~~', }

        res = self.client().post(
            '/questions',
            json=json_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'Question containing "~~~": No Found.')

# ----------------------------------------------------------------------------#
# Tests for POST endpoint on /categories
# ----------------------------------------------------------------------------#

    def test_create_category(self):

        json_create_category = {
            'type': 'Udacity'
            }

        res = self.client().post(
            '/categories',
            json=json_create_category)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_400_create_category_with_missing_json(
            self):

        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Method Not Allowed')

# ----------------------------------------------------------------------------#
# Tests for GET endpoint on /categories
# ----------------------------------------------------------------------------#

    def test_get_all_categories(self):

        json_create_category = {
            'type': 'Udacity'
            }

        res = self.client().post(
            '/categories',
            json=json_create_category)

        res = self.client().get('/categories')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            len(data['categories']) > 0)

    def test_error_405_get_all_categories(self):

        res = self.client().patch('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(
            data['message'],
            "Method Not Allowed")
        self.assertEqual(data['success'], False)

# ----------------------------------------------------------------------------#
# Tests for GET endpoint on /questions
# ----------------------------------------------------------------------------#

    def test_get_all_questions_paginated(self):

        res = self.client().get(
            '/questions?page=1',
            json={'category:': 'science'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            data['total_questions'] > 0)

    def test_error_405_get_all_questions_paginated(
            self):

        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(
            data['message'],
            "Method Not Allowed")
        self.assertEqual(data['success'], False)

    def test_error_404_get_all_questions_paginated(
            self):

        res = self.client().get(
            '/questions?page=1234567890')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(
            data['message'],
            "Resource Not Found")
        self.assertEqual(data['success'], False)

# -------------------------------------------------h---------------------------#
# Tests for DELETE endpoint /categories
# ----------------------------------------------------------------------------#

    def test_delete_category(self):

        last_category_id = Category.query.order_by(
            desc(Category.id)).first().id
        res = self.client().delete(
            '/categories/{}'.format(last_category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_delete_category(self):

        res = self.client().delete(
            '/categories/{}'.format(12345678790))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Resource Not Found')

# ----------------------------------------------------------------------------#
# Tests for POST endpoint on /quizzes
# ----------------------------------------------------------------------------#

    def test_play_quiz_with_category(self):

        json_play_quizz = {
            'previous_questions': [1, 2, 3],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
                }
            }
        res = self.client().post(
            '/quizzes', json=json_play_quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            data['question']['question'])
        self.assertTrue(
            data['question']['id']
            not
            in
            json_play_quizz
            ['previous_questions'])

    def test_play_quiz_without_category(self):

        json_play_quizz = {
            'previous_questions': [1, 2, 3]
            }
        res = self.client().post(
            '/quizzes', json=json_play_quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(
            data['question']['question'])
        self.assertTrue(
            data['question']['id']
            not
            in
            json_play_quizz
            ['previous_questions'])

    def test_error_400_play_quiz(self):

        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'No JSON Body')

    def test_error_405_play_quiz(self):

        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Method Not Allowed')


if __name__ == "__main__":
    unittest.main()
