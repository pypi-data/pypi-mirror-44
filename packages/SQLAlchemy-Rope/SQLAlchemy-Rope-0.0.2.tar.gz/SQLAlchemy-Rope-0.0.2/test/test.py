import flask


from sqlalchemy import String, Integer, Column, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_rope import SessionJenny

import os

app = flask.Flask(__name__)

Base = declarative_base()
url = "sqlite:///data.db"

if os.path.exists("data.db"):
    os.remove("data.db")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = relationship("Name", backref="users", lazy="dynamic")


class Name(Base):
    __tablename__ = "name"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", uselist=False)


engine = create_engine(url, echo=False)
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)
jenny = SessionJenny(SessionMaker)


user = User()
name = Name(user=user)

jenny.session.add_all([user, name])
jenny.session.commit()

jenny.remove()


@app.route("/")
def some_func():
    user = jenny.session.query(User).first()
    return flask.render_template("index.html", user=user)


app.run()

"""
SELECT name.id AS name_id, name.user_id AS name_user_id 
FROM name 
WHERE ? = name.user_id
"""
