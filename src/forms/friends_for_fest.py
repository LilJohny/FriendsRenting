from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired


class HireFriendsForFestForm(FlaskForm):
    friends_id = StringField('Friends id', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        return True if self.friends_id.data is not None  else False
