# Casting agency
Full stack Nanodegree Capstone project.

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

Casting Assistant Token:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJIV3c4ODhQUGdaWnk3a2F2VjI0TCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDNkMDQxODRiNDk3OTAwNjkyNjM4OTQiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE2MTQ2MTY0MDUsImV4cCI6MTYxNDcwMjgwNSwiYXpwIjoiSkdtamFSdXRXM2VXNjNyQTB3YlBDRFVvb241c0pYNzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMtaWQiLCJnZXQ6bW92aWVzLWlkIl19.d4ZUGsll-owe3Iv9MZAce_gCT0eVZjYwEky19uOegSqT_jvO1AcVYo7JiatvBpmczBvUBfmD_4MsCeElSFqC3Xk114FJMmv02UBtNjaeA2SJTOIv593GmFMCaCA9LaZAEEHOAL2XJhIQors2bp0DLE953jnQedXck4SJWkn_3MeAcxoyQ1CR3-RZOpqQj62vfv-k4r39XD0FjI_Smq3I3eRJSe1f2UU4Kx9pJW4J_UoKGbJ-OuCkEyrzsaXN4LSQvVsJEApnfr5JqIQESCTgynJNsKy2Mkev8HK5OaumSJY5DSO-Jiq59Ogi-Qj3FrxE1DMVWBtZQIeCarB0LqyBjw
```

casting director token:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJIV3c4ODhQUGdaWnk3a2F2VjI0TCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbmVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDNkMDQ0Mzg3NTZkZjAwNjlhNDk5MTUiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE2MTQ2MTc0MjMsImV4cCI6MTYxNDcwMzgyMywiYXpwIjoiSkdtamFSdXRXM2VXNjNyQTB3YlBDRFVvb241c0pYNzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzLWlkIiwiZ2V0Om1vdmllcy1pZCIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.Jv6-QFEhzBZCAPJpMMWhXtdu8daWocBFGRza9gDa6uiq8B8eft47lKZvZaM_MKHBMHH2aM1jOBPj6Yn5XT1xkC31gWbMhDiilgPa6j-aCfnrOJNGK43atePv8QgbgONv2Oz5ksBgaYuTqA348RZu36YesHS8Gs4mIq4wfHAuZlnLBr2a2mN2ecotT0L4okMrplMN4rlvbMD4buJj9E0KU1n_2hIe35kwjQx2AikocpKqZYyEuIm7BKpEFgRoz8VB2bpkZfHnI13T-afmJjFxG3hpOdTnxK8GWN4lk26s9I_KHIJBqJobb2S7WC4E1iQDCsmp1lFEPkiBftJM0k6gzA
```

## API Endpoints Documentation
### GET '/movies'



## Tests
