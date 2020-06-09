from flask import url_for, flash, render_template
from flask_login import current_user, login_user, logout_user
from sqlalchemy.orm import Session
from werkzeug.utils import redirect

from app import login, app
from forms.login_form import LoginForm
from models import engine
from models.client import Client
from models.friend import Friend
from models.profile import Profile
from models.user import User


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    form.validate()
    if form.validate_on_submit():
        session = Session(bind=engine)
        client = session.query(User, Client, Profile).select_from(User).join(Client).join(Profile).filter(
            Profile.mail == form.mail.data). \
            filter(User.check_password(Profile.password, form.password.data)).first()
        friend = session.query(User, Friend, Profile).select_from(User).join(Friend).join(Profile). \
            filter(Profile.mail == form.mail.data). \
            filter(User.check_password(Profile.password, form.password.data)).first()

        if friend is None and client is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        user = friend if friend is not None else client
        login_user(user.User, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
