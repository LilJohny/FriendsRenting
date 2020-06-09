from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class Query11Form(FlaskForm):
    min_friends_number = IntegerField('Min Friends number', validators=[DataRequired()])
    max_friends_number = IntegerField('Max Friends number', validators=[DataRequired()])

    submit = SubmitField('Submit')

    def validate_on_submit(self):
        return True if self.min_friends_number.data is not None \
                       and self.max_friends_number.data is not None else False
