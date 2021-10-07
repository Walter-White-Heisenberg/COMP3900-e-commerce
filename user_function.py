import sys
from datetime import datetime
import time
import uuid
import re
import hashlib
import random
# from flask_cors import CORS
from flask import Flask, request, jsonify
from db import *
import jwt
import regex
import smtplib
import socket
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr
from email.utils import formataddr


#####################################################################################
#                                                                                   #
#                               AUTHENTICATION FUNCTIONS                            #
#                                                                                   #
#####################################################################################
# REGISTRATION FUNCTION
# this method is used for the user register the frontend
# return error and the reason if there are some problems
# return success if the operation did successfully
def register(nickname, email, password, repeat_password, mobile):
    # Getting the email from server
    # CHECKS FOR INVALID INFORMATION BELOW
    result = valid_email(email)
    if result == -1:
        return {"result": "ERROR", "reason": "email already registered"}
    elif result == 0:
        return {"result": "ERROR", "reason": "Invalid email"}
    if not good_password(password):
        return {"result": "ERROR",
                "reason": "password must be between 5 and 50 characters, and contains number, capital letter and "
                          "lower case letter."}
    if password != repeat_password:
        return {"result": "ERROR", "reason": "password not match with repeat password"}

    password = hashpass(password)  # Hashing the password for storage
    users = User.query.all()
    u_id = 10000 + len(users)
    token = get_token(int(u_id))  # Getting token
    # Creating a user and setting variables of the user
    create_user(u_id, token, nickname, False, email, password, None, mobile)
    message = """\
    fivebluepetals\n\n\n 
    Hi dear """ + nickname + """.\nThanks for registering in fivebluepetals.com\n
    It's a confirmation that you registered successfully\n"""
    #send_email(message, email)
    userr = u_id
    return {"customer": {'nickname': nickname, 'email': email, 'token': token}}


# this method is used for the user log in the frontend
# return error and the reason if there are some problems
# return success if the operation did successfully
def auth_login(em, input_password):
    # CHECKS FOR INVALID INFORMATION BELOW
    result = valid_email(em)
    if result == 1:
        return {"result": "ERROR", "reason": "Email is not registered."}
    elif result == 0:
        return {"result": "ERROR", "reason": "Invalid Email."}
    # Finding u_id associated with token
    user = User.query.filter_by(email=em).first()
    # Checking matching passwords
    input_password = hashpass(input_password)
    if input_password != user.password:
        return {"result": "ERROR", "reason": "Password is incorrect."}

    user.is_online = True  # Setting state to logged in
    db.session.commit()
    return {"token": user.token, "userInfo": {
        "name": user.nickname,
        "id": user.U_id,
        "mobile": user.mobile,
        "password": user.password,
        "email": user.email
    }}


# this method is used for the user log out the frontend
# return error and the reason if there are some problems
# return success if the operation did successfully
def auth_logout(token, user):
    user = user = User.query.filter_by(token=token)  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return {"result": "ERROR", "reason": "there is no user corresponding to token"}
    if user.state == 2:  # If user is already logged out
        return {"result": "ERROR", "reason": "user is already logged out"}
    user.is_online = False  # Changing the user's state to logged out
    return {"result": "success"}


# this method would find the picture by the category
# it would return the products contains input category
def find_pic_by_category(category):
    return find_product_by_tags_or_name(category, None, "category", True)


# this method would find the picture by the keyword tags or name
# it would return the products contains input keyword or similar to input result
def find_pic_by_keywork(keyword, token):
    return find_product_by_tags_or_name(keyword, token, "keyword", False)


# this method would helps the user to change the password
# return error and the reason if there are some problems
# return success if the operation did successfully
def auth_passwordreset_request(token):
    # email = str(request.args.get("email"))
    user = User.query.filter_by(token=token).first()
    if user is None:
        return {"result": "ERROR", "reason": "can't find user with token."}
    reset_code = gen_reset_code()

    # Sending reset code to user by email
    # N: If this errors, this will be picked up by the error handler and an error will be shown
    msg = "Five Pedals RESET PASSWORD\n\n\nYou've requested to reset your password. Your reset code is : \n" + str(
        reset_code)
    create_Reset_Code(user.U_id, reset_code)
    #send_email(msg, user.email)
    return {"status": "success"}



