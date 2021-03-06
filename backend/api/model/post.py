'''
Contains example usage in the form of code. Has a required relationship with one user, one call, and one API.
Optional fields include: API version string, scope. TODO: a list of tags.
Required 
'''

from .base import Base
from flask import Flask, request, jsonify, abort
from database import db

class Post(Base):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # TODO: require authentication
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    call_id = db.Column(db.Integer, db.ForeignKey('calls.id'), nullable=False)

    #link to the many to one relationship from call
    call = db.relationship('Call', back_populates="posts")


    scope = db.Column(db.String(100))
    # TODO: tags (could encompass semantic version?)
    # TODO: link to repository?

    def __repr__(self):
        return '<Post %r>' % self.title