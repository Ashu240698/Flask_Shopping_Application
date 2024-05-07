from flask_package import db
from flask_package import bcrypt
from flask_package import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserItemLinkTable(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    itemId = db.Column('item_id', db.ForeignKey('item.id'))
    userId = db.Column('user_id', db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=80), nullable=False)
    Budget = db.Column(db.Integer(), nullable=False, default=10000)
    # items= db.relationship('Item', backref='owned_user', lazy=True)
    itemCount = db.Column(db.Integer(), nullable=False, default=0)
    Item_ID = db.relationship('Item', secondary=UserItemLinkTable.__table__, backref='users', lazy=True)



    @property
    def display_budget(self):
        if len(str(self.Budget)) > 4:
            return '{},{}$'.format(str(self.Budget)[:-3], str(self.Budget)[-3:]) 
        else:
            return '{}$'.format(str(self.Budget))  


    
    @property
    def password(self):
        self.paasword

    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf-8')

    
    def validate_password(self, password_to_be_checked):
        if bcrypt.check_password_hash(self.password_hash, password_to_be_checked):
            return True
    

    def __repr__(self):
        return '{}, {}, {}'.format(self.username, self.email_address, self.Budget)