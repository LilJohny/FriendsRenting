from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired


class GivePresentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    friend_id = IntegerField('Friend id', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        return True if self.friend_id.data is not None and self.title.data is not None else False
