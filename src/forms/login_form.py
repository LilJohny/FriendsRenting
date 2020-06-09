from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    mail = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_on_submit(self):
        return True if self.mail.data is not None and self.password.data is not None else False
