from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import Session

from src.app import app
from src.forms.holiday_form import HolidayForm
from src.forms.return_present_form import ReturnPresentForm
from src.models import engine
from src.models.holiday import Holiday
from src.models.present import Present


@app.route('/take_a_holiday', methods=['GET', 'POST'])
@login_required
def take_a_holiday():
    form = HolidayForm()
    if form.validate_on_submit() and form.validate():
        session = Session(bind=engine)
        user_friend_id = current_user.friend_id
        form_start_date, form_end_date = form.start_date.data, form.end_date.data
        is_on_holiday = session.query(Holiday). \
            filter(Holiday.friend_id == user_friend_id). \
            filter(form_start_date >= Holiday.start_date). \
            filter(form_start_date <= Holiday.end_date). \
            filter(form_end_date >= Holiday.start_date). \
            filter(form_end_date <= Holiday.end_date).all()
        is_on_holiday = len(is_on_holiday) != 0
        if is_on_holiday:
            flash('You are on holiday on these dates already.')
            return redirect(url_for('take_a_holiday'))
        holiday = Holiday()
        holiday.friend_id = current_user.friend_id
        holiday.start_date = form_start_date
        holiday.end_date = form_end_date
        session.add(holiday)
        session.commit()
        return render_template('success.html')
    return render_template('take_holiday.html', title='Taking a holiday', form=form)


@app.route('/returning_a_present', methods=['POST', 'GET'])
@login_required
def return_a_present():
    form = ReturnPresentForm()
    if form.validate_on_submit() and form.validate():
        session = Session(bind=engine)
        user_friend_id = current_user.friend_id
        user_presents = session.query(Present).with_entities(Present.present_id).filter(
            Present.to == user_friend_id).all()
        present_id = form.present_id.data
        present_id_valid = present_id in user_presents
        if not present_id_valid:
            flash("Wrong present id", category="error")
            return redirect(url_for('return_a_present'))
        present = session.query(Present).filter(Present.present_id == present_id).update({Present.returned: True})
        return render_template('success.html')
    return render_template('return_present.html', title='Returning a present', form=form)