import json

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session
from models import engine
from models.friend import Friend
from models.serializer import AlchemyEncoder


class FriendView(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        all_friends = session.query(Friend).all()
        if request_type == 'get_all':
            response = json.dumps(all_friends, cls=AlchemyEncoder)
            return response
