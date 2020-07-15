
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
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = postgres://caknuwumdnhotv:f62e05a5f053a9dc285c19d0b1d44c67de283b1d05923b39f41f9607113082f7@ec2-34-197-188-147.compute-1.amazonaws.com:5432/ddebgjg37tjl5j
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
    return db
    # db.create_all()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Link(db.Model):
    __tablename__ = 'link'

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), primary_key=True)


class Movie(db.Model):
  __tablename__ = 'movies'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.DateTime)
  actors = db.relationship('Actor',secondary='link', lazy=True)

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
      'release_date': self.release_date
    }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    movies = db.relationship('Movie', secondary='link', lazy=True)

    def __repr__(self):
        return f'Actor {self.id} {self.name}'

    def __init__(self, name, age, gender):
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

