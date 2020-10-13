import flask
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
# session = Session()

app = flask.Flask(__name__)
app.config['DEBUG'] = True

Base = declarative_base()


@app.route('/get')
def index():
    return flask.json.dumps({'success': True})


@app.route('/users')
def get_all_users():
    session = Session()
    data = session.query(User).all()
    session.close()
    return data


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
