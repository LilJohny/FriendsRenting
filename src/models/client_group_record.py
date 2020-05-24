from models import db


class ClientGroupRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete='CASCADE'), unique=False, nullable=False)
    client_group_id = db.Column(db.Integer, db.ForeignKey('client_group.client_group_id', ondelete='CASCADE'), unique=False, nullable=False)

    def __repr__(self):
        return '<Client group %r>' % ''.join([self.name, self.surname])
