from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import Session

from app import app
from forms.holiday_form import HolidayForm
from models import engine
from models.holiday import Holiday


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
