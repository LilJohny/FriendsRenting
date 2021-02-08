from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class HolidayForm(FlaskForm):
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('Start date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_end_date(self, field):
        field = field.data
        start_date = self.start_date.data
        difference = (field - start_date).days
        return difference > 0

    def validate_on_submit(self):
        return True if self.start_date.data is not None and self.end_date.data is not None else False
