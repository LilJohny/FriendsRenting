from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import Session
import datetime
from app import app
from forms.complaint_form import ComplaintForm
from forms.give_present_form import GivePresentForm
from models import engine
from models.client_group import ClientGroup
from models.client_group_record import ClientGroupRecord
from models.complaint import Complaint
from models.friend import Friend
from models.present import Present


@app.route('/giving_a_present', methods=['POST', 'GET'])
@login_required
def give_a_present():
    form = GivePresentForm()
    if form.validate_on_submit() and form.validate():
        session = Session(bind=engine)
        friend_id = form.friend_id.data
        friend_id_valid = session.query(Friend).filter(Friend.friend_id == friend_id).all()
        friend_id_valid = len(friend_id_valid) != 0
        if not friend_id_valid:
            flash("Wrong Friend Id", category="error")
            return redirect(url_for('give_a_present'))
        today = datetime.datetime.today()
        title = form.title.data
        client_id = current_user.client_id
        present = Present()
        present.to = friend_id
        present.title = title
        present.to = friend_id
        present._from = client_id
        present.date = today
        session.add(present)
        session.commit()
        return render_template('success.html')
    return render_template('give_present.html', title='Giving a present', form=form)


@app.route('/register_complaint', methods=['POST', 'GET'])
@login_required
def register_complaint():
    form = ComplaintForm()
    if form.validate_on_submit() and form.validate():
        session = Session(bind=engine)
        client_group_id = form.client_group_id.data
        user_client_id = current_user.client_id
        client_group_id_valid = session.query(ClientGroup, ClientGroupRecord).select_from(ClientGroup). \
            filter(ClientGroup.client_group_id == client_group_id). \
            join(ClientGroupRecord). \
            filter(ClientGroupRecord.client_id == user_client_id).all()
        client_group_id_valid = len(client_group_id_valid) != 0
        friend_id = form.friend_id.data
        friend_id_valid = session.query(Friend).filter(Friend.friend_id == friend_id).all()
        friend_id_valid = len(friend_id_valid) != 0
        if not friend_id_valid or not client_group_id_valid:
            flash("Wrong Friend Id or Client Group Id", category="error")
            return redirect(url_for('register_complaint'))
        today = datetime.datetime.today()
        complaint = Complaint()
        complaint.friend = friend_id
        complaint.client_group = client_group_id
        complaint.date = today
        session.add(complaint)
        session.commit()
        return render_template('success.html')
    return render_template('register_complaint.html', title='Register complaint', form=form)
