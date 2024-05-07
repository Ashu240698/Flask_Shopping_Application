from flask_wtf import FlaskForm
from flask_package.models.UserModel import User
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_be_checked):
        user = User.query.filter_by(username=username_to_be_checked.data).first()
        if user:
            raise ValidationError("Username already exists.")
    
    def validate_email_address(self, email_address_to_be_checked):
        emailAddress = User.query.filter_by(email_address=email_address_to_be_checked.data).first()
        if emailAddress:
            raise ValidationError("E-mail address already exists.")
        
    
    username = StringField(label='Username', validators=[Length(min=2, max=20), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Length(min=2), Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')