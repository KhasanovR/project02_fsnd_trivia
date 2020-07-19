# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

1. (optional) To execute tests, run
```bash 
$ dropdb trivia_test
$ createdb trivia_test
$ psql trivia_test < trivia.psql
$ python test_flaskr.py
```

## API Documentation

There you will see all the current endpoints, the strategies should be used, how to operate for them, and an overview of the responses you'll receive.

In addition, common pitfalls & error messages are explained, if applicable.

### Available Endpoints

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|-------|---------|
      /questions    |  [✓] |  [✓]  |   [✓]   |         
      /categories   |  [✓] |  [✓]  |   [✓]   |           
      /quizzes      |      |  [✓]  |         | 


### How to work with each endpoint

1. Questions
   1. [GET /questions](#get_questions)
   2. [POST /questions](#post_questions)
   3. [DELETE /questions/<question_id>](#delete_questions)
2. Categories
   1. [GET /categories](#get_categories)
   2. [GET /categories/<category_id>/questions](#get_categories_questions)
   3. [POST /categories](#post_categories)
   4. [DELETE /categories](#delete_categories)
3. Quizzes
   1. [POST /quizzes](#post_quizzes)

# <a name="get_questions"></a>
### 1. GET /questions

```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```
- Request Arguments: 
    - **integer** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. `questions`:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **list** `categories`
  3. **list** `current_category`
  4. **integer** `total_questions`
  5. **boolean** `success`

Output: 
#### Example response
```js
{
"categories": [
    "Category 1",
    "Category 2",
    "Category 3",
    "Category 4",
    "Category 5",
    "Category 6",
    "Category 7"
  ],
"current_category": [
    "Category 1",
    "Category 2",
    "Category 3",
    "Category 4",
    "Category 5",
    "Category 6",
    "Category 7"
  ],
"questions": [
    {
      "answer": "Answer 2",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "Question 2?"
    },
    {
      "answer": "Answer 2",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "Question 2?"
    },

 [...]

  ],
  "success": true,
  "total_questions": 19
}

```
#### Errors

```bash
curl -X GET http://127.0.0.1:5000/questions?page=1234567890
```

Output:
```js
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false
}

```

# <a name="post_questions"></a>
### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'
```

Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a test question?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'
```

- Request Arguments: **None**
- Request Headers :
  - **search** (_application/json_)
       1. **string** `searchTerm`
  - **insert** (_application/json_) 
       1. **string** `question`
       2. **string** `answer`
       3. **string** `category`
       4. **integer** `difficulty`
- Returns: 
  - Search:
    1. `questions` matching `searchTerm`:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. `current_category`:
        - **integer** `id`
        - **string** `type`
    3. **integer** `total_questions`
    4. **boolean** `success`
  - Insert:
    1. `questions`:
        - **integer** `id` 
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. **integer** `total_questions`
    3. **integer** `created` inserted question id
    4. **boolean** `success`

Output: 
#### Example response
Search Questions
```js
{
  "current_category": [
    {
      "id": 1,
      "type": "Category 1"
    },
    {
      "id": 2,
      "type": "Category 2"
    },

   [...] 

  ],
  "questions": [
    {
      "answer": "Yes, it is!",
      "category": 1,
      "difficulty": 1,
      "id": 10,
      "question": "Is this a test question?"
    }

    [...] 
  
  ],
  "success": true,
  "total_questions": 20
}

```
Create Question
```js
{
  "created": 8, 
  "questions": [
    {
      "answer": "Answer 8",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "Question 8?"
    },
   
   [...]

  ],
  "success": true,
  "total_questions": 21
}

```


#### Errors
**Search related**

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 
```

Output:
```js
{
  "error": 404,
  "message": "No questions that contains \"this does not exist\" found.",
  "success": false
}
```
**Insert related**

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Question withou answer?", "category" : "1" , "difficulty" : 1 }' -H 'Content-Type: application/json'
```

Output:
```js
{
  "error": 400,
  "message": "Fill Answer Field",
  "success": false
}
```
# <a name="delete_questions"></a>
### 3. DELETE /questions/<question_id>

```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```

- Request Arguments: 
  - **integer** `question_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` Id from deleted question.
    - **boolean** `success`

Output: 
#### Example response
```js
{
  "deleted": 10,
  "success": true
}
```

### Errors

If you try to delete a `question` which does not exist, it will throw an `400` error:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/7
```

Output:
```js
{
  "error": 400,
  "message": "Question with id 7 does not exist.",
  "success": false
}
```

# <a name="post_quizzes"></a>
### 4. POST /quizzes

Play quiz game.
```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Headers : 
     1. **list** `previous_questions` with **integer** ids from already asked questions
     1. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **integer** id from category
- Returns: 
  1. Exactly one `question` as **dict** with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **boolean** `success`

Output: 
#### Example response
```js
{
  "question": {
    "answer": "Jup",
    "category": 1,
    "difficulty": 1,
    "id": 24,
    "question": "Is this a test question?"
  },
  "success": true
}

```
### Errors

```bash
curl -X POST http://127.0.0.1:5000/quizzes
```

Output:
```js
{
  "error": 400,
  "message": "Please provide a JSON body with previous question Ids and optional category.",
  "success": false
}

```
# <a name="get_categories"></a>
### 5. GET /categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Request Arguments: **None**
- Request Headers : **None**

Output: 
#### Example response
```js
{
  "categories": [
    "Category 1",
    "Category 2",
    "Category 3",
    "Category 4",
    "Category 5",
    "Category 6",
    "Category 7"
  ],
  "success": true
}
```

# <a name="get_categories_questions"></a>
### 6. GET /categories/<category_id>/questions

```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```

- Request Arguments:
  - **integer** `category_id`
  - **integer** `page` (optinal, 10 questions per Page, defaults to `1` if not given)
- Request Headers: **None**

- Returns: 
  1. **integer** `current_category` inputted `category` id
  2. `questions`:
     - **integer** `id` 
     - **string** `question`
     - **string** `answer`
     - **string** `category`
     - **integer** `difficulty`
  3. **integer** `total_questions`
  4. **boolean** `success`

Output: 
#### Example response
```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Answer 5",
      "category": 2,
      "difficulty": 1,
      "id": 5,
      "question": "Question 5?"
    },
    {
      "answer": "Answer 6",
      "category": 2,
      "difficulty": 3,
      "id": 6,
      "question": "Question 6?"
    },
    {
      "answer": "Answer 7",
      "category": 2,
      "difficulty": 4,
      "id": 7,
      "question": "Question 7?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### Errors

```bash
curl -X GET http://127.0.0.1:5000/categories/10/questions?page=1
```

Output:
```js
{
  "error": 400,
  "message": "No questions with category 10 found.",
  "success": false
}
```

```bash
curl -X GET http://127.0.0.1:5000/categories/1/questions?page=5
```

Output:
```js
{
  "error": 404,
  "message": "No questions in selected page.",
  "success": false
}

```
# <a name="post_categories"></a>
### 7. POST /categories

```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "type" : "Udacity"}' -H 'Content-Type: application/json'
```

- Request Arguments: **None**
- Request Headers : (_application/json_) 
   1. **string** type
- Returns: 
  1. `categories`:
      - **integer** `id` 
      - **string** `type`
  2. **integer** `total_categories` - `categories` count
  3. **integer** `created` inserted `category` id
  4. **boolean** `success`

Output: 
#### Example response
```js
{
  "categories": [
    {
      "id": 1,
      "type": "Category 1"
    },
    {
      "id": 2,
      "type": "Category 2"
    },
    {
      "id": 3,
      "type": "Category 3"
    },
    {
      "id": 4,
      "type": "Category 4"
    },
    {
      "id": 5,
      "type": "Category 5"
    },
    {
      "id": 6,
      "type": "Category 6"
    },
    {
      "id": 7,
      "type": "Category 7"
    }
  ],
  "created": 7,
  "success": true,
  "total_categories": 7
}
```


#### Errors

```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "name" : "Udacity"}' -H 'Content-Type: application/json'
```

Output:
```js
{
  "error": 400,
  "message": "no type for new category provided.",
  "success": false
}
```
# <a name="delete_categories"></a>
### 8. DELETE /categories/<category_id>

```bash
curl -X DELETE http://127.0.0.1:5000/categories/8
```
- Request Arguments: 
  - **integer** `category_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` deleted `category` id
    - **boolean** `success`

Output: 
#### Example response
```js
{
  "deleted": 8,
  "success": true
}
```

### Errors

```bash
curl -X DELETE http://127.0.0.1:5000/categories/1234567890
```

Output:
```js
{
  "error": 400,
  "message": "Category with id 1234567890 does not exist.",
  "success": false
}
```
