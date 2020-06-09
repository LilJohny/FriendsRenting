import json

import sqlalchemy
from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from api.utils import get_sql_response
from models import engine
from models.friend import Friend
from models.friend_group import FriendGroup
from models.friend_group_record import FriendGroupRecord
from models.meeting import Meeting
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
        elif request_type == 'get_meetings_by_friend_id':
            friend_id = request.form['friend_id']
            return MeetingQueries.get_meetings_by_friend_id(session, friend_id)
        elif request_type == 'get_meetings_number_by_months':
            return MeetingQueries.get_meetings_number_by_months(session)
        elif request_type == 'get_common_meeting_for_friend_and_client_by_date':
            friend_id = request.form['friend_id']
            client_id = request.form['client_id']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            return MeetingQueries.get_common_meeting_for_friend_and_client_by_date(engine, friend_id, client_id,
                                                                                   start_date, end_date)

    @staticmethod
    def get_all(session):
        meeting_all = session.query(Meeting).all()
        response = json.dumps(meeting_all, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_meetings_by_friend_name(session, name, surname):
        meeting_by_friend_name = session.query(Meeting).join(FriendGroup). \
            join(FriendGroupRecord).join(Friend).filter(Friend.name == name).filter(Friend.surname == surname).all()
        response = json.dumps(meeting_by_friend_name, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_meetings_by_friend_id(session, friend_id):
        meeting_by_friend_id = session.query(Meeting).join(FriendGroup). \
            join(FriendGroupRecord).join(Friend).filter(Friend.friend_id == friend_id).all()
        response = json.dumps(meeting_by_friend_id, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_meetings_number_by_months(session, jsonify_response=True):
        month = sqlalchemy.func.date_trunc('month', Meeting.date)
        result = session.query(sqlalchemy.func.count(Meeting.meeting_id), month).group_by(month).all()
        result = [[month[0], str(month[1])] for month in result]
        response = json.dumps(result, cls=AlchemyEncoder) if jsonify_response else result
        return response

    @staticmethod
    def get_common_meeting_for_friend_and_client_by_date(sql_engine, friend_id, client_id, start_date, end_date,
                                                         jsonify_response):
        sql_statement = f"""select p.name, p.surname, m.meeting_id from client c 
                                inner join meeting m using(client_id)
                                inner join friend_group using(friend_group_id) 
                                inner join friend_group_record using(friend_group_id) 
                                inner join friend using(friend_id)
                                left join profile p on friend.profile_id = p.profile_id
                                where friend.friend_id = {friend_id} and c.client_id = {client_id} and m.date between date '{start_date}' and date  '{end_date}'
                                group by friend.friend_id,p.name, p.surname, m.meeting_id;"""
        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response
