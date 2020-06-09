from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm import Session

from api.friend_queries import FriendQueries
from app import app
from forms.query_10_form import Query10Form
from forms.query_11_form import Query11Form
from forms.query_12_form import Query12Form
from forms.query_1_form import Query1Form
from forms.query_2_form import Query2Form
from forms.query_3_form import Query3Form
from forms.query_4_form import Query4Form
from forms.query_5_form import Query5Form
from forms.query_6_form import Query6Form
from forms.query_7_form import Query7Form
from forms.query_8_form import Query8Form
from forms.query_9_form import Query9Form
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
    return render_template('query_1.html', title='DataBase Query', form=form)


@app.route('/query_2', methods=['GET', 'POST'])
@login_required
def query_2():
    form = Query2Form()
    return render_template('query_2.html', title='DataBase Query', form=form)


@app.route('/query_3', methods=['GET', 'POST'])
@login_required
def query_3():
    form = Query3Form()
    return render_template('query_3.html', title='DataBase Query', form=form)


@app.route('/query_4', methods=['GET', 'POST'])
@login_required
def query_4():
    form = Query4Form()
    return render_template('query_4.html', title='DataBase Query', form=form)


@app.route('/query_5', methods=['GET', 'POST'])
@login_required
def query_5():
    form = Query5Form()
    return render_template('query_5.html', title='DataBase Query', form=form)


@app.route('/query_6', methods=['GET', 'POST'])
@login_required
def query_6():
    form = Query6Form()
    return render_template('query_6.html', title='DataBase Query', form=form)


@app.route('/query_7', methods=['GET', 'POST'])
@login_required
def query_7():
    form = Query7Form()
    return render_template('query_7.html', title='DataBase Query', form=form)


@app.route('/query_8', methods=['GET', 'POST'])
@login_required
def query_8():
    form = Query8Form()
    return render_template('query_8.html', title='DataBase Query', form=form)


@app.route('/query_9', methods=['GET', 'POST'])
@login_required
def query_9():
    form = Query9Form()
    return render_template('query_9.html', title='DataBase Query', form=form)


@app.route('/query_10', methods=['GET', 'POST'])
@login_required
def query_10():
    form = Query10Form()
    return render_template('query_10.html', title='DataBase Query', form=form)


@app.route('/query_11', methods=['GET', 'POST'])
@login_required
def query_11():
    form = Query11Form()
    return render_template('query_11.html', title='DataBase Query', form=form)


@app.route('/query_12', methods=['GET', 'POST'])
@login_required
def query_12():
    form = Query12Form()
    return render_template('query_12.html', title='DataBase Query', form=form)
