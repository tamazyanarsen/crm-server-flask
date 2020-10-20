import uuid

import flask
from flask import request, jsonify
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import flask_bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, create_refresh_token, \
    jwt_refresh_token_required, set_access_cookies, unset_jwt_cookies, jwt_required, set_refresh_cookies
from flask_sqlalchemy import SQLAlchemy
import datetime

# datetime.datetime.now().timestamp() текущая дата через float

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = str(datetime.datetime.now().timestamp())
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True

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
        return f'User (email={self.email}, password={self.password})'


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
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
    user = User.query.filter(User.email == email).filter(User.email == email).first()
    print(f'user: {user}')
    if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        # Set the JWTs and the CSRF double submit protection cookies
        # in this response
        resp = jsonify({'login': True}), 200
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
    else:
        resp = jsonify({'login': False}), 400
    return resp


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
    answer = jsonify(access_token=create_access_token(identity=user.email)), 200
    return answer


@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@app.route('/api/example', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(username)}), 200


@app.route('/users')
def get_all_users():
    data = list(map(repr, User.query.all()))
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
