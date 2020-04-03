import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

ITEMS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  def paginate_items(items, page):
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    formatted_items = [item.format() for item in items]
    return formatted_items[start:end]

  '''
  The after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response

  '''
  An endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_trivia_categories():
    categories = Category.query.all()
    formatted_categories = {cat.id:cat.type for cat in categories}
    return jsonify({
      'success': True,
      'categories':formatted_categories
    })

  '''
  An endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should returns a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_trivia_questions():
    page=request.args.get('page',1, type=int)
    questions = Question.query.all()
    paginated_questions = paginate_items(questions, page)
    if(len(paginated_questions)==0):
      abort(404)
    current_category = paginated_questions[1]['category']
    categories = Category.query.all()
    formatted_categories = {cat.id:cat.type for cat in categories}
    return jsonify({
      'success': True,
      'total_questions': len(questions),
      'questions': paginated_questions,
      'categories': formatted_categories,
      'current_category': current_category
    })


  '''
  Deletes the question with the id passed. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_trivia_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if(question is None):
      abort(404)

    try:
      remaining_questions = Question.query.all()
      question.delete()
      return jsonify({
        'success': True,
        'deleted':question_id,
        'total_questions':len(remaining_questions)
      })
    except:
      abort(422)


  '''
  Creates a new question using the json body passed 
  in the request. 
  '''

  @app.route('/questions', methods=['POST'])
  def add_trivia_question():
    body = request.get_json()

    if body is None:
      abort(400)

    try:
      question = body.get('question', None)
      answer = body.get('answer', None)
      difficulty = body.get('difficulty', None)
      category = body.get('category', None)
    except:
      abort(401)

    try:
      new_question = Question(question, answer, category, difficulty)
      new_question.insert()

      all_questions = Question.query.all()

      return jsonify({
        'success':True,
        'created': new_question.id,
        # 'questions': [question.format() for question in all_questions],
        'total_questions': len(all_questions)
      })
    except:
      abort(422)

  '''
  A POST endpoint to get questions based on a search term. 
  It will return any questions for whom the search term 
  is a substring of the question. 

  Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    if body is None:
      abort(400)

    search_term = body.get('searchTerm')
    questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
    paginated_questions = paginate_items(questions, 1)
    
    if(len(paginated_questions) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(questions),
      'current_category': paginated_questions[0]['category']
    })

  '''
  A GET endpoint to get questions based on category. 

  In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_for_category(category_id):
    questions = Question.query.filter(Question.category == category_id).all()
    if(questions is None or len(questions) == 0):
      abort(404)

    paginated_questions = paginate_items(questions, 1)

    return jsonify({
      'success': True,
      'questions':paginated_questions,
      'total_questions':len(paginated_questions),
      'current_category':paginated_questions[0]['category']
    })

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

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success":False,
      "error": 404,
      "message": 'Not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success":False,
      "error": 422,
      "message": 'Unprocessable Entity'
    }), 422
  
  return app

    