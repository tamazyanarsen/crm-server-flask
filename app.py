import flask
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

app = flask.Flask(__name__)
app.config['DEBUG'] = True

Base = declarative_base()


@app.route('/get')
def index():
    return flask.json.dumps({'success': True})


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
