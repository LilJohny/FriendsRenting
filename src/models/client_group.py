from app import db


class Client_group(db.Model):
    client_group_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Client group %r>' % ''.join([self.name, self.surname])
