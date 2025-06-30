from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @DONETODO: Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs
    """
    with app.app_context():
        db.create_all()

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
    @DONETODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def set_access_control_headers(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    """
    @DONETODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories_list = Category.query.all()
        categories_dict = {cat.id: cat.type for cat in categories_list}

        return jsonify({
            'success': True,
            'categories': categories_dict
        }), 200

    """
    @DONETODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages. Clicking on the page numbers
    should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        per_page = QUESTIONS_PER_PAGE
        questions_query = Question.query.order_by(Question.id).all()
        formatted_questions = [q.format() for q in questions_query]
        paginated = formatted_questions[(page-1)*per_page: page*per_page]

        if not paginated:
            abort(404)

        categories = {cat.id: cat.type for cat in Category.query.all()}

        return jsonify({
            'success': True,
            'questions': paginated,
            'totalQuestions': len(formatted_questions),
            'categories': categories,
            'currentCategory': None
        }), 200

    """
    @DONETODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed. This removal will persist in the
    database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def remove_question(question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({
            'success': True,
            'id': question_id
        }), 200

    """
    @DONETODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at
    the end of the last page of the questions list in
    the "List" tab.
    """
    # Note that the POST endpoint is merged with search below

    """
    @DONETODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        payload = request.get_json()
        search = payload.get('searchTerm', None)

        if search:
            matches = Question.query.filter(Question.question.ilike(f"%{search}%")).all()
            if not matches:
                abort(404)
            results = [m.format() for m in matches]
            return jsonify({
                'success': True,
                'questions': results,
                'totalQuestions': len(results),
                'currentCategory': None
            }), 200

        # If not a search, it's a create
        question_text = payload.get('question')
        answer_text = payload.get('answer')
        difficulty = payload.get('difficulty')
        category = payload.get('category')

        if not all([question_text, answer_text, difficulty, category]):
            abort(422)

        new_question = Question(
            question=question_text,
            answer=answer_text,
            difficulty=difficulty,
            category=category
        )
        new_question.insert()

        return jsonify({'success': True}), 201

    """
    @DONETODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category_obj = Category.query.get_or_404(category_id)
        filtered_questions = Question.query.filter_by(category=str(category_id)).all()
        formatted = [q.format() for q in filtered_questions]
        return jsonify({
            'success': True,
            'questions': formatted,
            'totalQuestions': len(formatted),
            'currentCategory': category_obj.type
        }), 200

    """
    @DONETODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()

        # Safely grab previous questions and category ID from the request
        seen_questions = data.get('previous_questions', [])
        selected_category = data.get('quiz_category', {}).get('id', None)

        # Filter out questions already asked, and by category if provided
        if selected_category and str(selected_category) != "0":
            available_questions = Question.query.filter(
                Question.category == str(selected_category),
                ~Question.id.in_(seen_questions)
            ).all()
        else:
            available_questions = Question.query.filter(
                ~Question.id.in_(seen_questions)
            ).all()

        # If no questions remain, return success with no question
        if not available_questions:
            return jsonify({
                "success": True,
                "question": None
            }), 200

        # Pick one question at random from what's left
        next_question = random.choice(available_questions)

        return jsonify({
            "success": True,
            "question": next_question.format()
        }), 200

    """
    @DONETODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # Handles 400: Bad Request
    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request. Please check your input."
        }), 400

    # Handles 404: Resource Not Found
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The requested resource could not be found."
        }), 404

    # Handles 405: Method Not Allowed
    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "This HTTP method is not allowed for the requested URL."
        }), 405

    # Handles 422: Unprocessable Entity
    @app.errorhandler(422)
    def handle_422(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable request."
        }), 422

    # Handles 500: Internal Server Error
    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Something went wrong on the server."
        }), 500

    return app
