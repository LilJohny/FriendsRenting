from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.friend_id'), unique=True, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), unique=True, nullable=True)

    @staticmethod
    def check_password(hashed_password, password):
        return hashed_password == password

    def get_id(self):
        return self.user_id
