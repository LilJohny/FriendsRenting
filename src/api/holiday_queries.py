import json
from datetime import date

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.friend import Friend
from models.holiday import Holiday
from models.serializer import AlchemyEncoder


class HolidayQueries(Resource):

    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_number_holidays':
            num_friends = request.form['num_friends']
            return HolidayQueries.get_number_holidays(session, num_friends)

    @staticmethod
    def get_number_holidays(session, num_friends):
        return