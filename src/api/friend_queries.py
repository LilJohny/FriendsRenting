import json
from datetime import date

import sqlalchemy
from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.client import Client
from models.client_group import ClientGroup
from models.client_group_record import ClientGroupRecord
from models.complaint import Complaint
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
        elif request_type == 'get_average_complained_clients_in_group_by_months':
            friend_id = request.form['friend_id']
            return FriendQueries.get_average_complained_clients_in_group_by_months(session, friend_id)

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

    @staticmethod
    def get_average_complained_clients_in_group_by_months(session, friend_id):
        month = sqlalchemy.func.date_trunc('month', Complaint.date)
        records_count = sqlalchemy.sql.func.count(ClientGroupRecord.id)
        records_avg = sqlalchemy.func.avg(records_count).over()
        result = session.query(
                                           records_avg.label('avg'), month).select_from(Friend). \
            join(Complaint, Complaint.friend == Friend.friend_id). \
            join(ClientGroup, Complaint.client_group == ClientGroup.client_group_id). \
            join(ClientGroupRecord, ClientGroup.client_group_id == ClientGroupRecord.client_group_id). \
            join(Client, Client.client_id == ClientGroupRecord.client_id).\
            filter(Friend.friend_id == friend_id).\
            group_by(month).all()
        # TODO FINISH
        records_avg = sqlalchemy.sql.func.avg(records_count)
        result = [[float(month[0]), str(month[1])] for month in result]
        response = json.dumps(result, cls=AlchemyEncoder)
        return response
