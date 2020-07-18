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
# General Test
#----------------------------------------------------------------------------#
    
    def test_endpoint_not_available(self):
        """Test getting an endpoint which does not exist """
        res = self.client().get('/DoesNotExist')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()