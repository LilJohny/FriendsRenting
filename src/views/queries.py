from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm import Session
from flask import current_app as app

from src.api.client_queries import ClientQueries
from src.api.friend_queries import FriendQueries
from src.api.holiday_queries import HolidayQueries
from src.api.meeting_queries import MeetingQueries
from src.api.present_queries import PresentQueries
from src.forms.query_10_form import Query10Form
from src.forms.query_11_form import Query11Form
from src.forms.query_12_form import Query12Form
from src.forms.query_1_form import Query1Form
from src.forms.query_2_form import Query2Form
from src.forms.query_3_form import Query3Form
from src.forms.query_4_form import Query4Form
from src.forms.query_5_form import Query5Form
from src.forms.query_6_form import Query6Form
from src.forms.query_7_form import Query7Form
from src.forms.query_8_form import Query8Form
from src.forms.query_9_form import Query9Form
from src.models import engine
from src.models.client import Client
from src.models.friend import Friend
from src.models.holiday import Holiday


@app.route('/queries')
@login_required
def queries():
    return render_template('queries.html')


@app.route('/query_1', methods=['GET', 'POST'])
@login_required
def query_1():
    form = Query1Form()
    if form.validate_on_submit() and form.validate():
        client_id = form.client_id.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        rents = form.rents.data
        session = Session(bind=engine)
        client_id_valid = len(session.query(Client).filter(Client.client_id == client_id).all()) != 0

        if not client_id_valid:
            flash("Wrong Client Id", category="error")
            return redirect(url_for('query_1'))

        data = FriendQueries.get_rented_friends_by_client_rents_and_date(engine, client_id, start_date, end_date, rents,
                                                                         False)
        data = [["name", "surname", "friend_id", "client_id"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_1.html', title='DataBase Query', form=form)


def check_client_id_valid(client_id):
    session = Session(bind=engine)
    result = len(session.query(Client).filter(Client.client_id == client_id).all()) != 0
    return result


def check_friend_id_valid(friend_id):
    session = Session(bind=engine)
    result = len(session.query(Friend).filter(Friend.friend_id == friend_id).all()) != 0
    return result


@app.route('/query_2', methods=['GET', 'POST'])
@login_required
def query_2():
    form = Query2Form()
    if form.validate_on_submit():
        friend_id = form.friend_id.data
        if not check_friend_id_valid(friend_id) or not form.validate():
            flash("Wrong Friend Id", category="error")
            return redirect(url_for('query_2'))
        start_date = form.start_date.data
        end_date = form.end_date.data
        rents = form.rents.data
        data = ClientQueries.get_clients_who_rented_by_date_rents_and_number(engine, friend_id, start_date,
                                                                             end_date, rents, False)
        data = [["name", "surname"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_2.html', title='DataBase Query', form=form)


@app.route('/query_3', methods=['GET', 'POST'])
@login_required
def query_3():
    form = Query3Form()
    if form.validate_on_submit() and form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
        rents = form.rents.data
        data = FriendQueries.get_friends_filtered_by_rents(engine, rents, start_date, end_date, False)
        data = [["friend_id", "name", "surname", "mail", "birth_date", "address"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_3.html', title='DataBase Query', form=form)


@app.route('/query_4', methods=['GET', 'POST'])
@login_required
def query_4():
    form = Query4Form()
    if form.validate_on_submit() and form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
        least_friend = form.least_friend.data
        data = ClientQueries.get_clients_filtered_by_rented_friends_number_and_date(engine, least_friend, start_date,
                                                                                    end_date,
                                                                                    False)
        data = [["client_id", "name", "surname", "mail", "birth_date", "address"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_4.html', title='DataBase Query', form=form)


@app.route('/query_5', methods=['GET', 'POST'])
@login_required
def query_5():
    form = Query5Form()
    if form.validate_on_submit() and form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
        times_hired = form.times_hired.data
        data = FriendQueries.get_all_friends_by_rents_and_date(engine, start_date, end_date, times_hired, False)
        data = [["name", "surname"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_5.html', title='DataBase Query', form=form)


@app.route('/query_6', methods=['GET', 'POST'])
@login_required
def query_6():
    form = Query6Form()
    if form.validate_on_submit():
        session = Session(bind=engine)
        data = MeetingQueries.get_meetings_number_by_months(session, False)
        data = [["meetings number", "month"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_6.html', title='DataBase Query', form=form)


@app.route('/query_7', methods=['GET', 'POST'])
@login_required
def query_7():
    form = Query7Form()
    if form.validate_on_submit():
        friend_id = form.friend_id.data
        if not check_friend_id_valid(friend_id) or not form.validate():
            flash("Wrong Friend Id", category="error")
            return redirect(url_for('query_7'))
        start_date = form.start_date.data
        end_date = form.end_date.data
        least_friends = form.least_friends.data
        data = FriendQueries.get_how_many_times_rented(engine, friend_id, least_friends, start_date, end_date, False)
        data = [["times_hired", "friend_id", "name", "surname"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_7.html', title='DataBase Query', form=form)


@app.route('/query_8', methods=['GET', 'POST'])
@login_required
def query_8():
    form = Query8Form()
    if form.validate_on_submit():
        client_id = form.client_id.data
        if not check_client_id_valid(client_id) or not form.validate():
            flash("Wrong Client Id", category="error")
            return redirect(url_for('query_8'))
        start_date = form.start_date.data
        end_date = form.end_date.data
        data = PresentQueries.get_present_sorted_by_average_holidays(engine, client_id, start_date, end_date, False)
        data = [["avg.holiday", "present_id", "title", "from_id", "to_id", "date", "returned"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_8.html', title='DataBase Query', form=form)


@app.route('/query_9', methods=['GET', 'POST'])
@login_required
def query_9():
    form = Query9Form()
    if form.validate_on_submit() and form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data
        least_clients = form.least_clients.data
        data = FriendQueries.get_all_friends_sorted_by_complaint_number(engine, least_clients, start_date, end_date,
                                                                        False)
        data = [["complaints", "friend_id", "name", "surname"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_9.html', title='DataBase Query', form=form)


@app.route('/query_10', methods=['GET', 'POST'])
@login_required
def query_10():
    form = Query10Form()
    if form.validate_on_submit():
        client_id = form.client_id.data
        friend_id = form.friend_id.data
        if not check_client_id_valid(client_id) or not check_friend_id_valid(friend_id) or not form.validate():
            flash("Wrong Client Id or Friend Id", category="error")
            return redirect(url_for('query_10'))
        start_date = form.start_date.data
        end_date = form.end_date.data
        data = MeetingQueries.get_common_meeting_for_friend_and_client_by_date(engine, friend_id, client_id, start_date,
                                                                               end_date, False)
        data = [["name", "surname", "meeting id"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_10.html', title='DataBase Query', form=form)


@app.route('/query_11', methods=['GET', 'POST'])
@login_required
def query_11():
    form = Query11Form()
    if form.validate_on_submit() and form.validate():
        min_friends_absent = form.min_friends_number.data
        max_friends_absent = form.max_friends_number.data
        session = Session(bind=engine)
        start_date = session.query(Holiday.start_date).order_by(Holiday.start_date).all()[0][0]
        end_date = session.query(Holiday.end_date).order_by(Holiday.end_date).all()
        end_date = end_date[len(end_date) - 1][0]
        data = HolidayQueries.get_day_when_friends_had_holidays(engine, min_friends_absent, max_friends_absent,
                                                                start_date,
                                                                end_date, False)
        data = [["day", "friends on holiday"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_11.html', title='DataBase Query', form=form)


@app.route('/query_12', methods=['GET', 'POST'])
@login_required
def query_12():
    form = Query12Form()
    if form.validate_on_submit():
        friend_id = form.friend_id.data
        if not check_friend_id_valid(friend_id) or not form.validate():
            flash("Wrong  Friend Id", category="error")
            return redirect(url_for('query_8'))
        session = Session(bind=engine)
        data = FriendQueries.get_average_complained_clients_in_group_by_months(session, friend_id, False)
        data = [["avg. complained clients", "month"]] + data
        return render_template('query_results.html', data=data)
    return render_template('query_12.html', title='DataBase Query', form=form)
