import json

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from .utils import get_sql_response
from ..models import engine
from ..models.client import Client
from ..models.client_group import ClientGroup
from ..models.client_group_record import ClientGroupRecord
from ..models.complaint import Complaint
from ..models.friend import Friend
from ..models.friend_group import FriendGroup
from ..models.friend_group_record import FriendGroupRecord
from ..models.meeting import Meeting
from ..models.profile import Profile
from ..models.serializer import AlchemyEncoder


class ClientQueries(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return ClientQueries.get_all(session)
        elif request_type == 'get_compliant_to_friend':
            name = request.form['name']
            surname = request.form['surname']
            return ClientQueries.get_compliant_to_friend(session, name, surname)

        elif request_type == 'get_compliant_to_friend_id':
            friend_id = request.form['friend_id']
            return ClientQueries.get_compliant_to_friend_id(session, friend_id)

        elif request_type == 'get_hired_friend_id':
            friend_id = request.form['friend_id']
            return ClientQueries.get_hired_friend_id(session, friend_id)

        elif request_type == 'get_hired_friend':
            name = request.form['name']
            surname = request.form['surname']
            return ClientQueries.get_hired_friend(session, name, surname)

        elif request_type == 'get_clients_who_rented_by_date_rents_and_number':
            friend_id = request.form['friend_id']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            rents = request.form['friends_rented']
            return ClientQueries.get_clients_who_rented_by_date_rents_and_number(engine, friend_id, start_date,
                                                                                 end_date, rents)

    @staticmethod
    def get_all(session, jsonify_response=True):
        clients_all = session.query(Client, Profile).select_from(Client).join(Profile).all()
        response = json.dumps(clients_all, cls=AlchemyEncoder) if jsonify_response else clients_all
        return response

    @staticmethod
    def get_compliant_to_friend(session, name, surname, jsonify_response=True):
        clients_compliant_to_friend = session.query(Client, Profile).select_from(Client).join(Profile).join(
            ClientGroupRecord).join(ClientGroup).join(Complaint).join(Friend).filter(Friend.name == name).filter(
            Friend.surname == surname).all()
        response = json.dumps(clients_compliant_to_friend,
                              cls=AlchemyEncoder) if jsonify_response else clients_compliant_to_friend
        return response

    @staticmethod
    def get_compliant_to_friend_id(session, friend_id, jsonify_response=True):
        clients_compliant_to_friend = session.query(Client, Profile).select_from(Client).join(Profile).join(
            ClientGroupRecord).join(ClientGroup).join(Complaint).join(Friend).filter(
            Friend.friend_id == friend_id).all()
        response = json.dumps(clients_compliant_to_friend,
                              cls=AlchemyEncoder) if jsonify_response else clients_compliant_to_friend
        return response

    @staticmethod
    def get_hired_friend_id(session, friend_id, jsonify_response=True):
        clients_hired_friend = session.query(Client, Profile).select_from(Client). \
            join(Profile).join(Meeting).join(FriendGroup).join(FriendGroupRecord).join(Friend). \
            filter(Friend.friend_id == friend_id).all()
        response = json.dumps(clients_hired_friend, cls=AlchemyEncoder) if jsonify_response else clients_hired_friend
        return response

    @staticmethod
    def get_hired_friend(session, name, surname, jsonify_response=True):
        clients_hired_friend = session.query(Client, Profile).select_from(Client).join(Profile). \
            join(Meeting).join(FriendGroup).join(FriendGroupRecord).join(Friend). \
            filter(Friend.name == name).filter(Friend.surname == surname).all()
        response = json.dumps(clients_hired_friend, cls=AlchemyEncoder) if jsonify_response else clients_hired_friend
        return response

    @staticmethod
    def get_clients_who_rented_by_date_rents_and_number(sql_engine, friend_id, start_date, end_date, rents,
                                                        jsonify_response=True):
        sql_statement = f"""select profile.name, profile.surname from friend f
                                inner join friend_group_record using(friend_id) 
                                inner join friend_group using(friend_group_id) 
                                inner join meeting m using(friend_group_id)
                                inner join client c using(client_id)
                                left join profile on c.profile_id = profile.profile_id
                                where f.friend_id = {friend_id} and m.date between date '{start_date}' and date '{end_date}'
                                group by profile.name, profile.surname,c.client_id
                                having count(c.client_id) >= {rents};"""

        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response

    @staticmethod
    def get_clients_filtered_by_rented_friends_number_and_date(sql_engine, friends_rented, start_date, end_date,
                                                               jsonify_response=True):
        sql_statement = f"""select client.client_id, p.name, p.surname, p.mail, p.birth_date, p.address
                                from client
                                left join profile p on client.profile_id = p.profile_id
                                left join meeting m on client.client_id = m.client_id
                                left join friend_group fg on m.friend_group_id = fg.friend_group_id
                                left join friend_group_record fgr on fg.friend_group_id = fgr.friend_group_id
                                where m.date between date '{start_date}' and date '{end_date}'
                                group by client.client_id, p.name, p.surname, p.mail, p.birth_date, p.address
                                having count(fgr.id)>={friends_rented};"""
        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response
