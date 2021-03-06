# Casting agency

## Motivation
This project was developed to showcase the skills acquired for fullstack Nanodegree and it is Capstone project.


## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Overview

An api allowing:

1. creating movies and managing and assigning actors to those movies.

## Tech Stack (Dependencies)

Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install
```
## Main Files: Project Structure

── app.py  *** the main driver of the app. Includes your SQLAlchemy models.
├── auth *** responsible to validating user tokens
│   ├── auth.py
├── config.py  *** Database URLs, CSRF generation, etc
├── env
├── LICENSE
├── manage.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── models.py
├── Procfile
├── README.md
├── requirements.txt  *** The dependencies we need to install with "pip3 install -r requirements.txt"
├── setup.sh
└── test_app.py


Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* auth functions are located in auth.py
* manage.py can be used to create and run migrations


### Roles:
  * Public: access the movies and actors
  * Casting Assistant: Can view actors and movies
  * Casting Director:
    * All permissions a Casting Assistant has
    * Add or delete an actor from the database
    * Modify actors or movies
  * Executive Producer
    * All permissions a Casting Director has
    * Add or delete a movie from the database


## Development Setup


## Authentication

Each endpoint is access controlled using Auth0's Role Based Access Control (RBAC), with the exception of one publicly accessible endpoint.

Url for authorization:
```
https://fsnd-nes.us.auth0.com/login?state=g6Fo2SBidmZUeER4MWdxWFFPLVBJRjVlNVhjclJBU2ljeFRzZ6N0aWTZIHQzTHVHZFY3N2Y3R2JBeE53bmNpei1FbGFYcmV3NjZmo2NpZNkgSkdtamFSdXRXM2VXNjNyQTB3YlBDRFVvb241c0pYNzI&client=JGmjaRutW3eW63rA0wbPCDUoon5sJX72&protocol=oauth2&audience=casting-agency-api&response_type=token&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F
```

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Run Migrations
```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ python manage.py db init
  $ python manage.py db migrate
  $ python manage.py db upgrade
  ```
### Making API calls
   To start making API calls with sample tokens

1. Get authorization url
  ```http://localhost:5000/authorization/url
  ```
  Paster the url in the browser and follow the instructions below
2. Get token
    Casting Assistant
      * username castingassistant@gmail.com
      * password MOVIEcasting123
    Casting Director
      * username castingdirector@gmail.com
      * password MOVIEcasting123
    Executive Producer
       * username executiveproducer@gmail.com
       * password MOVIEcasting123
3. Get the token from the browser redirect after logging in with one of these users
   This depends on the action you want to perform
4. Use postman or any package to make a request with bearer authorization header

## Running Tests
Tests currently use a sample Casting Director token that has all roles access
  1. get the token from the authorization url and update the test_app.py before running the code
  2. ensure to run the app to post movie and actor
  2. python test_app.py

## Testing the live app
   1. production url
    ```http://localhost:5000/authorization/url
    ```
   2. Test instructions
      Test your endpoints with [Postman](https://getpostman.com).
      - get an authorization url **https://heroku-casting-agency-nes.herokuapp.com/**
      - login with one of the users specified in **2. Get token**
      - use the token above to test the endpoints (take note of user permissions as listed above)

## Endpoints
## Movies

### `GET /movies`

##### `Public`

- Fetches all the movies from the database
- Request arguments: None
- Returns: A list of movies contain key:value pairs of id, title and release_date

#### `Response`

```
{
  "success": true,
  "movie": [ {
    "id" : 1,
    "title": "Star Wars",
    "duration": 120,
    "release_year": "1971"
  }, {
    "id" : 2,
    "title": "Star Wars",
    "duration": 120,
    "release_year": "1971"
  }]
}
```

### `POST /movies`

##### `Executive Producer`

- Creates a movie from the request's body
- Request arguments: None
- Returns: the created movie contains key:value pairs of id, title and release_date

#### `Body`

```
{
  "title": "Star Wars",
  "duration": 120,
  "release_year": "1971"
}
```

#### `Response`

```
{
  "success": true,
  "movie": [{
    "title": "Star Wars",
    "duration": 120,
    "release_year": "1971"
  }]
}
```

### `PATCH /movies/<int:id>`

##### `Casting Director or Executive Producer`

- Updates a movie using the information provided by request's body
- Request arguments: Movie id
- Returns: the updated movie contains key:value pairs of id, title and release_date

#### `Body`

```
{

  "duration": 150
}
```

#### `Response`

```
{
  "success": true,
  "movie": [{
    "title": "Star Wars",
    "duration": 150,
    "release_year": "1971"
  }]
}
```

### `DELETE /movies/<int:id>`

##### `Executive Producer`

- Deletes a movie based the request argument
- Request arguments: Movie id
- Returns: the deleted movie id

#### `Response`

```
{
  "success": true,
  "deleted": 1
}
```

## Actors

### `GET /actors`

##### `Public`

- Fetches all the actors from the database
- Request arguments: None
- Returns: A list of actors contain key:value pairs of id, name, age and gender

#### `Response`

```
{
  "success": true,
  "actor": [
    {
      "id": 1,
      "name": "James",
      "date_of_birth": "1950-03-1",
      "gender": "M"
    },
    {
       "id" : 2
       "name": "Nicholas",
       "date_of_birth": "1950-03-1",
       "gender": "M"
    }
  ]
}
```

### `POST /actors`

##### `Casting Director or Executive Producer`

- Creates an actor from the request's body
- Request arguments: None
- Returns: the created actor contains key:value pairs of id, name, age and gender

#### `Body`

```
{
   "name": "Nicholas",
   "date_of_birth": "1950-03-1",
   "gender": "M"
}
```

#### `Response`

```
{
  "success": true,
  "actor": [{
     "id": 1,
     "name": "Nicholas",
     "date_of_birth": "1950-03-9",
     "gender": "M"
  }]
}
```

### `PATCH /actors/<int:id>`

##### `Casting Director or Executive Producer`

- Updates a actor using the information provided by request's body
- Request arguments: Actor id
- Returns: the updated actor contains key:value pairs of id, name, age and gender

#### `Body`

```
{
   "date_of_birth": "1950-03-1"
}
```

#### `Response`

```
{
  "success": true,
  "actor": [{
     "id": 1,
     "name": "Nicholas",
     "date_of_birth": "1950-03-9",
     "gender": "M"
  }]
}
```

### `DELETE /actors/<int:id>`

##### `Casting Director or Executive Producer`

- Deletes an actor based the request argument
- Request arguments: Actor id
- Returns: the deleted actor id

#### `Response`

```
{
  "success": true,
  "deleted": 1
}
```

## Status Codes

- `200` : Request has been fulfilled
- `201` : Entity has been created
- `401` : Unauthorized
- `404` : Resource not found
- `422` : Wrong info provided
- `500` : Internal Server Error
