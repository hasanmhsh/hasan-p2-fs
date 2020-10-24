import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {'origins': '*'}})
  

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      selection = Category.query.order_by(Category.id).all()

      total_size = len(selection)

      if total_size==0:
          abort(404)
      return jsonify({
        "success": True,
        "categories": [cat.type for cat in selection ]
      })

      
  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
      selection = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
      total_size = len(selection)

      if total_size==0:
          abort(404)
      current_questions = paginate_questions(request, selection)
      if len(current_questions)==0:
          abort(404)
      category_types = [cat.type for cat in categories ]
      return jsonify({
        "success": True,
        "questions": current_questions,
        # "questions": [question.question for question in current_questions],
        "total_questions": total_size,
        "categories": category_types,
        "current_category": -1
      })

  def paginate_questions(request, selection):
      page = request.args.get('page', 1, type=int)
      start = (page -1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = [question.format() for question in selection]
      current_questions = questions[start:end]
      return current_questions
      # return selection[start:end]

  
  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      success = True
      returned = {}
      try:
          question = Question.query.filter(Question.id == question_id).one_or_none()
          if question is None:
              abort(404)
          question.delete() 
          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request,selection)
          returned["success"] = True
          returned["deleted"] = question.id
          returned["questions"] = current_questions
          returned["total_questions"] = len(selection)
      except:
          success = False
          # Question.rollback()
      # finally:
          # Question.close()
      if success:
          return jsonify(returned)
      else:
          abort(422)


  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question_or_search():
      error = False
      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)
      search = body.get('searchTerm', None)
      test = body.get('test', None)
      # return search
      returned = {}


      try:
          if search: # is not None: #search
              selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
              current_questions = paginate_questions(request,selection)
              returned['success'] = True
              returned['questions'] = current_questions
              returned['total_questions'] = len(selection.all())
          else: #create new question
              question=Question(
                  question=new_question,
                  answer=new_answer,
                  difficulty=new_difficulty,
                  category=new_category
              )
              if test:
                question.id = body.get('id')
              question.insert()

              selection = Question.query.order_by(Question.id).all()
              current_questions = paginate_questions(request,selection)
              
              returned["success"] = True
              returned["created"] = question.id
              returned["questions"] = current_questions
              returned["total_questions"] = len(selection)
      except:
          error = True
          # Question.rollback()
          # print(sys.exc_info())
      # finally:
      #     Question.close()
      if error:
          abort(422)
      else:
          return jsonify(returned)

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_order>/questions')
  def get_category_questions(category_order):
      categories = Category.query.order_by(Category.id).all()
      selection = Question.query.filter(Question.category==str(category_order)).order_by(Question.id).all()
      total_size = len(selection)

      if total_size==0:
          abort(404)
      current_questions = paginate_questions(request, selection)
      return jsonify({
        "success": True,
        # "questions": [question.format() for question in selection],
        "questions": current_questions,
        # "questions": [question.question for question in current_questions],
        "total_questions": str(total_size),
        "categories": [cat.type for cat in categories ],
        "current_category": category_order
      })

  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def quiz():
      body = request.get_json()
      previous_question_ids = body.get('previous_questions', None)
      quiz_category = body.get('quiz_category', None)
      # categories = Category.query.order_by(Category.id).all()
      # previous_question_ids = [q['id'] for q in previous_questions]
      questions_to_return = []
      questions = []
      cat_index = int(quiz_category['id'])
      question_to_return = {}
      error = False
      try:
        if cat_index >= 0:
          #there is category
          cat_index += 1
          questions = Question.query.filter(Question.category==str(cat_index)).order_by(func.random()).all()
        else:
          # all questions
          questions = Question.query.order_by(func.random()).all()

        # if len(questions)==0:
        #   abort(404)

        for q in questions:
          if not q.id in previous_question_ids:
            questions_to_return.append(q.format())
        # quiz_category['question'] = questions_to_return[0]
        # return jsonify(quiz_category)
        question_to_return = questions_to_return[0]
      except:
        error = True
        # abort(404)

      return jsonify({
        "success": True,
        "question": question_to_return
      })



  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found",
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable",
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        "success": False,
          "error": 400,
          "message": "bad request",
      }), 400

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed",
      }), 405
  
  return app

    