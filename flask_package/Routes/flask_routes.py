from flask_package import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_package.models import ItemModel, UserModel
from flask_package.Forms import PurchaseItemForm, register_form, LoginForm, ReturnItemForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func


# @app.route("/")
# def homePage():
#     return "<h1> Hello world!!!! </h1>"

# @app.route("/s")
# def displayString():
#     return render_template_string("This is just a string returning.")

# @app.route("/<name>")
# def displayName(name):
#     return "Hi {}".format(name)

@app.route("/")
@app.route("/index")
def hello():
    return render_template("index.html")


@app.route("/market", methods=['GET', 'POST'])
@login_required
def loadMarketPage():
    purchaseForm = PurchaseItemForm.PurchaseItemForm()
    returnForm = ReturnItemForm.ReturnItemForm()

    if request.method == 'POST':
        productName = request.form.get('itemPurchased')
        print(productName)
        productObject = ItemModel.Item.query.filter_by(Product_Name = productName).first()
        print(productObject)
        if productObject:
            print("Current usr before buying: {}".format(current_user))
            ItemModel.Item.buyItem(productObject, current_user)
             
        
        returnItemId = request.form.get('returnItem')
        print("Return id: {}".format(returnItemId))
        returnItemObject = ItemModel.Item.query.filter_by(id = returnItemId).first()
        print("Return Object: {}".format(returnItemObject))
        if returnItemObject:
            print("Current usr before selling: {}".format(current_user))
            ItemModel.Item.sellItem(returnItemObject, current_user)
            
        return redirect(url_for('loadMarketPage'))


    # if request.method == 'GET':
    #     items = Item.query.all()
    #     print("items: {}".format(items))
    #     returnItems = db.session.query(Item).select_from(UserItemLinkTable).join(User)
    #     print("Current user id: {}".format(current_user.id))
    #     print("UserItemLinkTable.itemId : {}".format(UserItemLinkTable.itemId))
    #     print("Return Items: {}".format(returnItems))
    #     # users = User.query.all()
    #     # print(items)
    #     # print(users)
    #     return render_template('market.html', items=items, returnItems=returnItems, purchaseForm=purchaseForm, returnForm=returnForm)

    # Testing code
    if request.method == 'GET':
        items = ItemModel.Item.query.all()
        print("items: {}".format(items))
        
        returnItems = db.session.query(ItemModel.Item).select_from(UserModel.User).join(UserModel.UserItemLinkTable).filter(ItemModel.Item.id==UserModel.UserItemLinkTable.itemId, UserModel.User.id==current_user.id).all()
        itemCountPerUser = db.session.query(UserModel.UserItemLinkTable.itemId, current_user.id, func.count(UserModel.UserItemLinkTable.userId)).group_by(UserModel.UserItemLinkTable.userId, UserModel.UserItemLinkTable.itemId).all()
        countList = []
        for tup in itemCountPerUser:
                for count in tup:
                    countList.append(count)
 
        for item_ID, user_ID, count in itemCountPerUser:
            print(item_ID)
            print(user_ID)
            print(count)

        print(countList)
        print("Current user id: {}".format(current_user.items))
        print("Item count: {} per userID: {}".format(itemCountPerUser, current_user.id))
        print("UserItemLinkTable.itemId : {}".format(UserModel.UserItemLinkTable.itemId))
        print("Return Items: {}".format(returnItems))
        # users = User.query.all()
        # print(items)
        # print(users)
        return render_template('market.html', items=items, returnItems=returnItems, purchaseForm=purchaseForm, returnForm=returnForm)
    

app.route('/allUsers')
def showAllUsers():
    # usersList = User.query.all()
    # print(usersList)
    return render_template('users.html')

@app.route('/register', methods=['POST', 'GET'])
def displayRegisterForm():
    form = register_form.RegisterForm()

    if form.validate_on_submit():
        userCreated = UserModel.User(username=form.username.data, email_address=form.email_address.data, password=form.password.data)
        db.session.add(userCreated)
        db.session.commit()
        login_user(userCreated)
        flash("Account created successfully. logged in as '{}'".format(userCreated.username), category="success")
        return redirect(url_for('loadMarketPage'))
        
    if form.errors != {}:
        for errMsg in form.errors.values():
            print("ERROR RAISED ----> {}".format(form.errors.values()))
            flash(errMsg, category='danger')
        return render_template('register.html', form=form)
  
    return render_template('register.html', form=form)



@app.route('/login', methods=['POST', 'GET'])
def displayLoginPage():
    form = LoginForm.LoginForm()

    if form.validate_on_submit():
        user = UserModel.User.query.filter_by(username=form.username.data).first()
        if user and user.validate_password(form.password.data):
            login_user(user)
            flash("Login susscessfull..", category='success')
            return redirect(url_for('loadMarketPage'))
        elif not user:
            flash("User does not exist. Try Sign Up", category="danger")
            return redirect(url_for('displayRegisterForm'))
        else:
            flash("Invalid username/password..!!", category="danger")
            return render_template('login.html', form=form)
        
    return render_template('login.html', form=form)



@app.route('/logout')
def logoutUser():
    logout_user()
    flash("User logged out successfully..!", category="info")
    return redirect(url_for('hello'))





    

