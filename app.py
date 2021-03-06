import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Movies, Actor, setup_db
import sys
from auth.auth import AuthError, requires_auth

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'fsnd-nes.us.auth0.com')
ALGORITHMS = os.environ.get("JWT_TOKEN_ENCRYPTION_ALGORITHMS", ['RS256'])
API_AUDIENCE = os.environ('AUTH0_JWT_API_AUDIENCE', 'casting-agency-api')
CLIENT_ID = os.environ('AUTH0_CLIENT_ID', 'JGmjaRutW3eW63rA0wbPCDUoon5sJX72')
CALLBACK_URL = os.environ('CALLBACK_URL', "http://localhost:5000/")


def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        """
         generate auth url to get tokens for each user
        """
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{CLIENT_ID}&redirect_uri=' \
            f'{CALLBACK_URL}'

        return jsonify({
            'url': url
        })

    # CORS Headers
    @app.after_request
    def after_request(response):

        # Allow requests headers ( Content-Type, Authorization)
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        # Allow specific requests methods (GET, POST, PATCH, DELETE, OPTIONS)
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def welcome():
        return 'Welcome to the Casting Agency app'

    @app.route('/movies')
    def get_movies():
        """
        GET /movies
        returns status code 200 and json {"success": True, "movie": movies}
        where movies is the list of movies
        or appropriate status code indicating reason for failure
        """
        try:
            movies = list(map(Movies.short, Movies.query.all()))
            return jsonify({
                'success': True,
                'movie': movies,
            }), 200

        except Exception:
            print(sys.exc_info())
            abort(500)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        """
            POST /movies
            it should create a new row in the movies table
            it should require the 'post:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies":
        movie} where
        drink an array containing only the newly created
         drink or appropriate status code indicating reason for failure
        """
        try:
            data = request.get_json()
            movie = Movies(title=data.get('title', None),
                           duration=data.get('duration', None),
                           release_year=data.get('release_year', None))
            movie.insert()
            movies = list(map(Movies.long, Movies.query.all()))
            return jsonify({
                'success': True,
                'movie': movies,

            }), 200
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth("get:movies-id")
    def get_movie_by_id(jwt, movie_id):
        """
        GET /movies/<int:movie_id>
        get the movie by id
        """
        try:
            movie = Movies.query.filter_by(id=movie_id).one_or_none()
            if not movie:
                abort(404)
            return jsonify({
                "success": True,
                "movie": movie.long()
            }), 200
        except Exception:
            print(sys.exc_info())
            abort(404)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movie_by_id(jwt, movie_id):
        """
        PATCH /movies/<int:movie_id>
        to update the movie by id
        """

        data = request.get_json()
        movie = Movies.query.filter_by(id=movie_id).one_or_none()
        if not movie:
            abort(404)
        if not data:
            abort(422)
        # check if none of the fields is there to raise an error
        if not any(item in data.keys() for item in
                   ['title',
                    'release_year', 'duration']):
            abort(400)
        try:
            if data.get('title', None):
                movie.title = data['title']
            if data.get('duration', None):
                movie.duration = data['duration']
            if data.get('release_year', None):
                movie.release_year = data['release_year']
            movie.update()
            return jsonify({
                "success": True,
                "movie": movie.long()
            }), 200
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        """
        DELETE /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "delete": id}
         where id is the id of the deleted record
            or appropriate status code indicating reason for failure
        """
        movie = Movies.query.filter_by(id=movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id,
            })
        except Exception:
            abort(422)

    @app.route('/actors')
    def get_actors():
        """
        GET /actors
        returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors
        or appropriate status code indicating reason for failure
        """
        try:
            actors = list(map(Actor.long, Actor.query.all()))
            return jsonify({
                'success': True,
                'actor': actors,
            }), 200

        except Exception:
            print(sys.exc_info())
            abort(500)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        """
            POST /actors
            it should create a new row in the actors table
            it should require the 'post:actors' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actor":
         actor} where
        actor an array containing only the newly created
         actor or appropriate status code indicating reason for failure
        """
        try:
            data = request.get_json()

            actor = Actor(name=data.get('name', None),
                          gender=data.get('gender', None),
                          date_of_birth=data.get('date_of_birth', None))
            actor.insert()
            actors = list(map(Actor.long, Actor.query.all()))
            return jsonify({
                'success': True,
                'actor': actors,

            }), 200
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth("get:actors-id")
    def get_actor_by_id(jwt, actor_id):
        """
        GET /actors/<int:actor_id>
        get the actors by id
        """
        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if not actor:
                abort(404)
            return jsonify({
                "success": True,
                "actor": actor.long()
            }), 200
        except Exception:
            print(sys.exc_info())
            abort(404)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actor_by_id(jwt, actor_id):
        """
        PATCH /actors/<int:actor_id>
        to update the movie by id
        """
        data = request.get_json()
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if not actor:
            abort(404)
        # check if none of the fields is there to raise an error
        if not any(item in data.keys() for item in
                   ['name',
                    'gender', 'date_of_birth']):
            abort(400)
        try:
            if data.get('name', None):
                actor.name = data['name']
            if data.get('gender', None):
                actor.gender = data['gender']
            # todo: reading these fields in correct format
            if data.get('date_of_birth', None):
                actor.date_of_birth = data['date_of_birth']
            actor.update()
            return jsonify({
                "success": True,
                "actor": actor.long()
            }), 200
        except Exception:
            print(sys.exc_info())
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        """
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id}
         where id is the id of the deleted record
            or appropriate status code indicating reason for failure
        """
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id,
            })
        except Exception:
            abort(422)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['code']
        }), error.status_code
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
