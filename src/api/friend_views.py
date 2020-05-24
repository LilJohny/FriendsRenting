import json
from datetime import datetime, date

import pytz
from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session
from models import engine
from models.friend import Friend
from models.holiday import Holiday
from models.serializer import AlchemyEncoder


class FriendView(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return FriendView.get_all_friends(session)
        elif request_type == 'get_available':
            return FriendView.get_available_friends(session)

    @staticmethod
    def get_all_friends(session):
        all_friends = session.query(Friend).all()
        response = json.dumps(all_friends, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_available_friends(session):
        now = date.today()
        before_available_friends = session.query(Friend, Holiday).select_from(Friend).join(Holiday).filter(
            now < Holiday.start_date).all()
        after_available_friends = session.query(Friend, Holiday).select_from(Friend).join(Holiday).filter(
            now > Holiday.end_date).all()

        available_friends = before_available_friends + after_available_friends
        available_friends = [friend.Friend for friend in available_friends]
        response = json.dumps(available_friends, cls=AlchemyEncoder)
        return response
