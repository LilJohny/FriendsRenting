import json

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
