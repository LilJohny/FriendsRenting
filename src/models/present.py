from models import db


class Present(db.Model):
    present_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=False, nullable=False)
    _from = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete='CASCADE'), unique=False, nullable=False)
    to = db.Column(db.Integer, db.ForeignKey('friend.friend_id', ondelete='CASCADE'), unique=False, nullable=False)
    returned = db.Column(db.Boolean, default=False, unique=False, nullable=False)

    def __repr__(self):
        return '<Present %r>' % self.title
