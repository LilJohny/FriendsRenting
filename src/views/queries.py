from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm import Session

from api.friend_queries import FriendQueries
from app import app
from forms.query_1_form import Query1Form
from models import engine
from models.client import Client


@app.route('/queries')
@login_required
def queries():
    return render_template('queries.html')


@app.route('/query_1', methods=['GET', 'POST'])
@login_required
def query_1():
    form = Query1Form()
    if form.validate_on_submit():
        client_id = form.client_id.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        rents = form.rents.data
        session = Session(bind=engine)
        client_id_valid = len(session.query(Client).filter(Client.client_id == client_id).all()) != 0

        if not client_id_valid:
            flash("Wrong Client Id", category="error")
            return redirect(url_for('query_1'))

        FriendQueries.get_rented_friends_by_client_rents_and_date(engine, client_id, start_date, end_date, rents, False)
        return render_template('success.html')
    return render_template('query_1.html', title='Hire friend for a date', form=form)
