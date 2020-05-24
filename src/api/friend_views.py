from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session
from models import engine
from models.friend import Friend


class FriendView(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        all_friends = session.query(Friend).all()
        if request_type == 'get_all':
            return all_friends
