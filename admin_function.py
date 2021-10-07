import sys
from json import dumps
from datetime import datetime
import uuid
import re
import random
from os import path, mkdir, remove
from user_function import send_email
from db import *
import jwt

admin_acct = "1234567@q.com"
admin_pass = "1234567"

# admin login
# this method is used for admin login in the frontend
# return error and the reason if there are some problems
# return success if the operation success
def adminLogin(email, password):
    if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email.lower()):
        if email != admin_acct:
            return {"result": "ERROR", "reason": "Non-exist email"}
        if password == admin_pass:
            return {"token": encode({"id": 1})}
        return {"result": "ERROR", "reason": "Wrong password"}
    return {"result": "ERROR", "reason": "Invalid email"}


# this method would let admin see orders
# return error admin's token is wrong
# return the order list if the operation success
def admin_orders_result(token_str):
    if decode(token_str)['id'] != 1:
        return {"result": "ERROR", "reason": "user with token is not an admin"}
    else:
        orders = Order.query.all()
        return_list = []
        i = 0
        for order in orders:
            return_list.append(order_to_dict(order))
        return {"orders": return_list}


# let admin see products results
# return error admin's token is wrong
# return the products list if the operation success
def admin_products_result(token_str):
    if decode(token_str)['id'] != 1:
        return {"result": "ERROR", "reason": "user with token is not an admin"}
    else:
        products = Product.query.order_by(Product.pro_id).all()
        result = {"products": products}
        prods = [product_to_dict(i) for i in products]
        return {"products": prods}


# this method would find the products by product id for admin
# return error and the reason if there are some problems
# return the products list if the operation success
def find_prods(IDs):
    list_of_id = IDs.split(";")
    prods = []
    for ID in list_of_id:
        product = getProductById(ID)
        if product is None:
            return {"result": "ERROR", "reason": "id " + ID + " doesn't exist"}
        else:
            prods.append(product_to_dict(product))
    return {"products": prods}


# this method would find the products by product id for admin and then admin could update the information of product
# if product id == -1, we will create a new product
# return error admin's token is wrong
# return success if the operation success
def update_product(token, productId, newTitle, newDescription, newPrice, newQuantity, newcategory, newDiscount, images,
                   visible):
    if decode(token)['id'] != 1:
        return {"result": "ERROR", "reason": "user with token is not an admin"}
    if len(newTitle) > 50 or len(newTitle) == 0:
        return {"result": "ERROR", "reason": "newTitle should be between 1-1000 characters"}
    if len(newDescription) > 1000 or len(newDescription) == 0:
        return {"result": "ERROR", "reason": "desciption should be between 1-1000 characters"}
    if newPrice < 0:
        return {"result": "ERROR", "reason": "price need to be positive"}
    if newQuantity < 0:
        return {"result": "ERROR", "reason": "quantity need to be positive"}
    if newDiscount < 0:
        return {"result": "ERROR", "reason": "discount need to be positive"}
        # if id  ==  -1 then we are adding new product without any images
    if visible == "True":
        is_visible = True
    else:
        is_visible = False
    if int(productId) == -1:
        create_product(len(Product.query.all()), newTitle, is_visible, newPrice, newQuantity,
                       round(random.uniform(2, 4) * random.uniform(1, 2) * 100), newDiscount, newcategory,
                       newDescription)
        return {"result": "created success"}
    else:
        product = Product.query.filter_by(pro_id=int(productId)).first()
        if product is None:
            return {"result": "ERROR", "reason": "id " + productId + " doesn't exist"}

        # if there is less image than before , we will delete the reluctant image
        image_links = images.split(',')
        prod_pics = Product_picture.query.filter_by(pro_id=int(productId)).all()
        for prod_pic in prod_pics:
            if prod_pic.pic_link not in image_links:
                try:
                    remove(prod_pic.pic_link)
                    db.session.delete(prod_pic)
                    db.session.commit()
                except Exception:
                    db.session.delete(prod_pic)
                    db.session.commit()
        product.name = newTitle
        product.price = newPrice
        product.stock = newQuantity
        product.tags = newcategory
        product.description = newDescription
        product.discount = newDiscount
        product.if_shown = is_visible
        db.session.commit()
    return {"result": "updated success"}


# this method would find the user by user's token
# return error and the reason if there are some problems
# return the user's info if the operation success
def find_user_by_token(tk):
    user = User.query.filter_by(token=tk).first()
    if user is None:
        return {"result": "ERROR", "reason": "customer with token(" + tk + ") doesn't exist"}
    return dumps(user_to_dict(user))


