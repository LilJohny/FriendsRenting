from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class HireFriendForMeetingForm(FlaskForm):
    friend_id = IntegerField('Friend id', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        return True if self.friend_id.data is not None else False
