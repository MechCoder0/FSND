import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
def get_body(request):
    body = request.get_json()
    if body is None:
        abort(400)
    return body
'''
    GET /drinks
        it is  a public endpoint
        it contains only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def drinks():
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in Drink.query.all()]
    })


'''
    GET /drinks-detail
        it requires the 'get:drinks-detail' permission
        it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_details():
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in Drink.query.all()]
    })

'''
    POST /drinks
        it creates a new row in the drinks table
        it requires the 'post:drinks' permission
        it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks():
    body = get_body(request)
    try:
        title = body.get('title', None)
        recipe = [json.dumps(body.get('recipe', None))]
    except:
        abort(401)

    try:
        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        print('test')
        new_drink.insert()
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in Drink.query.all()]
        })
    except Exception as e:
        print(e)
        abort(422)

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it responds with a 404 error if <id> is not found
        it updates the corresponding row for <id>
        it requires the 'patch:drinks' permission
        it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    drink = Drink.query.get(id)
    if(drink is None):
        abort(404)
    
    body = get_body(request)
    try:
        title = body.get('title', None)
    except:
        abort(401)
    
    try:
        drink.title = title
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }) 
    except Exception as e:
        print(e)
        abort(422)

'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    drink = Drink.query.get(id)
    if(drink is None):
        abort(404)
    
    try:
        drink.delete()
        return jsonify({
            "success":True,
            "delete":id
        })
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
def handle_error(code, message):
    return jsonify({
      'success':False,
      'error': code,
      'message': message
    }), code

@app.errorhandler(400)
def bad_request(error):
    return handle_error(400, 'Bad request')
  
@app.errorhandler(404)
def not_found(error):
    return handle_error(404, 'Not found')

@app.errorhandler(422)
def unprocessable_entity(error):
    return handle_error(422, 'Unprocessable entity') 

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response