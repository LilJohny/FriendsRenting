from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class ReturnPresentForm(FlaskForm):
    present_id = IntegerField('Present id', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        return True if self.present_id.data is not None else False
