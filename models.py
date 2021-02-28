
from sqlalchemy import Column, String, Date, Integer
from flask_sqlalchemy import SQLAlchemy
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movies(db.Model):
    '''
    Movies
    Have title and release year
    '''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    release_year = db.Column(Integer, nullable=False)
    duration = db.Column(Integer, nullable=False)
    title = Column(String(180), nullable=False, unique=True)

    def __init__(self, title, release_year, duration):
        self.title = title
        self.release_year = release_year
        self.duration = duration

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'release_year': self.release_year,
            'title': self.title
        }

    def long(self):
        return {
            'id': self.id,
            'release_year': self.release_year,
            'duration': self.duration,
            'title': self.title
        }

    def __repr__(self):
        return f'<Movie {self.title} {self.duration} {self.release_year} >'

    def row2dict(row):
        return dict((col, getattr(row, col))
                    for col in row.__table__.columns.keys())


class Actor(db.Model):
    '''
    Actor
    Have name and dob
    '''
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    gender = Column(String(), nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def __init__(self, name, gender, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "name": self.name,
            "gender": self.gender
        }

    def long(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
            "gender": self.gender
        }

    def __repr__(self):
        return f'<Actor {self.name} {self.date_of_birth} {self.gender} >'

    def row2dict(row):
        return dict((col, getattr(row, col))
                    for col in row.__table__.columns.keys())
