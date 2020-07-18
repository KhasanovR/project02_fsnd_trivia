import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO(Done): Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO(Done): Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO(Done): Create an endpoint to handle GET requests for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()

    if not categories:
      abort(404)

    categories_all = [category.format() for category in categories]
    
    categories_returned = []
    for cat in categories_all:
      categories_returned.append(cat['type'])

    return jsonify({
      'success': True,
      'categories' : categories_returned
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO(Done): Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    question = Question.query.get(question_id)
    if not question:
      abort(400, {'message': 'Question ID {}: Not Found'.format(question_id)})
    try:
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
      abort(422)

  '''
  @TODO(Done): 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_or_search_questions():
    body = request.get_json()

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    if not new_question:
      abort(400, {'message': 'Fill Question Field'})

    if not new_answer:
      abort(400, {'message': 'Fill Answer Field'})

    if not new_category:
      abort(400, {'message': 'Fill Category Field'})

    if not new_difficulty:
      abort(400, {'message': 'Fill Difficulty Field'})

    try:
      question = Question(
        question = new_question, 
        answer = new_answer, 
        category= new_category,
        difficulty = new_difficulty
        )
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id,
        'question': {
          'question': question.question,
          'answer': question.answer,
          'category': question.category,
          'difficulty': question.difficulty
        }
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    