# if we put category name, then the method would return a dict for the frontend
def get_product_information_by_category(categories):
    products = Product.query.all()
    return_list1 = []
    for pro in products:
        if categories in pro.tags:
            return_list1.append(pro)
    product_dicts = []
    for i in return_list1:
        product_dicts.append(product_to_dict(i))
    return {"products": product_dicts}



# this method is for sorting the products in the shop-all
# it would return product list by different number
'''
1 : A-Z
2 : Z-A
3 : price high to low
4 : price low to high
5 : stock low to high
6 : stock high to low
'''
def sort_by_case(case, low, high, categories):
    case = int(case)
    low = int(low)
    high = int(high)
    products = []
    prods = []
    if high < low:
        return {"result": "ERROR", "reason": "the upper bond should be lower than lower bound."}
    if case == 0:
        products = Product.query.all()
    if case == 1:
        products = Product.query.order_by(Product.name, Product.stock).all()
    if case == 2:
        products = Product.query.order_by(Product.name.desc(), Product.stock).all()
    if case == 3:
        products = Product.query.order_by(Product.price.desc(), Product.stock).all()
    if case == 4:
        products = Product.query.order_by(Product.price, Product.stock).all()
    if case == 5:
        products = Product.query.order_by(Product.stock, Product.price.desc()).all()
    if case == 6:
        products = Product.query.order_by(Product.stock.desc(), Product.price.desc()).all()
    if case > 6 or case < 0:
        return {"result": "ERROR", "reason": "Number is not valid."}
    for i in products:
        if i.if_shown == True and high >= i.price >= low and include_category(i, categories) is True:
            prods.append(product_to_dict(i))
    return {"products": prods}


# this method would get all of the products
# it would return list including all of the products
def get_all():
    return_list1 = []
    prods = Product.query.all()
    for p in prods:
        return_list1.append(p)
    product_dicts = [product_to_dict(i) for i in return_list1]
    return {"products": product_dicts}


# this method would obtain one product ID and get the product in our database
# return the product with this id
def get_prod_by_id(ID, token):
    id = int(ID)
    user = User.query.filter_by(token=token).first()
    if user is not None:
        c_h = Click_history.query.filter_by(U_id=user.U_id, P_id=id).first()
        if c_h is None:
            create_Click_history(user.U_id, id)
    return {"products": [product_to_dict(Product.query.filter_by(pro_id=id).all()[0])]}


# this method would be used in the admin recommendation in the frontend
# it would return a collection of products recommended by the admin
def admin_recommend():
    return get_product_information_by_category("Recommend")


# this method would add the product into the cart
# it would return the status of the operation, like status or error
def add_to_cart(productINFO):
    id_quant = productINFO.split('?')
    id = int(id_quant[0])
    quant = int(id_quant[1])
    product = Product.query.filter_by(pro_id=id).first()
    if product.stock < quant:
        return {"result": "ERROR", "reason": "not enough stock"}
    return {"result": "success"}


# if customer viewed this item before, there is higher possibility that the product get recommended
# if customer searched related term before, there will also be higher possibility that the product get recommended
# but not high as click history
# product with more stock will get recommended with higher possibility
# it would return the collection of products for the products recommended
def guess(token):
    user = User.query.filter_by(token=token).first()
    products = Product.query.order_by(Product.stock.desc()).all()
    length = len(products)
    product_list = []
    if user is None:
        list_of_id = random_product_id(length, 20)
        while len(list_of_id) > 0:
            number = list_of_id.pop(0)
            for p in products:
                if p.pro_id == number:
                    product_list.append(p)
    else:
        p_favor = {}
        i = length
        u_id = user.U_id
        for p in products:
            fav_num = i * 10 / length
            if if_user_viewed(u_id, p.pro_id):
                fav_num = fav_num + 30
            fav_num = fav_num + num_search_to_favor(user.U_id, p.name, p.tags)
            p_favor[p] = fav_num
            i = i - 1
        product_list = sorted(p_favor, key=p_favor.get, reverse=True)[:20]
    dict_list = []
    for p in product_list:
        dict_list.append(product_to_dict(p))
    return {"products": dict_list}



