from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import Session
import datetime
from src.app import app
from src.forms.complaint_form import ComplaintForm
from src.forms.friend_for_date_form import HireFriendForMeetingForm
from src.forms.friends_for_fest import HireFriendsForFestForm
from src.forms.give_present_form import GivePresentForm
from src.models import engine
from src.models.client_group import ClientGroup
from src.models.client_group_record import ClientGroupRecord
from src.models.complaint import Complaint
from src.models.friend import Friend
from src.models.friend_group import FriendGroup
from src.models.friend_group_record import FriendGroupRecord
from src.models.meeting import Meeting
from src.models.present import Present


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


@app.route('/hire_friend_for_a_date', methods=['GET', 'POST'])
@login_required
def hire_friend_for_a_date():
    form = HireFriendForMeetingForm()
    if form.validate_on_submit():
        session = Session(bind=engine)
        friend_id = form.friend_id.data
        user_client_id = current_user.client_id

        friend_id_valid = session.query(Friend).filter(Friend.friend_id == friend_id).all()
        friend_id_valid = len(friend_id_valid) != 0
        if not friend_id_valid:
            flash("Wrong Friend Id", category="error")
            return redirect(url_for('hire_friend_for_a_date'))
        friend_group = FriendGroup()
        friend_group_id = len(session.query(FriendGroup).all()) + 1
        friend_group.friend_group_id = friend_group_id
        friend_group_record = FriendGroupRecord()
        friend_group_record.friend_group_id = friend_group.friend_group_id
        friend_group_record.friend_id = friend_id

        today = datetime.datetime.today()
        meeting = Meeting()
        meeting.friend_group_id = friend_group.friend_group_id
        meeting.client_id = user_client_id
        meeting.date = today
        session.add(meeting)
        session.add(friend_group)
        session.add(friend_group_record)
        session.commit()
        return render_template('success.html')
    return render_template('hire_friend.html', title='Hire friend for a date', form=form)


@app.route('/hire_friends_for_a_fest', methods=['GET', 'POST'])
@login_required
def hire_friends_for_a_fest():
    form = HireFriendsForFestForm()
    if form.validate_on_submit():
        session = Session(bind=engine)
        friends_id = form.friends_id.data
        user_client_id = current_user.client_id
        friends_ids = friends_id.split(' ')
        try:
            friends_ids = [int(f_id) for f_id in friends_ids]
        except:
            flash("Invalid some of Friends Id", category="error")
            return redirect(url_for('hire_friends_for_a_fest'))
        friends_id_valid = True
        if len(friends_ids):
            for friends_id_term in friends_ids:
                friends_id_term_valid = session.query(Friend).filter(Friend.friend_id == friends_id_term).all()
                friends_id_term_valid = len(friends_id_term_valid) != 0
                friends_id_valid = friends_id_valid and friends_id_term_valid
                if not friends_id_valid:
                    break

        if not friends_id_valid:
            flash("Wrong some of Friends Id", category="error")
            return redirect(url_for('hire_friends_for_a_fest'))

        friend_group = FriendGroup()
        friend_group_id = len(session.query(FriendGroup).all()) + 1
        friend_group.friend_group_id = friend_group_id
        for f_id in friends_ids:
            friend_group_record = FriendGroupRecord()
            friend_group_record.friend_group_id = friend_group.friend_group_id
            friend_group_record.friend_id = f_id
            session.add(friend_group_record)
        today = datetime.datetime.today()
        meeting = Meeting()
        meeting.friend_group_id = friend_group.friend_group_id
        meeting.client_id = user_client_id
        meeting.date = today
        session.add(meeting)
        session.add(friend_group)
        session.commit()
        return render_template('success.html')
    return render_template('hire_friends.html', title='Hire friend for a date', form=form)
