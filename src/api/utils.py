import json
import datetime
import random

from sqlalchemy import text

from models.serializer import AlchemyEncoder


def execute_sql_statement(sql_engine, sql_statement):
    statement = text(sql_statement)
    with sql_engine.connect() as connection:
        result = connection.execute(statement)
    return result


def jsonify(result):
    response = json.dumps(result, cls=AlchemyEncoder)
    return response


def get_sql_response(sql_engine, sql_statement, jsonify_response=False):
    response = execute_sql_statement(sql_engine, sql_statement)
    response = jsonify(response) if jsonify_response else response
    return response


def get_random_date(start_date, end_date):

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date
