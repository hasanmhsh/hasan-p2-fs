import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test2"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'id' : 909,
            'question': 'Which programming language do you prefer hasan-m.shehata?',
            'answer': 'answer1',
            'category': '1',
            'difficulty': 5,
            'test': True
        }

        self.new_question2 = {
            'id' : 910,
            'question': 'Which programming language do you prefer?',
            'answer': 'answer1',
            'category': '1',
            'difficulty': 5,
            'test': True
        }

        try:
            self.client().post('/questions', json=self.new_question)
        except:
            error = True

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question2) # new_book is creating during setup above ^
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']) #test existance
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'prefer hasan-m.shehata'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'How much'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)



    def test_get_only_category_questions(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        for question in data['questions']:
            self.assertEqual(question['category'], '1')

    def test_get_only_category_questions_of_empty_category(self):
        res = self.client().get('/questions/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_one_question_only_at_atime_is_displayed_in_play_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': '1'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(isinstance(data['question'], list))


    def test_delete_question(self):
        res = self.client().delete('/questions/910')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 910).one_or_none()
      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 910)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

