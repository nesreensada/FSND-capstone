
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movies, Actor, setup_db

DB_PATH = os.getenv('DATABASE_URL',
                    "postgresql://postgres@localhost:5432/casting_agency")


EXECUTIVE_PRODUCER_TOKEN = os.getgetenv("TOKEN")

headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}


class CastingTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = DB_PATH
        setup_db(self.app, self.database_path)
        self.actor = {
            "name": "Nicholas Cage  gdc",
            "date_of_birth": "1950-03-9",
            "gender": "M"
        }
        self.movie = {
            "title": "Star Wars forever",
            "duration": 120,
            "release_year": "1971"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_authorization_url(self):
        """Test authorization url"""
        res = self.client().get('/authorization/url')
        self.assertEqual(res.status_code, 200)

    def test_401_create_movie_noheader(self):
        """Test get movies without header """
        res = self.client().post('/movies', json=self.movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_200_create_movie_header(self):
        """Test get movies without header """
        res = self.client().post('/movies', json=self.movie, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_200_get_movies_noheader(self):
        """Test get movies without header since it does not require a header"""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_200_get_movies_header(self):
        """Test get movies with header """
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_404_get_movie_id_header(self):
        """Test get movies by ID that is not found """
        res = self.client().get('/movies/290', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_get_movie_id_noheader(self):
        """Test get movies without header """
        movie_id = Movies.query.all()[0].id
        res = self.client().get(f'/movies/{movie_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_200_get_movie_id_header(self):
        """Test get movies by ID not found """
        movie_id = Movies.query.all()[0].id
        res = self.client().get(f'/movies/{movie_id}', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_401_patch_movie_noheader(self):
        """Test patch movies without header """
        movie_id = Movies.query.all()[0].id
        data = {"duration": 150}
        res = self.client().patch(f'/movies/{movie_id}', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_404_patch_movie_header(self):
        """Test patch movies for a non found movie"""
        data = {"duration": 150}
        res = self.client().patch('/movies/290',
                                  json=data, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_200_patch_movie_header(self):
        """Test patch movies for a movie"""
        movie_id = Movies.query.all()[0].id
        data = {"duration": 150}
        res = self.client().patch(f'/movies/{movie_id}',
                                  json=data, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_404_delete_movie_id_header(self):
        """Test get movies by ID that is not found """
        res = self.client().delete('/movies/20', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_delete_movie_id_noheader(self):
        """Test get movies without header """
        movie_id = Movies.query.all()[0].id
        res = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_200_delete_movie_id_header(self):
        """Test get movies by ID not found """
        movie_id = Movies.query.all()[0].id
        res = self.client().delete(f'/movies/{movie_id}', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_create_actors_noheader(self):
        """Test get actors without header """
        res = self.client().post('/actors', json=self.actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_200_create_actor_header(self):
        """Test get actors with header """
        res = self.client().post('/actors', json=self.actor, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_404_get_actor_id_header(self):
        """Test get actors by ID that is not found """
        res = self.client().get('/actors/100', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_get_actor_id_noheader(self):
        """Test get actors without header """
        actor_id = Actor.query.all()[0].id
        res = self.client().get(f'/actors/{actor_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_200_get_actor_id_header(self):
        """Test get actors by ID not found """
        actor_id = Actor.query.all()[0].id
        res = self.client().get(f'/actors/{actor_id}', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_200_get_actors_noheader(self):
        """Test get actors without header since it does not require a header"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_200_get_actors_header(self):
        """Test get actors with header """
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_401_patch_actors_noheader(self):
        """Test patch actors without header """
        actor_id = Actor.query.all()[0].id
        data = {"date_of_birth": "1950-03-1"}
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_404_patch_actors_header(self):
        """Test patch actors for a non found movie"""
        data = {"date_of_birth": "1950-03-1"}
        res = self.client().patch('/actors/100', json=data, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_200_patch_actor_header(self):
        """Test patch actors for a actors"""
        actor_id = Actor.query.all()[0].id
        data = {"date_of_birth": "1950-03-1"}
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=data, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_404_delete_actor_id_header(self):
        """Test get actors by ID that is not found """
        res = self.client().delete('/actors/100', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_delete_actor_id_noheader(self):
        """Test get actors without header """
        actor_id = Actor.query.all()[0].id
        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_200_delete_actor_id_header(self):
        """Test get actors by ID not found """
        actor_id = Actor.query.all()[0].id
        res = self.client().delete(f'/actors/{actor_id}', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
