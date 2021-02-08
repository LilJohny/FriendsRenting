from . import db


class FriendGroupRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.friend_id', ondelete='CASCADE'), unique=False, nullable=False)
    friend_group_id = db.Column(db.Integer, db.ForeignKey('friend_group.friend_group_id', ondelete='CASCADE'), unique=False, nullable=False)

    def __repr__(self):
        return '<Client group %r>' % self.id
