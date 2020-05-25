from models import db


class Meeting(db.Model):
    meeting_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), unique=False, nullable=False)
    friend_group_id = db.Column(db.Integer, db.ForeignKey('friend_group.friend_group_id'), unique=False, nullable=False)

    def __repr__(self):
        return '<Client group %r>' % ''.join([self.name, self.surname])
