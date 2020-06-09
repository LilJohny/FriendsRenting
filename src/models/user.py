from flask_login import UserMixin

from models import db
from models.profile import Profile


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.profile_id'), unique=True, nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.friend_id'), unique=True, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), unique=True, nullable=True)

    @staticmethod
    def check_password(hashed_password, password):
        return hashed_password == password

    def get_id(self):
        return self.user_id
