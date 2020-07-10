
import json
import dateutil.parser
import babel
import sys
from datetime import datetime, date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler

database_name = "capstone"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#Relationships - locales can have many venues and many artists
class Movie(db.Model):
  __tablename__ = 'movies'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.DateTime)
  actors = db.relationship('Actor', backref='movies', lazy=True)

  def __repr__(self):
        return f'Movie {self.id} {self.title}'

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release.date
    }

# Relationships - Venue has one locale, many artists and many shows. 
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    movies = db.relationship('Movie', backref='actors', lazy=True)

    def __repr__(self):
        return f'Actor {self.id} {self.name}'

    def __init__(self, title, release_date):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender' : self.gender
        }



