from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    logged_in = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "logged_in": self.logged_in,
            "id": self.id
        }
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.todo_item

    def serialize(self):
        return {
            "todo_item": self.todo_item,
            "id": self.id
        }
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testStatus = db.Column(db.Boolean(), default=False)
    name = db.Column(db.String(10))

    def __repr__(self):
        return '<Test %r>' % self.testStatus

    def serialize(self):
        return {
            "testStatus": self.testStatus,
            "name": self.name,
            "id": self.id
        }