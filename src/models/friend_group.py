from . import db


class FriendGroup(db.Model):
    friend_group_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Client group %r>' % self.friend_group_id
