from sqlalchemy import Integer, ForeignKey

from app import db
# from models/friend.py import Friend

class Present(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=False, nullable=False)
    returned = db.Column(db.Boolean, unique=False, nullable=False)
    _from = db.Column(Integer, ForeignKey('friend.friend_id', ondelete='CASCADE'), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % ''.join([self.name, self.surname])
