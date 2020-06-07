from models import db
from models.profile import Profile


class Friend(db.Model):
    friend_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.profile_id'), unique=True, nullable=False)

    def __repr__(self):
        return '<Friend>'
