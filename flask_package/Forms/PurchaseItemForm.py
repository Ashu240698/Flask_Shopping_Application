from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_package.models.UserModel import User

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Confirm")
