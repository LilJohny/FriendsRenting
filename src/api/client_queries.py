import json

from flask import request
from flask_restful import Resource
from sqlalchemy import text
from sqlalchemy.orm import Session

from models import engine
from models.client import Client
from models.client_group_record import ClientGroupRecord
from models.client_group import ClientGroup
from models.complaint import Complaint
from models.friend import Friend
from models.meeting import Meeting
from models.friend_group import FriendGroup
from models.friend_group_record import FriendGroupRecord
from models.serializer import AlchemyEncoder


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
            rents = request.form['rents']
            return ClientQueries.get_clients_who_rented_by_date_rents_and_number(engine, friend_id, start_date,
                                                                                 end_date, rents)

    @staticmethod
    def get_all(session):
        clients_all = session.query(Client).all()
        response = json.dumps(clients_all, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_compliant_to_friend(session, name, surname):
        clients_compliant_to_friend = session.query(Client).join(ClientGroupRecord).join(ClientGroup). \
            join(Complaint).join(Friend).filter(Friend.name == name).filter(Friend.surname == surname).all()
        response = json.dumps(clients_compliant_to_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_compliant_to_friend_id(session, friend_id):
        clients_compliant_to_friend = session.query(Client).join(ClientGroupRecord).join(ClientGroup). \
            join(Complaint).join(Friend).filter(Friend.friend_id == friend_id).all()
        response = json.dumps(clients_compliant_to_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_hired_friend_id(session, friend_id):
        clients_hired_friend = session.query(Client).join(Meeting).join(FriendGroup).join(FriendGroupRecord). \
            join(Friend).filter(Friend.friend_id == friend_id).all()
        response = json.dumps(clients_hired_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_hired_friend(session, name, surname):
        clients_hired_friend = session.query(Client).join(Meeting).join(FriendGroup).join(FriendGroupRecord). \
            join(Friend).filter(Friend.name == name).filter(Friend.surname == surname).all()
        response = json.dumps(clients_hired_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_clients_who_rented_by_date_rents_and_number(sql_engine, friend_id, start_date, end_date, rents):
        with sql_engine.connect() as connection:
            sql_statement = f"""select profile.name, profile.surname from friend f
                                left join profile using (profile_id)
                                inner join friend_group_record using(friend_id) 
                                inner join friend_group using(friend_group_id) 
                                inner join meeting m using(friend_group_id)
                                inner join client c using(client_id)
                                where f.friend_id = {friend_id} and m.date between {start_date} and {end_date}
                                group by c.client_id
                                having count(c.client_id) >= {rents};"""
            result = connection.execute(text(sql_statement))
        response = json.dumps(result, cls=AlchemyEncoder)
        return response
