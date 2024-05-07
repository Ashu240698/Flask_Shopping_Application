from flask_wtf import FlaskForm
from flask_package.models.UserModel import User
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required

class LoginForm(FlaskForm):

    # def validate_username(self, username_to_be_checked):
    #     user = User.query.filter_by(username=username_to_be_checked.data).first()
    #     if
    username = StringField(label="Username", validators=[input_required("Enter username")])
    password = PasswordField(label="Password", validators=[input_required("Enter password")])
    submit = SubmitField(label="Sign in")