# this one if for the user to view his/her orders in the frontend after he/she purchased a item
# return error and the reason if there are some problems
# return a product list if the operation did successfully
def users_orders(token):
    if token is None:
        return {"result": "ERROR", "reason": "invalid token."}
    user = User.query.filter_by(token=token).first()
    if user is None:
        return {"result": "ERROR", "reason": "invalid token."}
    orders = Order.query.all()
    return_list = []
    i = 0
    for order in orders:
        if order.U_id == user.U_id and "cancel" not in order.status:
            return_list.append(order_to_dict(order))
    return {"orders": return_list}



# this method would check whether the email is valid or invalid
# return 1 is the email is not in use
# return -1 if the email is existing
# return 0 if the email is invalid
def valid_email(em):
    low_em = em.lower()
    if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', low_em):
        user = User.query.filter_by(email=em).first()
        if user is None:
            return 1  # email not in use
        else:
            return -1  # returns -1 for existing email
    else:
        return 0  # returns 0 for invalid email


# we encode the password by hashlib to protect the password safety
# it would return the generated password
def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()


# we use a jwt way to create a token for the user by algorithm HS256
# this would be taken as a user id in the system
# it would return the generated token
def get_token(u_id):
    curr_time = datetime.now()
    token = jwt.encode({"u_id": u_id, "time": curr_time.isoformat()}, 'fivebluepetals', algorithm='HS256')
    return token


# this would generate a reset_code for the user to use
# it would return the generated code
def gen_reset_code():
    reset_code = uuid.uuid4().hex
    return reset_code


# check whether the password contains: 1.numbers 2. lower word 3. capital word
# Then we check the length of the password.
# Then return the boolean indicate if a passowrd is a good password
def good_password(password):
    decimal = 0
    lower = 0
    higher = 0
    length = 0
    for i in password:
        x = ord(i)
        length = length + 1
        if ord('0') <= x <= ord('9'):
            decimal = decimal + 1
        elif ord('a') <= x <= ord('z'):
            lower = lower + 1
        elif ord('A') <= x <= ord('Z'):
            higher = higher + 1

    if length < 5 or length > 50:
        return False
    if lower == 0 or higher == 0 or decimal == 0:
        return False
    return True


# this method is for user to change their profile
# return error and the reason if there are some problems
# return success if the operation did successfully
def edit_profile(email, password, nickname, token, mobile, reset_code):
    user = User.query.filter_by(token=token).first()
    if not mobile.replace('(', '').replace(')', '').replace('（', '').replace('）',
                                                                             '').isdecimal():  # If there is no user
        # corresponding to token
        return {"result": "ERROR", "reason": "mobile should only contain number"}
    result = valid_email(email)
    if result == 0:
        return {"result": "ERROR", "reason": "Invalid email"}
    if len(nickname) < 1 or len(nickname) > 50:
        return {"result": "ERROR", "reason": "nickname must be between 1 and 50 characters."}
    user.nickname = nickname
    user.mobile = mobile
    db.session.commit()
    if reset_code is not None:
        if not check_reset(user.U_id, reset_code):
            return {"result": "ERROR", "reason": "incorrect reset_code, please generate again."}
        elif not good_password(password):
            return {"result": "ERROR",
                    "reason": "password must be between 1 and 50 characters and contaings number, capital letter and "
                              "lower case letter."}
        user.email = email
        user.password = hashpass(password)
        db.session.commit()
    return {"result": "success"}


# this method would generate random product id for use
# it would return the generated id
def random_product_id(length, n):
    i = 0
    l_of_id = []
    while i != n:
        x = round(random.uniform(1, length) * random.uniform(1, length) * random.uniform(1, length) * random.uniform(1,
                                                                                                                     length)) % length
        if x not in l_of_id:
            l_of_id.append(x)
            i = i + 1
    return l_of_id


