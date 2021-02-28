# Casting agency

## Introduction
Full stack Nanodegree Capstone project



## Overview

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
  * Casting Assistant: Can view actors and movies
* Casting Director:
  * All permissions  a Casting Assistant has and…
  * Add or delete an actor from the database
  * Modify actors or movies
* Executive Producer
  * All permissions a Casting Director has and…
  * Add or delete a movie from the database


## Development Setup

## API Endpoints Documentation
### GET '/movies'
