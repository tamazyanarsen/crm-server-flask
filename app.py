import uuid

import flask
from flask import request
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
# session = Session()

app = flask.Flask(__name__)
app.config['DEBUG'] = True

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    nickname = Column(String, nullable=True)

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


Base.metadata.create_all(engine)


@app.route('/')
def index():
    return flask.jsonify({'success': True})


@app.route('/users/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    session = Session()
    user = session.query(User).filter(User.email == login).filter(
        bcrypt.checkpw(password.encode('utf8'), User.password)).first()
    session.close()
    return flask.jsonify(user.id)


@app.route('/users/add', methods=['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    user = User(email, password)
    session = Session()
    session.add(user)
    session.commit()
    session.close()
    return flask.jsonify(repr(user))


@app.route('/users')
def get_all_users():
    session = Session()
    data = list(map(repr, session.query(User).all()))
    print(data)
    session.close()
    return flask.jsonify(data)


app.run()
