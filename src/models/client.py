from models import db


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.profile_id'), unique=True, nullable=False)

    def __repr__(self):
        return '<Client>'
