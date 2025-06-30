# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Documentation

### Error Handling
All errors are returned in JSON format:

```json
{
  "success": false,
  "error": 404,
  "message": "The requested resource could not be found."
}
```

Error types will be returned by the API when requests fail. These include:

400: Bad Request

404: Resource Not Found

405: Method Not Allowed

422: Unprocessable Request

500: Internal Server Error

### Endpoints
### GET /categories 

This returns a list of categories along with a success value

```bash

curl http://127.0.0.1:5000/categories

```
```bash

{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}

```

Questions are returned and paginated in groups of 10.

### DELETE /questions/{id}

This deletes the question of the given ID if it exists along with a success value.

```bash
curl -X DELETE http://127.0.0.1:5000/questions/1?page=1
```
```bash
{
  "success": true
}
```

### POST /questions/{id}

This creates a new question using title, answer, category and difficulty as shown in the example below. It returns a success value.

```bash
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the capital of Spain?", "answer": "Madrid","category" :"3", "difficulty":"1"}'
```

```bash
{
  "success": true
}
```

### POST /search

This allows the search of a question using the submitted search term and returns the results, success value, total questions.


```bash
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'
```

```bash
{
  "currentCategory":null,
  "questions":[
    {
      "answer":"Maya Angelou",
      "category":4,
      "difficulty":2,
      "id":5,
      "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer":"George Washington Carver",
      "category":4,
      "difficulty":2,
      "id":12,
      "question":"Who invented Peanut Butter?"
    },
    {
      "answer":"Alexander Fleming",
      "category":1,
      "difficulty":3,
      "id":21,
      "question":"Who discovered penicillin?"
    }
  ],
  "success":true,
  "totalQuestions":3
}
```

### GET /categories/{id}/questions

This returns a list of questions, in the given category, category total_questions and success value
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

```bash
curl http://127.0.0.1:5000/categories/3/questions
```

```bash
{
  "currentCategory":"Geography",
  "questions":[
    {
      "answer":"Lake Victoria",
      "category":3,
      "difficulty":2,
      "id":13,
      "question":"What is the largest lake in Africa?"
    },
    {
      "answer":"The Palace of Versailles",
      "category":3,
      "difficulty":3,
      "id":14,
      "question":"In which royal palace would you find the Hall of Mirrors?"},
    {
      "answer":"Agra",
      "category":3,
      "difficulty":2,
      "id":15,
      "question":"The Taj Mahal is located in which Indian city?"},
    {
      "answer":"Madrid",
      "category":3,
      "difficulty":1,
      "id":24,
      "question":"What is the capital of Spain?"}
  ],
  "success":true,"totalQuestions":4
}
```

### POST /quizzes

This will receive the actual question and the category and return the next question in the same category and a success value.

```bash
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[1]}'
```

```bash
{
  "question":
  {
    "answer":"Lake Victoria",
    "category":3,
    "difficulty":2,"id":13,
    "question":"What is the largest lake in Africa?"
  },
  "success":true
}
```
# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure, plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

---

## API Documentation (Kamal D Natwest)

### Error Handling

All errors are returned in JSON format:

```json
{
  "success": false,
  "error": 404,
  "message": "The requested resource could not be found."
}
```

Possible error codes:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable Request
- 500: Internal Server Error

---

### Endpoints

#### GET /categories

Get a list of available categories.

```bash
curl http://127.0.0.1:5000/categories
```

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

#### GET /questions?page=\<page\_number>

Fetches a paginated list of questions (10 per page) and category info.

```bash
curl http://127.0.0.1:5000/questions?page=1
```

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of Italy?",
      "answer": "Rome",
      "category": 3,
      "difficulty": 2
    }
    // ...
  ],
  "totalQuestions": 24,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography"
    // ...
  },
  "currentCategory": null
}
```

---

#### DELETE /questions/\<question\_id>

Remove a question by its ID.

```bash
curl -X DELETE http://127.0.0.1:5000/questions/5
```

```json
{
  "success": true,
  "id": 5
}
```

---

#### POST /questions

If you provide a `searchTerm`, this acts as a search endpoint.\
Otherwise, it creates a new question.

**Create a new question:**

```bash
curl -X POST http://127.0.0.1:5000/questions \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the capital of Spain?", "answer":"Madrid", "category":"3", "difficulty":1}'
```

```json
{
  "success": true
}
```

**Search for questions:**

```bash
curl -X POST http://127.0.0.1:5000/questions \
  -H "Content-Type: application/json" \
  -d '{"searchTerm":"who"}'
```

```json
{
  "success": true,
  "questions": [
    {
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2
    },
    {
      "id": 12,
      "question": "Who invented Peanut Butter?",
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2
    }
  ],
  "totalQuestions": 2,
  "currentCategory": null
}
```

---

#### GET /categories/\<category\_id>/questions

Get questions filtered by category.

```bash
curl http://127.0.0.1:5000/categories/3/questions
```

```json
{
  "success": true,
  "questions": [
    {
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2
    },
    {
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3
    }
  ],
  "totalQuestions": 2,
  "currentCategory": "Geography"
}
```

---

#### POST /quizzes

Request the next quiz question that hasn't been seen, optionally filtered by category.

```bash
curl -X POST http://127.0.0.1:5000/quizzes \
  -H "Content-Type: application/json" \
  -d '{"quiz_category":{"id":"3"}, "previous_questions":[1,13]}'
```

```json
{
  "success": true,
  "question": {
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?",
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3
  }
}
```

when no more questions,`"question"` will be `null`

---

### Example Error Responses

**404 Not Found**

```json
{
  "success": false,
  "error": 404,
  "message": "The requested resource could not be found."
}
```

**422 Unprocessable Entity**

```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable request."
}
```

All endpoints return JSON. Pagination for questions is in groups of 10.\
For more usage examples, see the test file.