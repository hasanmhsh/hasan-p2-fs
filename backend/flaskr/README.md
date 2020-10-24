# The Quiz project (trivia)

This project is a quizz project which provide a way to test individuals by providing a platform of categorized questions and provide a way to add them and create exams with categorized or non-categorized and randomized questions with no repetetions, every question is consists of categor and question and answer and difficulty , Fullstack platform structure contain a number of endpoints which used by front end app to query or manipulate database in an specefied demand. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


## Getting Started

### Pre-requisites and Local Development 
Developers who will use this project must have Python3 and pip and node installed on their workstations.

#### Backend

First you must install back end dependence , in backend folder type this command in shell
`pip install requirements.txt`

To run the app execute the following command
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands setup the application in development mode and use `__init__.py` 

application is running on `http://127.0.0.1:5000/` by default and is a proxy on the frontend settings. 

#### Frontend

Execute the following commands in the frontend folder: 
```
npm install // once
npm start 
```

The frontend is running on localhost:3000. 

### Tests
To run tests change directory to 'backend' folder then execute the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < questions.psql
python test_flaskr.py
```

First time neglect dropdb command. 

## API Reference

### Getting Started
- Base URL: backend app is running by default on this endpoint, `http://127.0.0.1:5000/`, which is s proxy in the frontend settings. 


### Error Handling
Errors are issued in JSON format as following:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
API will issue three error types at failure:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories objects, success value, and total number of questions
- Sample: `curl http://127.0.0.1:5000/categories`
``` 
{
  "categories": [
    {
      "type": "Geography",
      "id": 1
    },
    {
      "type": "History",
      "id": 1
    }
  ],
"success": true
}
```

#### GET /questions
- General:
    - Returns a list of questions objects, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` 
{
  "questions": [
    {
      "question": "where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    }
  ],
"success": true,
"total_questions": 45
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"What is your name?", "answer":"hhh", "category":"5", "difficulty": 4}'`
```
{
  "questions": [
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    }
  ],
  "created": 55,
  "success": true,
  "total_questions": 46
}
```

#### POST /questions
- General:
    - Searches in questions with part of question ignoring case of letters. 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"where"}`
```
{
  "questions": [
    {
      "question": "where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    }
  ],
"success": true,
"total_questions": 45
}

```
#### DELETE /questions/{book_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`
```
{
  "questions": [
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    },
    {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
    }
  ],
  "deleted": 23,
  "success": true,
  "total_questions": 42
}
```
#### POST /quizzes
- General:
    - Returns a question of required category or un categorized which is randomized with no repetetins
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"category":{"type": "Gegraphy", "id": "1"}, "previous_questions":[2, 3, 4]}'`
``` 
{
  "category": {
  {
    "type": "Geography",
    "id": 1
  },
  "question": {
      "question": "Where is athenes?",
      "id": 1,
      "answer": "greece",
      "category": "Giography",
      "difficulty": 3
  },
  "success": true
}
```

## Authors
Hasan

## Acknowledgements 
The awesome team at Udacity and all of the instructors, mentors and reviewers
