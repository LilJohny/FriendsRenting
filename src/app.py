from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:docker@localhost:5432/friends_rent'

# API setup
from api.hello_world import HelloWorld
from api.friend_queries import FriendQueries
api.add_resource(HelloWorld, '/rest_hello_world')
api.add_resource(FriendQueries, '/friends')

@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
