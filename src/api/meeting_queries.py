import json

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.meeting import Meeting
from models.serializer import AlchemyEncoder


class MeetingQueries(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return MeetingQueries.get_all(session)

    @staticmethod
    def get_all(session):
        meeting_all = session.query(Meeting).all()
        response = json.dumps(meeting_all, cls=AlchemyEncoder)
        return response
