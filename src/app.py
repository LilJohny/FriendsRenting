from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'

api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:docker@localhost:5432/friends_rent'

# Secret key
import os

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# Views
import views.profile
import views.login
import views.dashboard
import views.queries
import views.actions
import views.index
import views.friend_actions_views
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

if __name__ == '__main__':
    app.run()
