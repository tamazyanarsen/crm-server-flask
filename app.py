import flask
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
# session = Session()

app = flask.Flask(__name__)
app.config['DEBUG'] = True

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    email = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


Base.metadata.create_all(engine)


@app.route('/')
def index():
    return flask.jsonify({'success': True})


@app.route('/users')
def get_all_users():
    session = Session()
    data = session.query(User).all()
    session.close()
    return flask.jsonify(data)


app.run()
