import json
from flask import Flask, request, Response, flash, abort, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from datetime import datetime, date
from dateutil.parser import parse
from logging import Formatter, FileHandler
from database.models import setup_db, Movie, Actor
from config.config import TestingConfig, LocalConfig, HerokuConfig
from authorization.auth import AuthError, requires_auth

# -------------------------------------------------------------------------------
# SETUP
# -------------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(HerokuConfig)
db = setup_db(app)

CORS(app, resources={r"*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, POST, PATCH, DELETE, OPTIONS'
    )
    return response

# --------------------------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------------------------

# GET

@app.route('/login')
def login():
    return 'Success'

@app.route('/actors')
@requires_auth(permission='get:actors')
def get_actors(payload):
    actors = Actor.query.order_by('id').all()
    if actors is None:
        abort(404)
    else:
        mapped_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': mapped_actors
        })


@app.route('/movies')
@requires_auth(permission='get:movies')
def get_movies(payload):
    movies = Movie.query.order_by('id').all()
    if movies is None:
        abort(404)
    else:
        mapped_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': mapped_movies
        })

# POST


@app.route('/actors', methods=['POST'])
@requires_auth(permission='post:actors')
def add_actor(payload):
    # Extract relevant details from request.
    req_data = request.get_json()
    name = req_data['name']
    age = req_data['age']
    gender = req_data['gender']

    # Check if age is integer
    if type(age) is int:
        pass
    else:
        abort(422)
    # Create new
    newActor = Actor(
        name=name,
        age=age,
        gender=gender
    )
    
    # Save
    try:
        newActor.insert()
    except:
        abort(500)
    finally:
        # Return
        actor = newActor.format()

        return jsonify({
            'success': True,
            'actors': actor
        })


@app.route('/movies', methods=['POST'])
@requires_auth(permission='post:movies')
def add_movie(payload):
    # Extract relevant details from request.
    req_data = request.get_json()
    title = req_data['title']
    release_date = req_data['release_date']
    check_movie_values(title, release_date)
    
    # Create new
    new_movie = Movie(
        title=title,
        release_date=release_date,
    )
    # Save
    try:
        new_movie.insert()
    except:
        abort(500)
    finally:
        # Return
        movie = new_movie.format()

        return jsonify({
            'success': True,
            'movie': movie
        })

# PATCH


@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth(permission='patch:actors')
def update_actor(payload, id):
    # Search by id
    actor = Actor.query.get(id)
    if actor is None:
        abort(404)
    # Extract new data from request
    req_data = request.get_json()
    name = req_data['name']
    age = req_data['age']
    gender = req_data['gender']

    if type(age) is int:
        pass
    else:
        abort(422)

    # Update data
    actor.name = name
    actor.age = age
    actor.gender = gender

    # Save
    try:
        actor.update()
    except:
        abort(500)
    finally:
        # Return

        return jsonify({
            'success': True,
            'actors': actor.format()
        })


@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth(permission='patch:movies')
def update_movie(payload, id):
    # Search by id
    movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    # Extract new data from request
    req_data = request.get_json()
    title = req_data['title']
    release_date = req_data['release_date']
    check_movie_values(title, release_date)

    # Update data
    movie.title = title
    movie.release_date = release_date

    # Save
    try:
        movie.update()
    except:
        abort(500)
    finally:
        # Return

        return jsonify({
            'success': True,
            'movies': movie.format()
        })

# DELETE


@app.route('/actors/<id>', methods=['DELETE'])
@requires_auth(permission='delete:actors')
def delete_actor(payload, id):
    # Search for actor to be deleted
    actor = Actor.query.get(id)
    if actor is None:
        abort(404)
    # Delete actor
    try:
        actor.delete()
    except:
        abort(500)
    finally:
        # Return actor
        return jsonify({
            'success': True,
            'delete': actor.id
        })


@app.route('/movies/<id>', methods=['DELETE'])
@requires_auth(permission='delete:movies')
def delete_movie(payload, id):
    # Search for movie to be deleted
    movie = Movie.query.get(id)
    if movie is None:
        abort(404)
    # Delete movie
    try:
        movie.delete()
    except:
        abort(500)
    finally:
        # Return movie
        return jsonify({
            'success': True,
            'delete': movie.id
        })
# # Error Handling


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
      }), 404


@app.errorhandler(422)
def unprocessable_error(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
        }), 422


@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": get_error_message(AuthError.error, "authentification fails")
    }), 401


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server Error"
    }), 500

# Helper

def check_movie_values(title, release_date):
    #check if title is string
    if isinstance(title, str):
        pass
    else:
        abort(422)

    #check if release_date can be parsed to datetime
    if is_date(release_date):
        pass
    else:
        abort(422)

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def get_error_message(error, message):
    description = error['description']
    return message + " - " + description