# save image into folder with name "static\\image\\product_image\\input id"
# this method would save the image by its id
# return error admin's token is wrong
# return the success if the operation success
def save_image_by_id(token, image, Id):
    if  decode(token)['id'] != 1:
        return {"result": "ERROR", "reason": "user with token is not an admin"}
    prod = Product.query.filter_by(pro_id = int(Id)).first()
    if prod is None:
        return {"result": "ERROR", "reason": "id " + Id + " doesn't exist"}
    if(path.exists("static/img/product_image") == False):
        return {"result": "ERROR", "reason": "folder : /static/img/product_image" " doesn't exist"}
    image_path = "static/img/product_image/" + Id
    if path.exists(image_path) == False:
        mkdir(image_path)
    i = 0
    while path.exists(image_path + "/" + str(i) + ".jpg"):
        i = i + 1
    image_name = image_path + "/" + str(i) + ".jpg"
    with open(image_name,"wb") as f:
        f.write(image)
    create_product_picture(image_name, int(Id))
    return {"result": "SUCCESS","img_url": image_name}


# this method would check whether the user is admin or not
# return error admin's token is wrong
# return the user info in a list if the operation success
def admin_user_result(token):
    if decode(token)['id'] != 1:
        return {"result": "ERROR", "reason": "user with token is not an admin"}
    else:
        users = User.query.order_by(User.U_id).all()
        users_dicts = [user_to_dict(i) for i in users]
        return {"customers": users_dicts}


# this method would find the order by order id for admin and change the order status
# return error admin's token is wrong
# return success if the operation success
def change_order(token, order_id, new_status, shipping):
    if decode(token)['id'] != 1:
        return {"result": "ERROR", "reason": "user with token is not an admin"}
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return {"result": "ERROR", "reason": "can't find order with id " + order_id}

    if new_status != "cancelled" and new_status != "shipped" and new_status != "paid":
        return {"result": "ERROR", "reason": "wrong status,  must be shipped, paid or cancelled"}

    order.status = new_status
    order.track_number = shipping
    if new_status != "shipped":
        order.track_number = None
    else:
        message = """\
        fivebluepetals\n\n\n 
        Hi dear, \nThanks for buying our products\n
        It's a confirmation that your order with track_number """ + str(order.track_number) + """ is sent successfully\n
        your order id is """ + str(order.id + 10000) + "\n"
        # send_email(order.email, message)
    db.session.commit()
    return {"result": "SUCCESS"}


# assumption: token belongs to a existed user, product's quantity in order is less than its stock
# and product info is in form product1_id?product1_quantity,product2_id?product2_quantity....
# this method would find the products by product id for admin
# return error and the reason if there are some problems
# return success if the operation success
def complete_order(token, recieve_name, productInfo, shipping_address, billing_address, comment, mobile, email,
                   sender_name):
    user = User.query.filter_by(token=token).first()
    if user is None:
        return {"result": "ERROR", "reason": "can't find user with token"}
    if not mobile.isdecimal():
        return {"result": "ERROR", "reason": "mobile number must only include nubmer"}
    ps_info = productInfo.split(',')
    create_order(user.U_id, recieve_name, mobile, email, "paid", datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                 shipping_address, comment, None)
    user.address = billing_address
    db.session.commit()
    number_of_order = Order.query.count()
    ps_info.remove("")
    for info in ps_info:
        id_quant = info.split('?')
        id = int(id_quant[0])
        quant = int(id_quant[1])
        product = Product.query.filter_by(pro_id=id).first()
        if product is None:
            return {"result": "ERROR", "reason": "can't find product with id " + id}
        if product.stock < quant:
            return {"result": "ERROR", "reason": "not enough stock"}
        create_op(number_of_order, id, quant)
        create_Purchase_history(user.U_id, id, quant)
        product.stock = product.stock - quant
        clich_hist = Click_history.query.filter_by(U_id=user.id, P_id=product.pro_id).first()
        if clich_hist is not None:
            db.session.delete(clich_hist)
        db.session.commit()
    message = """\
    fivebluepetals\n\n\n 
    Hi dear """ + sender_name + """.\nThanks for buying our products\n
    It's a confirmation that you paid successfully\n
    your order id is """ + str(number_of_order + 10000) + """\n"""
    # send_email(email, message)
    return {"result": "SUCCESS"}


# this method would get the order by order id
# it would return a order's info
def get_order(id):
    id = int(id)
    order = Order.query.filter_by(id=id).first()
    return {"order": order_to_dict(order)}

def encode(data):
    return jwt.encode(data, "fivebluepetals", algorithm="HS256")


def decode(data):
    print(data)
    return jwt.decode(data, "fivebluepetals", algorithms=["HS256"])


