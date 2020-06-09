from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import Session
import datetime
from app import app
from forms.give_present_form import GivePresentForm
from models import engine
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
