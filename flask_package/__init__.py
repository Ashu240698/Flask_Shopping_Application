from flask import Flask, make_response
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
print(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'SECRET_KEY' #Without this line --> RuntimeError: A secret key is required to use CSRF.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# db.init_app(app)
app.app_context().push()

login_manager.login_view = 'displayLoginPage'
login_manager.login_message_category = 'info'

from flask_package.Routes import flask_routes
