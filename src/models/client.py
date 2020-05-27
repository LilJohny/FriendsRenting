from models import db


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(30), unique=False, nullable=False)
    mail = db.Column(db.String(40), unique=True, nullable=False)
    sex = db.Column(db.String(1), unique=False, nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=True)
    birth_date = db.Column(db.Date, unique=False, nullable=True)

    def __repr__(self):
        return '<Client %r>' % ' '.join([self.name, self.surname])
