import json

from flask import request
from flask_restful import Resource
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

        elif request_type ==  'get_compliant_to_friend_id':
            friend_id = request.form['friend_id']
            return ClientQueries.get_compliant_to_friend_id(session, friend_id)

        elif request_type == 'get_hired_friend_id':
            friend_id = request.form['friend_id']
            return ClientQueries.get_hired_friend_id(session, friend_id)

        elif request_type == 'get_hired_friend':
            name = request.form['name']
            surname = request.form['surname']
            return ClientQueries.get_hired_friend(session, name, surname)

    @staticmethod
    def get_all(session):
        clients_all = session.query(Client).all()
        response = json.dumps(clients_all, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_compliant_to_friend(session, name, surname):
        clients_compliant_to_friend = session.query(Client).join(ClientGroupRecord).join(ClientGroup).\
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
        clients_hired_friend = session.query(Client).join(Meeting).join(FriendGroup).join(FriendGroupRecord).\
            join(Friend).filter(Friend.friend_id == friend_id).all()
        response = json.dumps(clients_hired_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_hired_friend(session, name, surname):
        clients_hired_friend = session.query(Client).join(Meeting).join(FriendGroup).join(FriendGroupRecord).\
            join(Friend).filter(Friend.name == name).filter(Friend.surname == surname).all()
        response = json.dumps(clients_hired_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_rented_friends_by_client_time_rents_and_date(engine, client_id, start_date, finish_date,
                                                   rents):
        with engine.connect() as connection:
            sql_statement = f"""select friend.name, friend.surname from client c
                            inner join meeting m using(client_id)
                            inner join friend_group using(friend_group_id) 
                            inner join friend_group_record using(friend_group_id) 
                            inner join friend using(friend_id)
                            where c.client_id = {client_id} and m.date between {start_date} and {finish_date}
                            group by friend.friend_id
                            having count(friend.friend_id) >= {rents};"""

            result = connection.execute(text(sql_statement))
        response = json.dumps(result, cls=AlchemyEncoder)
        return response