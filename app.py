import uuid

import flask
from flask import request, jsonify
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import flask_bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import datetime

# datetime.datetime.now().timestamp() текущая дата через float

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = str(datetime.datetime.now().timestamp())

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String, nullable=True)
    fullname = db.Column(db.String, nullable=True)
    nickname = db.Column(db.String, nullable=True)

    def __init__(self, email, password, name=None, fullname=None, nickname=None):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = str(bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()))
        self.name = name
        self.fullname = fullname
        self.nickname = nickname

    def __repr__(self):
        return "<User(email=%s, name='%s', fullname='%s', nickname='%s')>" % (
            self.email, self.name, self.fullname, self.nickname)


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.String, primary_key=True)
    token = db.Column(db.String)
    created_at = db.Column(db.String)
    token_live = db.Column(db.String)  # время жизни токена задаем в минутах

    def __init__(self, token):
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return f'token=${self.token}'


db.create_all()


@app.route('/')
def index():
    return jsonify({'success': True})


@app.route('/users/login', methods=['POST'])
def login():
    print(request, request.json)  # работает, если в Content-Type передавать application/json
    email = request.form['email']
    password = request.form['password']
    print(bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()))
    user = User.query.filter(User.email == email).filter(
        bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()) == User.password).first()
    if user:
        access_token = create_access_token(identity=user.id)
        answer = jsonify(access_token=access_token), 200
    else:
        answer = jsonify({'error': True, 'code': 400}), 400
    return answer


@app.route('/users/<user_id>')
def read_user(user_id):
    return jsonify(User.query.filter(User.id == user_id))


@app.route('/users', methods=['POST'])
def create():
    email = request.form['email']
    password = request.form['password']
    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    answer = jsonify(access_token=create_access_token(identity=user.id)), 200
    return answer


@app.route('/users')
def get_all_users():
    data = list(map(repr, User.query.all()))
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
