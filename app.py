import json
from flask import Flask, request, Response, flash, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from database.models import setup_db, Movie, Actor
from authorization.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
db = SQLAlchemy()
migrate = Migrate(app, db)
CORS(app, resources={r"*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

# ROUTES
@app.route('/drinks')
def get_drinks():
    return "Hello"
#     drinks = Drink.query.order_by('title').all()
#     if drinks is None:
#         abort(404)
#     else:
#         mapped_drinks = [drink.short() for drink in drinks]
#         return jsonify({
#             'success': True,
#             'drinks': mapped_drinks
#         })


# @app.route('/drinks-detail')
# @requires_auth(permission='get:drinks-detail')
# def get_drink_detail(payload):
#     drinks = Drink.query.order_by('title').all()
#     if drinks is None:
#         abort(404)
#     else:
#         mapped_drinks = [drink.long() for drink in drinks]
#     return jsonify({
#         'success': True,
#         'drinks': mapped_drinks
#     })


# @app.route('/drinks', methods=['POST'])
# @requires_auth(permission='post:drinks')
# def add_drink(payload):
#     # Extract relevant drink details from request.
#     req_data = request.get_json()
#     title = req_data['title']
#     recipe = req_data['recipe']
#     # Postman request format doesn't match frontend format
#     if type(recipe) is dict:
#         recipe = [recipe]
#     # Create new drink object
#     newDrink = Drink(
#         title=title,
#         recipe=json.dumps(recipe)
#     )
#     # Save Drink
#     try:
#         newDrink.insert()
#     except:
#         abort(500)
#     finally:
#         # Return drink
#         drink = newDrink.short()

#         return jsonify({
#             'success': True,
#             'drinks': drink
#         })


# @app.route('/drinks/<id>', methods=['PATCH'])
# @requires_auth(permission='patch:drinks')
# def update_drink(payload, id):
#     # Search for drink by id
#     drink = Drink.query.get(id)
#     if drink is None:
#         abort(404)
#     # Extract new data from request
#     req_data = request.get_json()
#     # Update data in drink
#     title = req_data['title']
#     drink.title = title
#     if 'recipe' in req_data:
#         recipe = req_data['recipe']
#         drink.recipe = json.dumps(recipe)
#     # Save Drink
#     try:
#         drink.update()
#     except:
#         abort(500)
#     finally:
#         # Return drink

#         return jsonify({
#             'success': True,
#             'drinks': [drink.short()]
#         })


# @app.route('/drinks/<id>', methods=['DELETE'])
# @requires_auth(permission='delete:drinks')
# def delete_drink(payload, id):
#     # Search for drink to be deleted
#     drink = Drink.query.get(id)
#     if drink is None:
#         abort(404)
#     # Delete drink
#     try:
#         drink.delete()
#     except:
#         abort(500)
#     finally:
#         # Return Drink
#         return jsonify({
#             'success': True,
#             'delete': drink.id
#         })


# # Error Handling
# @app.errorhandler(404)
# def not_found_error(error):
#     return jsonify({
#         "success": False,
#         "error": 404,
#         "message": "Not Found"
#       }), 404


# @app.errorhandler(422)
# def unprocessable_error(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "Unprocessable"
#         }), 422


# @app.errorhandler(AuthError)
# def authentification_failed(AuthError):
#     return jsonify({
#         "success": False,
#         "error": AuthError.status_code,
#         "message": get_error_message(AuthError.error, "authentification fails")
#     }), 401


# @app.errorhandler(500)
# def server_error(error):
#     return jsonify({
#         "success": False,
#         "error": 500,
#         "message": "Server Error"
#     }), 500


# # Helper
# def get_error_message(error, message):
#     description = error['description']
#     return message + " - " + description