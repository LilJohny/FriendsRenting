from models import db


class Friend(db.Model):
    friend_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(30), unique=False, nullable=False)
    mail = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % ''.join([self.name, self.surname])
