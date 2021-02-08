from . import db


class Complaint(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    friend = db.Column(db.Integer, db.ForeignKey('friend.friend_id'), unique=False, nullable=False)
    client_group = db.Column(db.Integer, db.ForeignKey('client_group.client_group_id'), unique=False, nullable=False)

    def __repr__(self):
        return '<Complaint %r>' % self.complaint_id
