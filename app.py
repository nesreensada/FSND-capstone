import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movies, Actor, Cast, setup_db
import sys
from auth import AuthError


def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def welcome():
        return 'Welcome to the Casting Agency app'

    @app.route('/movies')
    def get_movies():
        """
        GET /movies
        returns status code 200 and json {"success": True, "movies": movies} where
        movies is the list of movies
        or appropriate status code indicating reason for failure
        """
        try:
            movies = list(map(Movies.short, Movies.query.all()))
            return jsonify({
                'success': True,
                'movies': movies,
            }), 200

        except Exception:
            print(sys.exc_info())
            abort(500)

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


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
