from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from .utils import get_sql_response
from src.models import engine
from src.models.holiday import Holiday


class HolidayQueries(Resource):

    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_number_holidays':
            num_friends = request.form['num_friends']
            return HolidayQueries.get_number_holidays(session, num_friends)

    @staticmethod
    def get_number_holidays(session, num_friends):
        num_friends = session.query(Holiday).all()

    @staticmethod
    def get_day_when_friends_had_holidays(sql_engine, min_friends_absent, max_friends_absent, start_date, end_date,
                                          jsonify_response):
        sql_statement = f"""select day::date, count(*) as friends_on_holiday
                                from generate_series(date '{start_date}', date '{end_date}', '1 day') as gs(day)
                                left join holiday h on h.start_date <= day and h.end_date >= day
                                left join friend f on h.friend_id = f.friend_id
                                group by day
                                having count(*) >= {min_friends_absent}
                                and count(*) <= {max_friends_absent};"""
        response = get_sql_response(sql_engine, sql_statement, jsonify_response)
        return response
