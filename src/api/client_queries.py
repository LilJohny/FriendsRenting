import json

from flask import request
from flask_restful import Resource
from sqlalchemy.orm import Session

from models import engine
from models.client import Client
from models.serializer import AlchemyEncoder


class ClientQueries(Resource):
    def post(self):
        request_type = request.form['type']
        session = Session(bind=engine)
        if request_type == 'get_all':
            return ClientQueries.get_all(session)

    @staticmethod
    def get_all(session):
        clients_all = session.query(Client).all()
        response = json.dumps(clients_all, cls=AlchemyEncoder)
