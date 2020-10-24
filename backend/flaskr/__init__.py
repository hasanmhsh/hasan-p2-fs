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

  # @app.route('/categories/create/debug-only')
  # def c_categories():
  #     cats = Category.query.all()
  #     for cat in cats:
  #       db.session.delete(cat)
  #     db.session.commit()
  #     cat1 = Category(type = "cat1")
  #     cat2 = Category(type = "cat2")
  #     cat3 = Category(type = "cat3")
  #     cat4 = Category(type = "cat4")
  #     cat5 = Category(type = "cat5")
  #     cat6 = Category(type = "cat6")
  #     db.session.add(cat1)
  #     db.session.add(cat2)
  #     db.session.add(cat3)
  #     db.session.add(cat4)
  #     db.session.add(cat5)
  #     db.session.add(cat6)
  #     db.session.commit()
  #     return 'done'
      
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
      return jsonify({
        "success": True,
        "questions": current_questions,
        # "questions": [question.question for question in current_questions],
        "total_questions": total_size,
        "categories": [cat.type for cat in categories ],
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

  @app.route('/questions/create/debug-only')
  def c_categories():
      questions = Question.query.all()
      # for q in questions:
      #   db.session.delete(q)
      # db.session.commit()
      Question(question="question19?", answer="answer19", category="cat1", difficulty=10).insert()
      Question(question="question20?", answer="answer20", category="cat2", difficulty=20).insert()
      Question(question="question21?", answer="answer21", category="cat3", difficulty=30).insert()
      Question(question="question22?", answer="answer22", category="cat4", difficulty=40).insert()
      Question(question="question23?", answer="answer23", category="cat5", difficulty=50).insert()
      Question(question="question24?", answer="answer24", category="cat6", difficulty=60).insert()
      Question(question="question25?", answer="answer25", category="cat1", difficulty=70).insert()
      Question(question="question26?", answer="answer26", category="cat2", difficulty=80).insert()
      Question(question="question27?", answer="answer27", category="cat3", difficulty=90).insert()
      Question(question="question28?", answer="answer28", category="cat4", difficulty=100).insert()
      Question(question="question29?", answer="answer29", category="cat5", difficulty=110).insert()
      Question(question="question30?", answer="answer30", category="cat6", difficulty=120).insert()
      Question(question="question31?", answer="answer31", category="cat1", difficulty=130).insert()
      Question(question="question32?", answer="answer32", category="cat2", difficulty=140).insert()
      Question(question="question33?", answer="answer33", category="cat3", difficulty=150).insert()
      Question(question="question34?", answer="answer34", category="cat4", difficulty=160).insert()
      Question(question="question35?", answer="answer35", category="cat5", difficulty=170).insert()
      Question(question="question36?", answer="answer36", category="cat6", difficulty=180).insert()
      return 'done'
    
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
      selection = Question.query.filter(Question.category==str(category_order+1)).order_by(Question.id).all()
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
  @TODO: 
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
      categories = Category.query.order_by(Category.id).all()
      # previous_question_ids = [q['id'] for q in previous_questions]
      questions_to_return = []
      questions = []
      if quiz_category['type'] in [category.type for category in categories]:
        #there is category
        questions = Question.query.filter(Question.category==quiz_category['type']).order_by(func.random()).all()
      else:
        # all questions
        questions = Question.query.order_by(func.random()).all()

      for q in questions:
        if not q.id in previous_question_ids:
          questions_to_return.append(q.format())
      # quiz_category['question'] = questions_to_return[0]
      # return jsonify(quiz_category)
      return jsonify({
        "question": questions_to_return[0]
      })



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    