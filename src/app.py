from flask import Flask, render_template
from flask_restful import Api
from flask_login import LoginManager

from models.user import User

app = Flask(__name__)
login = LoginManager(app)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:docker@localhost:5432/friends_rent'

# API setup
from api.hello_world import HelloWorld
from api.friend_queries import FriendQueries
from api.client_queries import ClientQueries
from api.meeting_queries import MeetingQueries
from api.present_queries import PresentQueries
from api.holiday_queries import HolidayQueries

api.add_resource(HelloWorld, '/rest_hello_world')
api.add_resource(FriendQueries, '/friends')
api.add_resource(ClientQueries, '/clients')
api.add_resource(MeetingQueries, '/meetings')
api.add_resource(PresentQueries, '/presents')
api.add_resource(HolidayQueries, '/holiday')


@app.route('/')
def hello():
    return render_template('dashboard.html')


@app.route('/actions')
def actions():
    return render_template('actions_clients.html')


@app.route('/queries')
def queries():
    return render_template('queries.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run()
