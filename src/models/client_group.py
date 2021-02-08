from . import db


class ClientGroup(db.Model):
    client_group_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Client group %r>' % self.client_group_id
