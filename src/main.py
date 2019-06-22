"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity, get_jwt
)

from models import db, Person, Todo, Test

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)


# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    email = params.get('email', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400

    usercheck = Person.query.filter_by(username=username, email=email).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or email"}), 401
    # if username != 'test' or email != 'test':
    #     return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username),'JWT': get_jwt()}
    return jsonify(ret), 200

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/person', methods=['POST', 'GET'])
# @jwt_required
def handle_person():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        user1 = Person(username=body['username'], email=body['email'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':

        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404


@app.route('/person/<int:person_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_person(person_id):
    """
    Single person
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if "username" in body:
            user1.username = body["username"]
        if "email" in body:
            user1.email = body["email"]
        db.session.commit()

        return jsonify(user1.serialize()), 200

    # GET request
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        return "ok", 200

    return "Invalid Method", 404

@app.route('/todo', methods=['POST', 'GET'])
# @jwt_required
def handle_todo():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'todo_item' not in body:
            raise APIException('You need to specify a Todo', status_code=400)


        todo1 = Todo(todo_item=body['todo_item'])
        db.session.add(todo1)
        db.session.commit()
        return jsonify(todo1.serialize()), 200

    # GET request
    if request.method == 'GET':
        all_todos = Todo.query.all()
        all_todos = list(map(lambda x: x.serialize(), all_todos))
        return jsonify(all_todos), 200

    return "Invalid Method", 404

@app.route('/todo/<int:todo_id>', methods=['PUT', 'GET', 'DELETE'])
# @jwt_required
def get_single_todo(todo_id):
    """
    Single Todo
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        todo1 = Todo.query.get(todo_id)
        if todo1 is None:
            raise APIException('Todo not found', status_code=404)

        if "todo_item" in body:
            todo1.todo_item = body["todo_item"]
        db.session.commit()

        return jsonify(todo1.serialize()), 200

    # GET request
    if request.method == 'GET':
        todo1 = Todo.query.get(todo_id)
        if todo1 is None:
            raise APIException('Todo not found', status_code=404)
        return jsonify(todo1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        todo1 = Todo.query.get(todo_id)
        if todo1 is None:
            raise APIException('Todo not found', status_code=404)
        db.session.delete(todo1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404
@app.route('/test/<int:test_id>', methods=['PUT', 'GET', 'DELETE'])
# @jwt_required
def get_single_test(test_id):
    """
    Single Todo
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        test1 = Test.query.get(test_id)
        if test1 is None:
            raise APIException('Test not found', status_code=404)

        if "testStatus" in body:
            test1.testStatus = body["testStatus"]
        if "name" in body:
            test1.name = body["name"]

        db.session.commit()

        return jsonify(test1.serialize()), 200

    # GET request
    if request.method == 'GET':
        test1 = Test.query.get(test_id)
        if test1 is None:
            raise APIException('Test not found', status_code=404)
        return jsonify(test1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        test1 = Test.query.get(test_id)
        if test1 is None:
            raise APIException('Test not found', status_code=404)
        db.session.delete(test1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/test', methods=['POST', 'GET'])
# @jwt_required
def handle_test():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'testStatus' not in body:
        #     raise APIException('You need to specify the test', status_code=400)


        test1 = Test(name=body['name'])
        db.session.add(test1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = Test.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
