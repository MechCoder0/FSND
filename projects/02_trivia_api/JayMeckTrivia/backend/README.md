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

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

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

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

All endpoints return Json Objects. 

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/{category_id}/questions
POST '/questions'
POST '/questions/search'
POST '/quizzes'
DELETE '/questions/{question_id}'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
GET '/questions'
 - Fetches a dictionary of questions, paginated to 10 per page. The page returned is based off of the page request argument.  
 - Request Arguments: page - the page of questions. 
 - URL example: /questions?page=1
 - Returns: A list of questions, number of total questions, current category, categories. 
 {
    success: true,
    total_questions: "10",
    questions: [
        {
            id: 3, 
            question:"What is the heaviest organ?",
            answer:"The liver",
            category :1,
            difficulty:1 
        },
        {
            id: 2, 
            question :"What state is Pittsburgh in?",
            answer:"Pennsylvania",
            category :2,
            difficulty':1 },
        }
    ],
    categories: [{'1':"Science", '2':"History"}],
    current_category: 1
}

```
DELETE '/questions/{question_id}
- Deletes the question with the passed id
- Request arguments: none
- Returns the deleted question ID and the amount of 
questions remaining.
{
    success:true,
    deleted:1,
    total_questions:10
}

```
POST '/questions'
- Creates a new question using the json body passed 
  in the request. 
- Request arguments: a JSON object with the question (String), answer (String), 
difficulty (int), and category (int):
{
    question:"What color is the sky",
    answer:"Blue",
    difficulty:1,
    category:2
}
-Returns the id of the created question and the number of total questions.
{
    success: true,
    created: 1,
    total_questions: 10
}

```
POST '/questions/search'
- searches the questions via a passed phrase. Search returns any question whose question contains the the phrase passed. The case of the phrase doesn't matter. 
- Request arguments: A JSON object containing the phrase (String) to search by:
{
    searchTerm: "color"
}
- Returns the questions that match, the total number of questions which have the passed phrase, and the current category, which is based off of the question that best matches the passed phrase:
{
    success :true, 
    questions : [
        {
            id:1,
            question:"What color is the sky",
            answer:"Blue", 
            difficulty:1,
            category:2
        }
    ],
    total_questions: 1,
    current_category: 2
}

```
GET '/categories/{category_id}/questions'
- Gets all the questions of the past caregory.
- Request arguments: the category id
- Returns all the questions of the given category, the total number of questions in the category, and the current category:
{
    success:true,
    questions:[
        {
            id: 1,
            question:"What color is the sky",
            answer:"Blue", 
            difficulty:1,
            category:2
        }
    ],
    total_questions: 1,
    current_category:2
}  

```
POST '/quizzes'
- Get a random question that is not in the list of questions passed. This request can also be limited to a certain category.
- Request arguments: the past questions (array of ints, optional) and a quiz category(int, optional):
{
    previous_questions:[2,3],
    quiz_category: 2
} 
- Returns a random question in the passed category if a category is given. If a category is not given, it returns a random question in a random category. If the passed questions are given in the request, the returned question will not be one of them:
{
    success:true,
    question:{
        id: 1,
        question:"What color is the sky",
        answer:"Blue", 
        difficulty:1,
        category:2
    }
}  


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```