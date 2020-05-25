import json

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.meeting import Meeting
from models.friend import Friend
from models.friend_group import FriendGroup
from models.friend_group_record import FriendGroupRecord
from models.serializer import AlchemyEncoder


class MeetingQueries(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return MeetingQueries.get_all(session)
        elif request_type == 'get_meetings_by_friend_name':
            name = request.form['name']
            surname = request.form['surname']
            return MeetingQueries.get_meetings_by_friend_name(session, name, surname)

    @staticmethod
    def get_all(session):
        meeting_all = session.query(Meeting).all()
        response = json.dumps(meeting_all, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_meetings_by_friend_name(session, name, surname):
        meeting_by_friend_name = session.query(Meeting).join(FriendGroup).\
            join(FriendGroupRecord).join(Friend).filter(Friend.name == name and Friend.surname == surname).all()
        response = json.dumps(meeting_by_friend_name, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_meetings_by_friend_id(session, friend_id):
        meeting_by_friend_id = session.query(Meeting).join(FriendGroup). \
            join(FriendGroupRecord).join(Friend).filter(Friend.friend_id == friend_id).all()
        response = json.dumps(meeting_by_friend_id, cls=AlchemyEncoder)
        return response