# this method is used when the user wants to reset the password
# it would return False if the code is None
# return True if the operation did successfully
def check_reset(id, code):
    if code is None:
        return False
    user_reset = Reset_Code.query.filter_by(U_id=id, reset_code=str(code)).first()
    if user_reset is None:
        return False
    db.session.delete(user_reset)
    db.session.commit()
    return True


# this method would check whether the product is viewed by the user
# if the user viewed then return 1
# else return 0
def if_user_viewed(U_id, P_id):
    c_h = Click_history.query.filter_by(U_id=U_id, P_id=P_id).first()
    if c_h is None:
        return False
    return True


# we would generate a number by calculating the user history and predict how much a user like a product user
# return a integer, the higher integer means the more a user like it
def num_search_to_favor(U_id, p_name, p_tag):
    count_keyword = 0
    count_category = 0
    historys = Search_history.query.filter_by(U_id=U_id).all()
    for history in historys:
        if history.history in p_name:
            count_keyword = count_keyword + 1
        elif history.history in p_tag:
            count_category = count_category + 1

    return count_category * 3 + count_keyword * 6


# for user safety, we would encode the user address
# this would return the address string after encode
def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


# thia one would send the email
# we currently using yun li's gmail
def send_email(content, reciever_email):
    from_email = "w17a.credible4@gmail.com"
    from_email_pwd = "Frank19981229"
    smtp_server = "smtp.gmail.com"
    msg = MIMEText("<html><body><h3>hello</h3><p>" + content + "</p></body></html>", "html", "utf-8")
    msg["From"] = format_addr("%s" % from_email)
    msg["To"] = format_addr("%s" % reciever_email)
    msg["Subject"] = Header("python email", "utf-8").encode()
    socket.getaddrinfo('127.0.0.1', 5000)
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_email, from_email_pwd)
    text = msg.as_string()
    server.sendmail(from_email, reciever_email, content)
    server.quit()


# this method would find the products by the keyword tags or name
# return error and the reason if there are some problems
# type can be both, keyword or category. both means either contains keyword or contain category
# clear_search indicate if we are gonna append unclear_result after the clear results search
# return searched products
def find_product_by_tags_or_name(keyword, token, type, clear_search):
    if token is not None and type == "keyword":
        user = User.query.filter_by(token=token).first()
        if user is not None:
            create_Search_history(user.U_id, keyword)
    list_of_id = []
    second_similar = []
    prods = Product.query.all()
    for p in prods:
        if type == "keyword":
            term = p.name
        elif type == "both":
            term = p.tags + p.name
        else:
            term = p.tags
        if p.if_shown == True and keyword in term:
            list_of_id.append(p)
        elif p.if_shown == True and unclear_search(keyword, p.name):
            second_similar.append(p)
    product_dicts = []
    for p in list_of_id:
        product_dicts.append(product_to_dict(p))
    for p in second_similar:
        product_dicts.append(product_to_dict(p))
    return {"products": product_dicts}



# this method would check whether the product have one of the categories
# if it contains one or more it would return 1
# otherwise it would return 0
def include_category(product, categories):
    if categories == '' or categories == ',':
        return True
    int_to_cate = {
        '1': "Love flowers",
        '2': "Friendship flowers",
        '3': "Birthday flowers",
        '4': "Greeting flowers",
        '5': "Congratulations flowers",
        '6': "Visiting and condolences",
        '7': "Apology flowers",
        '8': "Wedding flowers"
    }
    cs = categories.split(",")
    pcs = product.tags.split(",")
    for pc in pcs:
        for c in cs:
            if int_to_cate[c] == pc:
                return True
    return False

# this method would be used for the chatbot for unclear search
# like schol it would still gets school
# it would return the Boolean value depends on whether target can be regex searched by search_term
def unclear_search(search_term, target):
    target = target.lower()
    search_term = search_term.lower()
    result = regex.search(r'(%s){e<=1}' % search_term, target)
    return result