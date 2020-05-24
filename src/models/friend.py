from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % ''.join([self.name, self.surname])
