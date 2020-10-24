import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
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
        "current_category": current_questions[0]['category']
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
      for q in questions:
        db.session.delete(q)
      db.session.commit()
      Question(question="question1?", answer="answer1", category="cat1", difficulty=10).insert()
      Question(question="question2?", answer="answer2", category="cat2", difficulty=20).insert()
      Question(question="question3?", answer="answer3", category="cat3", difficulty=30).insert()
      Question(question="question4?", answer="answer4", category="cat4", difficulty=40).insert()
      Question(question="question5?", answer="answer5", category="cat5", difficulty=50).insert()
      Question(question="question6?", answer="answer6", category="cat6", difficulty=60).insert()
      Question(question="question7?", answer="answer7", category="cat1", difficulty=70).insert()
      Question(question="question8?", answer="answer8", category="cat2", difficulty=80).insert()
      Question(question="question9?", answer="answer9", category="cat3", difficulty=90).insert()
      Question(question="question10?", answer="answer10", category="cat4", difficulty=100).insert()
      Question(question="question11?", answer="answer11", category="cat5", difficulty=110).insert()
      Question(question="question12?", answer="answer12", category="cat6", difficulty=120).insert()
      Question(question="question13?", answer="answer13", category="cat1", difficulty=130).insert()
      Question(question="question14?", answer="answer14", category="cat2", difficulty=140).insert()
      Question(question="question15?", answer="answer15", category="cat3", difficulty=150).insert()
      Question(question="question16?", answer="answer16", category="cat4", difficulty=160).insert()
      Question(question="question17?", answer="answer17", category="cat5", difficulty=170).insert()
      Question(question="question18?", answer="answer18", category="cat6", difficulty=180).insert()
      return 'done'
    
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

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

    