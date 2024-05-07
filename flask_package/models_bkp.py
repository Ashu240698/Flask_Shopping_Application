from flask_package import db
from flask_package import bcrypt
from flask_package import login_manager
from flask_login import UserMixin
from flask import flash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=80), nullable=False)
    Budget = db.Column(db.Integer(), nullable=False, default=10000)
    items= db.relationship('Item', backref='owned_user', lazy=True)
    itemCount = db.Column(db.Integer(), nullable=False, default=0)
    itemId = db.relationship('Item', back_ref = 'owned_items', lazy=True)



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

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Product_Name = db.Column(db.String(length=50), nullable=False, unique=True)
    Quantity = db.Column(db.Integer(), nullable=False)
    Price = db.Column(db.Integer(), nullable=False)
    Description = db.Column(db.String(length=200), nullable=False)
    Owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return self.Product_Name
    
    def buyItem(itemObject, User):
        if itemObject.Quantity > 0:
            if itemObject.Price <= User.Budget:
                itemObject.Owner = User.id
                User.Budget -= itemObject.Price
                itemObject.Quantity -= 1
                User.itemCount += 1
                db.session.commit()
            else:
                flash(message="Insufficient budget.", category="danger")
        else:
            flash(message="Selected item is out of stock.", category="danger")

    def sellItem(sellItemObject, owner):
        sellItemObject.Quantity += 1
        owner.Budget += sellItemObject.Price
        sellItemObject.Owner = None
        User.itemCount -= 1
        db.session.commit()


    def load_database():
        db.drop_all()
        db.create_all()

        
        item1 = Item(Product_Name="Google Chromebook", Quantity=4, Price=600, Description="Google Chromebook is a laptop. with 12GB RAM, 1 TB hard disk, 40x5cm display.")
        item2 = Item(Product_Name="HP Laptop", Quantity=4, Price=800, Description="HP is a laptop. with 8GB RAM, 1 TB hard disk, 40x5cm display.")
        item3 = Item(Product_Name="Apple MacBook", Quantity=1, Price=1200, Description="Apple MacBook is a laptop. with 4GB RAM, 500 GB hard disk, 40x5cm display.")
        item4 = Item(Product_Name="Samsung S24", Quantity=1, Price=1200, Description="Samsung S24 is a mobile phone product. with 12GB RAM, 128 GB ROM, 6.5inch display, GPS.")
        user1 = User(username = 'Ashutosh', email_address = 'ashu@gmail.com', password='Ashu@123456')
 
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.add(user1)
  
        db.session.commit()

  


