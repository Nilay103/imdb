import json
import unittest

from app import app
from database import mongo


class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = mongo


class SignupTest(TestClass):
    def test_successfully_singup(self):
        payload = json.dumps({
            "name": "nilayy_user5",
            "email": "xy1z@gmail.com",
            "pwd": "1234"})

        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(201, response.status_code)

    def test_precondition_failed_no_username(self):
        payload = json.dumps({
            "name": "",
            "email": "xyz@gmail.com",
            "pwd": "1234"})

        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(412, response.status_code)

    def test_precondition_failed_no_password(self):
        payload = json.dumps({
            "name": "nilay 101",
            "email": "xyz@gmail.com",
            "pwd": ""})

        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(412, response.status_code)

    def test_precondition_failed_no_email(self):
        payload = json.dumps({
            "name": "nilay 101",
            "email": "",
            "pwd": "1234"})

        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(412, response.status_code)

    def test_failed_user_already_existed(self):
        payload = json.dumps({
            "name": "nilay 101",
            "email": "xyz@gmail.com",
            "pwd": "1234"})

        response = self.app.post('/signup', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(412, response.status_code)


class LoginTest(TestClass):
    def test_successfully_login(self):
        payload = json.dumps({
            "name": "nilay 101",
            "email": "xyz@gmail.com",
            "pwd": "1234"})

        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(201, response.status_code)

    def test_failed_login_invalid_user(self):
        payload = json.dumps({
            "name": "nilay 101",
            "email": "invaliduser@gmail.com",
            "pwd": "1234"})

        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(412, response.status_code)


class MoviesTest(TestClass):
    def test_successfully_get_all_movies(self):
        response = self.app.get('/api/movies/')

        self.assertEqual(201, response.status_code)

    def test_failed_precondition_authentication(self):
        payload = json.dumps({
            "99popularity": 87,
            "_id": "xxxxxxyyyyyy",
            "director": "Andy Wachowski",
            "genre": [
                "Action",
                " Adventure",
                " Sci-Fi"
            ],
            "imdb_score": 8.7,
            "name": "The Matrix 3"
        })

        response = self.app.post('/api/movies/', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(412, response.status_code)
