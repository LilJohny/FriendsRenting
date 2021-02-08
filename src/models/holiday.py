from . import db


class Holiday(db.Model):
    holiday_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, unique=False, nullable=False)
    end_date = db.Column(db.Date, unique=False, nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.friend_id', ondelete='CASCADE'), unique=False, nullable=False)

    def __repr__(self):
        return f'<Holiday of {self.friend_id!r}>'
