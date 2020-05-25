import json

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.present import Present
from models.friend import Friend
from models.serializer import AlchemyEncoder


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
        response = json.dumps(presents_all, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_presents_of_friend(session, name, surname):
        presents_of_friend = session.query(Present).join(Friend).filter(Friend.surname == surname).\
            filter(Friend.name == name).all()
        response = json.dumps(presents_of_friend, cls=AlchemyEncoder)
        return response

    @staticmethod
    def get_presents_by_friend_id(session, friend_id):
        presents_of_friend = session.query(Present).join(Friend).filter(Friend.friend_id == friend_id).all()
        response = json.dumps(presents_of_friend, cls=AlchemyEncoder)
        return response
