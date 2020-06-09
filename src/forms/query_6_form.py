from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired


class Query6Form(FlaskForm):
    submit = SubmitField('Submit')


    def validate_on_submit(self):
        return True if self.submit.data ==True else False
