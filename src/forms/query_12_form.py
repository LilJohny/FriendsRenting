from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class Query12Form(FlaskForm):
    friend_id = IntegerField('Friend id', validators=[DataRequired()])

    submit = SubmitField('Submit')

    def validate_on_submit(self):
        return True if self.friend_id.data is not None else False
