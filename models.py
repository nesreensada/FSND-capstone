
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
    cast = db.relationship('Cast', backref='movies', lazy='dynamic')

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
            'title': self.title,
            'cast': list(map(lambda actor: actor.name, self.cast))
        }

    def __repr__(self):
        return f'<Movie {self.title} {self.duration} {self.release_year} >'


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
    cast = db.relationship('cast', backref='actors', lazy='dynamic')

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

    def details(self):
        return {
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
            "gender": self.gender,
            "movies": [movie.title for movie in self.movies]
        }

    def __repr__(self):
        return f'<Actor {self.name} {self.date_of_birth} {self.gender} >'


class Cast(db.Model):
    __tablename__ = 'cast'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(Integer, db.ForeignKey('actors.id'))
    movie_id = db.Column(Integer, db.ForeignKey('movies.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

    def details(self):
        return {
            'id': self.id,
            'actor_id': self.actor_id,
            'movie_id': self.movie_id
        }

    def show_movie(self):
        return {
            'id': self.movie_id,
        }
