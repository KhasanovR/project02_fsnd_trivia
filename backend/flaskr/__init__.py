import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):

  app = Flask(__name__)
  setup_db(app)

  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
  
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
    
    ret_categories = []
    for cat in categories_all:
      ret_categories.append(cat['type'])

    return jsonify({
      'success': True,
      'categories' : ret_categories
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
  @app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    paginated_questions = paginate_questions(request, selection)
    if len(paginated_questions) == 0:
      abort(404)

    categories = Category.query.all()
    categories_all = [category.format() for category in categories]
    
    ret_categories = []
    for cat in categories_all:
      ret_categories.append(cat['type'])
    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(selection),
      'categories' : ret_categories,
      'current_category' : ret_categories 
      })

  '''
  @TODO(Done): Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
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

  
  @app.route('/questions', methods=['POST'])
  def create_or_search_questions():
    body = request.get_json()

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    
    search_term = body.get('searchTerm', None)
    
    if search_term is None:
      '''
      @TODO(Done): 
      Create an endpoint to POST a new question, 
      which will require the question and answer text, 
      category, and difficulty score.

      TEST: When you submit a question on the "Add" tab, 
      the form will clear and the question will appear at the end of the last page
      of the questions list in the "List" tab.  
      '''
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
    else:
      '''
      @TODO(Done): Create a POST endpoint to get questions based on a search term. 
      It should return any questions for whom the search term 
      is a substring of the question. 

      TEST: Search by any phrase. The questions list will update to include 
      only question that include that string within their question. 
      Try using the word "title" to start. 
      '''
      questions = Question.query.filter(Question.question.like("%{}%".format(search_term))).all()

      if not questions:
        abort(404, {'message': 'Question containing "{}": No Found.'.format(search_term)})
    
      questions_found = [question.format() for question in questions]

      return jsonify({
        'success': True,
        'questions': questions_found,
      })


  '''
  @TODO: Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO(Done): Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():

    body = request.get_json()

    if not body:
      abort(400, {'message': 'Please provide a JSON body with previous question Ids and optional category.'})
    
    prev_questions = body.get('previous_questions', None)
    cur_category = body.get('quiz_category', None)

    if not prev_questions:
      if cur_category:
        questions = (Question.query
          .filter(Question.category == str(cur_category['id']))
          .all())
      else:
        questions = (Question.query.all())    
    else:
      if cur_category:
        questions = (Question.query
          .filter(Question.category == str(cur_category['id']))
          .filter(Question.id.notin_(prev_questions))
          .all())
      else:
        questions = (Question.query
          .filter(Question.id.notin_(prev_questions))
          .all())
    
    formatted_questions = [question.format() for question in questions]
    random_question = formatted_questions[random.randint(0, len(formatted_questions))]
    
    return jsonify({
        'success': True,
        'question': random_question
      })

  '''
  @TODO: Create error handlers for all expected errors including 404 and 422. 
  '''
  def get_error_message(error, text):
    try:
      return error.description["message"]
    except TypeError:
      return text

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": get_error_message(error, "Bad Request")
      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": get_error_message(error, "Resource Not Found")
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": get_error_message(error, "Method Not Allowed")
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": get_error_message(error, "Unprocessable")
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": get_error_message(error,"Internal Server Error")
      }), 500
  
  return app

    