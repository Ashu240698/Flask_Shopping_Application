from flask_package import db
from flask_package import bcrypt
from flask_package import login_manager
from flask_login import UserMixin
from flask_package.models import UserModel
from flask import flash

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Product_Name = db.Column(db.String(length=50), nullable=False, unique=True)
    Quantity = db.Column(db.Integer(), nullable=False)
    Price = db.Column(db.Integer(), nullable=False)
    Description = db.Column(db.String(length=200), nullable=False)
    # Owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    User_ID = db.relationship('User', secondary=UserModel.UserItemLinkTable.__table__, backref='items', lazy=True)

    def __repr__(self):
        return self.Product_Name
    
    def buyItem(itemObject, User):
        if itemObject.Quantity > 0:
            if itemObject.Price <= User.Budget:
                # itemObject.Owner = User.id
                User.Budget -= itemObject.Price
                itemObject.Quantity -= 1
                User.itemCount += 1
                item1 = db.session.query(Item).filter(Item.id==itemObject.id).first()
                item1.User_ID.append(User)
                print("item1 in buy func: {}".format(item1))
                print("item1.user_ID.append(user): {}".format(item1))
                print("user object in buy function: {}".format(User))
                db.session.commit()
            else:
                flash(message="Insufficient budget.", category="danger")
        else:
            flash(message="Selected item is out of stock.", category="danger")

    def sellItem(sellItemObject, User):
        print("Selling item id: {}".format(sellItemObject.id))
        print("Item id in sell func: {}".format(Item.id))
        sellItemObject.Quantity += 1
        User.Budget += sellItemObject.Price
        print("user: {}".format(User))
        userLinkObj = db.session.query(UserModel.UserItemLinkTable).filter(UserModel.UserItemLinkTable.userId==User.id).first()
        print("deleteStmt: {}".format(userLinkObj))
        db.session.delete(userLinkObj)
        print(UserModel.UserItemLinkTable.userId)
        User.itemCount -= 1
        db.session.commit()


    def load_database():
        db.drop_all()
        db.create_all()

        
        item1 = Item(Product_Name="Google Chromebook", Quantity=4, Price=600, Description="Google Chromebook is a laptop. with 12GB RAM, 1 TB hard disk, 40x5cm display.")
        item2 = Item(Product_Name="HP Laptop", Quantity=4, Price=800, Description="HP is a laptop. with 8GB RAM, 1 TB hard disk, 40x5cm display.")
        item3 = Item(Product_Name="Apple MacBook", Quantity=1, Price=1200, Description="Apple MacBook is a laptop. with 4GB RAM, 500 GB hard disk, 40x5cm display.")
        item4 = Item(Product_Name="Samsung S24", Quantity=1, Price=1200, Description="Samsung S24 is a mobile phone product. with 12GB RAM, 128 GB ROM, 6.5inch display, GPS.")
        user1 = UserModel.User(username = 'Ashutosh', email_address = 'ashu@gmail.com', password='Ashu@123456')
 
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.add(user1)
  
        db.session.commit()

  


