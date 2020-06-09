from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from api.utils import jsonify, get_sql_response
from models import engine
from models.friend import Friend
from models.present import Present


class PresentQueries(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return PresentQueries.get_all(session)

        elif request_type == 'get_presents_of_friend':
            name = request.form['name']
            surname = request.form['surname']
            return PresentQueries.get_presents_of_friend(session, name, surname)

        elif request_type == 'get_presents_by_friend_id':
            friend_id = request.form['friend_id']
            return PresentQueries.get_presents_by_friend_id(session, friend_id)

    @staticmethod
    def get_all(session):
        presents_all = session.query(Present).all()
        return jsonify(presents_all)

    @staticmethod
    def get_presents_of_friend(session, name, surname):
        presents_of_friend = session.query(Present).join(Friend).filter(Friend.surname == surname). \
            filter(Friend.name == name).all()
        return jsonify(presents_of_friend)

    @staticmethod
    def get_presents_by_friend_id(session, friend_id):
        presents_of_friend = session.query(Present).join(Friend).filter(Friend.friend_id == friend_id).all()
        return jsonify(presents_of_friend)

    @staticmethod
    def get_present_sorted_by_average_holidays(sql_engine, client_id, start_date, end_date, jsonify_response=True):

        sql_statement = f"""select avg(end_date - start_date), present_id, title, _from, "to", p.date, returned
                            from friend
                            inner join holiday h on friend.friend_id = h.friend_id
                            inner join present p on friend.friend_id = p."to"
                            left join client c on p._from = c.client_id
                            where p._from = {client_id} and p.date >=  date '{start_date}' and p.date <= date  '{end_date}'
                            group by p.present_id, p.title, p._from, p."to"
                            order by avg(end_date - start_date) desc ;"""

        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response
