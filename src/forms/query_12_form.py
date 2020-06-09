from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class Query12Form(FlaskForm):
    friend_id = IntegerField('Friend id', validators=[DataRequired()])
    rents = IntegerField('Rents', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('Start date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_end_date(self, field):
        field = field.data
        start_date = self.start_date.data
        difference = (field - start_date).days
        return difference > 0

    def validate_on_submit(self):
        return True if self.friend_id.data is not None and self.rents.data is not None \
                       and self.start_date.data is not None and self.end_date.data is not None else False
