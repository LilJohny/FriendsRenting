import json
from datetime import date

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.friend import Friend
from models.friend_group import FriendGroup
from models.friend_group_record import FriendGroupRecord
from models.holiday import Holiday
from models.meeting import Meeting
from models.serializer import AlchemyEncoder


class FriendQueries(Resource):

    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return FriendQueries.get_all_friends(session)
        elif request_type == 'get_available':
            return FriendQueries.get_available_friends(session)
        elif request_type == 'get_by_client_id':
            client_id = int(request.form['client_id'])
            return FriendQueries.get_by_client_id(session, client_id)
        elif request_type == 'get_by_name':
            name = request.form['name']
            surname = request.form['surname']
            return FriendQueries.get_by_name(session, name, surname)

    @staticmethod
    def get_all_friends(session):
        friends_all = session.query(Friend).all()
        response = json.dumps(friends_all, cls=AlchemyEncoder)
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

    @staticmethod
    def get_by_client_id(session, client_id):
        friends_by_client_id = session.query(Friend).join(FriendGroupRecord).join(FriendGroup).join(Meeting).filter(
            Meeting.client_id == client_id).all()
        response = json.dumps(friends_by_client_id, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_by_name(session, name, surname):
        friends_by_name = session.query(Friend).filter(Friend.surname == surname).filter(Friend.name == name).all()
        response = json.dumps(friends_by_name, cls=AlchemyEncoder)
        return response
