from flask_wtf import FlaskForm
from wtforms import SubmitField

class ReturnItemForm(FlaskForm):
    submit = SubmitField(label="Return Item")