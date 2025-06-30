import os
import unittest
from dotenv import load_dotenv
from flaskr import create_app
from models import db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """Test suite for Trivia application."""

    def setUp(self):
        """Initialize test environment and setup database connection."""
        load_dotenv()
        db_test_name = os.getenv('DB_TEST_NAME')
        db_test_user = os.getenv('DB_TEST_USER')
        db_test_host = os.getenv('DB_TEST_HOST')
        self.db_path = f"postgresql://{db_test_user}@{db_test_host}/{db_test_name}"

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.db_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        pass

    # """
    # DONETODO
    # Write at least one test for each test for successful operation and for expected errors.
    # """
    def post_json(self, endpoint, payload):
        return self.client.post(endpoint, json=payload)

    def test_get_categories(self):
        response = self.client.get('/categories')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['categories']), 0)

    def test_get_categories_error(self):
        with self.app.app_context():
            Category.query.delete()
            db.session.commit()
        response = self.client.get('/categories')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 0)
        with self.app.app_context():
            db.session.add_all([
                Category(type='Science'),
                Category(type='Art'),
                Category(type='Geography')
            ])
            db.session.commit()

    def test_get_paginated_questions(self):
        response = self.client.get('/questions?page=1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)

    def test_get_paginated_questions_error(self):
        response = self.client.get('/questions?page=999')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        with self.app.app_context():
            question = Question.query.first()
            if not question:
                new_q = Question(question="Test Q", answer="Test A", category=1, difficulty=1)
                db.session.add(new_q)
                db.session.commit()
                question = new_q
            q_id = question.id
        response = self.client.delete(f'/questions/{q_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        with self.app.app_context():
            self.assertIsNone(Question.query.get(q_id))

    def test_delete_question_error(self):
        response = self.client.delete('/questions/99999')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_question(self):
        new_question = {
            "question": "What is the largest planet?",
            "answer": "Jupiter",
            "category": 1,
            "difficulty": 2
        }
        response = self.post_json('/questions', new_question)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        with self.app.app_context():
            found = Question.query.filter_by(question=new_question['question']).first()
            self.assertIsNotNone(found)

    def test_create_question_error(self):
        incomplete = {
            "question": "Where is the Eiffel Tower?",
            "answer": "Paris"
        }
        response = self.post_json('/questions', incomplete)
        data = response.get_json()
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_search_question(self):
        response = self.post_json('/questions', {"searchTerm": "planet"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)

    def test_search_question_error(self):
        response = self.post_json('/questions', {"searchTerm": "zzzzzzzzzzz"})
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_questions_by_category(self):
        response = self.client.get('/categories/1/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)

    def test_get_questions_by_category_error(self):
        response = self.client.get('/categories/99999/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_play_quiz(self):
        payload = {
            "previous_questions": [],
            "quiz_category": {"id": 1}
        }
        response = self.post_json('/quizzes', payload)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)

if __name__ == "__main__":
    unittest.main()
