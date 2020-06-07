import json
from datetime import date

import sqlalchemy
from flask import request
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.utils import get_sql_response, jsonify
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
from models.profile import Profile
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

        elif request_type == 'get_days_when_was_number_of_friends_available':
            min_friends = request.form['min_friends_number']
            max_friends = request.form['max_friends_number']
            return FriendQueries.get_days_when_was_number_of_friends_available(session, min_friends, max_friends)

        elif request_type == 'get_all_friends_by_rents_and_date':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            rents = request.form['friends_rented']
            return FriendQueries.get_all_friends_by_rents_and_date(engine, rents, start_date, end_date)

        elif request_type == 'get_rented_friends_by_client_time_rents_and_date':
            client_id = request.form['client_id']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            rents = request.form['rent']

            return FriendQueries.get_rented_friends_by_client_rents_and_date(engine, client_id, start_date,
                                                                             end_date, rents)

    @staticmethod
    def get_all_friends(session, jsonify_response=True):
        friends_all = session.query(Friend, Profile).select_from(Friend).join(Profile).all()
        response = json.dumps(friends_all, cls=AlchemyEncoder) if jsonify_response else friends_all
        return response

    @staticmethod
    def get_available_friends(session,  jsonify_response=True):
        now = date.today()
        before_available_friends = session.query(Friend, Holiday, Profile).select_from(Friend). \
            join(Profile).join(Holiday).filter(now < Holiday.start_date).all()

        after_available_friends = session.query(Friend, Holiday, Profile).select_from(Friend). \
            join(Profile).join(Holiday).filter(now > Holiday.end_date).all()

        available_friends = before_available_friends + after_available_friends
        available_friends = [[friend.Friend, friend.Profile] for friend in available_friends]
        response = json.dumps(available_friends, cls=AlchemyEncoder) if jsonify_response else available_friends
        return response

    @staticmethod
    def get_by_client_id(session, client_id, jsonify_response=True):
        friends_by_client_id = session.query(Friend, Profile).select_from(Friend).join(Profile).join(
            FriendGroupRecord).join(FriendGroup).join(Meeting).filter(
            Meeting.client_id == client_id).all()
        response = json.dumps(friends_by_client_id, cls=AlchemyEncoder) if jsonify_response else friends_by_client_id
        return response

    @staticmethod
    def get_by_name(session, name, surname, jsonify_response=True):
        friends_by_name = session.query(Friend, Profile).select_from(Friend).join(Profile).filter(
            Profile.surname == surname).filter(Profile.name == name).all()
        response = json.dumps(friends_by_name, cls=AlchemyEncoder) if jsonify_response else friends_by_name
        return response

    @staticmethod
    def get_average_complained_clients_in_group_by_months(session, friend_id, jsonify_response=True):
        month = func.date_trunc('month', Complaint.date)
        records_count = sqlalchemy.sql.func.count(ClientGroupRecord.id)
        records_avg = func.avg(records_count).over()
        result = session.query(records_avg.label('avg'), month).select_from(Friend). \
            join(Complaint, Complaint.friend == Friend.friend_id). \
            join(ClientGroup, Complaint.client_group == ClientGroup.client_group_id). \
            join(ClientGroupRecord, ClientGroup.client_group_id == ClientGroupRecord.client_group_id). \
            join(Client, Client.client_id == ClientGroupRecord.client_id). \
            filter(Friend.friend_id == friend_id). \
            group_by(month).all()
        result = [[float(month[0]), str(month[1])] for month in result]
        response = jsonify(result) if jsonify_response else result
        return response

    @staticmethod
    def get_all_friends_by_rents_and_date(sql_engine, start_date, end_date, rents, jsonify_response=True):
        sql_statement = f"""select profile.name, profile.surname from client c
                                left join profile using (profile_id)
                                inner join meeting m using(client_id)
                                inner join friend_group using(friend_group_id) 
                                inner join friend_group_record using(friend_group_id) 
                                inner join friend using(friend_id)
                                where m.date between {start_date} and {end_date}
                                group by friend.friend_id
                                having count(friend.friend_id) >= {rents};"""
        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response

    @staticmethod
    def get_rented_friends_by_client_rents_and_date(sql_engine, client_id, start_date, end_date,
                                                    rents, jsonify_response=True):
        sql_statement = f"""select profile.name, profile.surname from client c
                                left join profile using (profile_id)
                                inner join meeting m using(client_id)
                                inner join friend_group using(friend_group_id) 
                                inner join friend_group_record using(friend_group_id) 
                                inner join friend using(friend_id)
                                where c.client_id = {client_id} and m.date between {start_date} and {end_date}
                                group by friend.friend_id
                                having count(friend.friend_id) >= {rents};"""
        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response

    @staticmethod
    def get_friends_filtered_by_rents(sql_engine, rents, start_date, end_date, jsonify_response=True):
        sql_statement = f"""select friend.friend_id, name, surname, mail, birth_date, address from friend
                                left join profile p on friend.profile_id = p.profile_id
                                left join friend_group_record fgr on friend.friend_id = fgr.friend_id
                                left join meeting m on fgr.friend_group_id = m.friend_group_id
                                where m.date between {start_date} and {end_date}
                                group by friend.friend_id, name, surname, mail, birth_date, address
                                having count(friend.friend_id) >= {rents};"""
        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response

    @staticmethod
    def get_all_friends_sorted_by_complaint_number(sql_engine, min_clients_number, start_date, end_date,
                                                   jsonify_response=True):
        sql_statement = f"""select count(*) as complaints, friend_id
                                from (select count(cgr.id), complaint.friend as friend_id
                                    from complaint
                                    left join client_group cg on complaint.client_group = cg.client_group_id
                                    left join friend on complaint.friend = friend.friend_id
                                    left join client_group_record cgr on cg.client_group_id = cgr.client_group_id
                                    group by cg.client_group_id, complaint.date, complaint.friend
                                    having count(cgr.id) >= {min_clients_number}
                                    and (complaint.date >= {start_date} and complaint.date <= {end_date})) as cf
                                    group by friend_id
                                    order by complaints desc;"""

        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response
