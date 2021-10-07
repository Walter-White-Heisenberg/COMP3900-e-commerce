from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import random
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BFP.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(200), nullable=False)
    nickname = db.Column(db.String(50))
    is_online = db.Column(db.Boolean)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    mobile = db.Column(db.String(20))

    def __init__(self, id_number, token, nickname, online, em, passw, addre, mobile):
        self.U_id = id_number
        self.token = token
        self.nickname = nickname
        self.is_online = online
        self.email = em
        self.password = passw
        self.address = addre
        self.mobile = mobile


class Search_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    history = db.Column(db.String(50), nullable=False)

    def __init__(self, U_id, history):
        self.U_id = U_id
        self.history = history


class Shopping_cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    P_id = db.Column(db.Integer, nullable=False)

    def __init__(self, U_id, P_id):
        self.U_id = U_id
        self.P_id = P_id


class Click_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    P_id = db.Column(db.Integer, nullable=False)
    times = db.Column(db.Integer, nullable=False)

    def __init__(self, U_id, P_id, times):
        self.U_id = U_id
        self.P_id = P_id
        self.times = times


class Purchase_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    p_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, U_id, p_id, quant):
        self.U_id = U_id
        self.p_id = p_id
        self.quantity = quant


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pro_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    if_shown = db.Column(db.Boolean)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    sold = db.Column(db.Integer)
    discount = db.Column(db.Float)
    tags = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __init__(self, pro_id, name, if_shown, price, stock, sold, discount, tags, description):
        self.pro_id = pro_id
        self.name = name
        self.if_shown = if_shown
        self.price = price
        self.stock = stock
        self.sold = sold
        self.discount = discount
        self.tags = tags
        self.description = description


class Reset_Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer)
    reset_code = db.Column(db.String(50))

    def __init__(self, U_id, reset_code):
        self.U_id = U_id
        self.reset_code = reset_code


# this method would generate a reset code
def create_Reset_Code(U_id, reset_code):
    rc = Reset_Code(U_id, reset_code)
    add_item(rc)


class Product_picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic_link = db.Column(db.String(50))
    pro_id = db.Column(db.Integer)

    def __init__(self, pic_link, pro_id):
        self.pic_link = pic_link
        self.pro_id = pro_id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reciever = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100))
    U_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    time = db.Column(db.String(20))
    address = db.Column(db.String(100))
    comment = db.Column(db.String(200))
    track_number = db.Column(db.String(100))

    def __init__(self, U_id, reciever, mobile, email, status, time, address, comment, track_number):
        self.U_id = U_id
        self.reciever = reciever
        self.mobile = mobile
        self.email = email
        self.status = status
        self.time = time
        self.address = address
        self.comment = comment
        self.track_number = track_number


class Order_products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    o_id = db.Column(db.Integer)
    p_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, o_id, p_id, quant):
        self.o_id = o_id
        self.p_id = p_id
        self.quantity = quant


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


db.create_all()


# this method would take all of the data in data.json into BFP.db
def load_data():
    with open('static/data.json') as json_file:
        data = json.load(json_file)
        for pro in data['products']:
            tags = ",".join(pro["usage"])
            tags = tags.replace(",Repay the teacher", '')
            create_product(pro["id"], pro["title"], True, pro["price"],
                           round(random.uniform(2, 4) * random.uniform(1, 2) * 100),
                           round(random.uniform(2, 4) * random.uniform(1, 2) * 100), 0, tags, pro["description"])
            for image in pro["image"]:
                create_product_picture(image.replace('/image/', '/img/'), int(pro["id"]))


# this method would be used when there is an item to be added into the database
def add_item(item):
    db.session.add(item)
    db.session.commit()


# address can be NULL at the beginning
# this method would generate a new user and add it to the database
def create_user(id_number, token, nickname, online, em, passw, addre, mobile):
    new_user = User(id_number, token, nickname, online, em, passw, addre, mobile)
    add_item(new_user)


# this method would generate a click history and add it to the database
def create_Click_history(U_id, p_id):
    ch = Click_history.query.filter_by(U_id=U_id, P_id=p_id).first()
    if ch is None:
        new_ph = Click_history(U_id, p_id, 1)
        add_item(new_ph)
    else:
        ch.times = ch.times + 1
        db.session.commit()


# this method would generate a search history and add it to the database
def create_Search_history(U_id, history):
    new_sh = Search_history(U_id, history)
    add_item(new_sh)


# can be NULL at the beginning
# this method would generate a order and add it to the database
def create_order(id_number, recieve_name, mobile, email, status, time, address, comment, track_number):
    new_order = Order(id_number, recieve_name, mobile, email, status, time, address, comment, track_number)
    add_item(new_order)


# this method would generate a product and add it to the database
def create_product(id_number, name, if_shown, price, stock, sold, discount, tags, desciprtion):
    new_product = Product(id_number, name, if_shown, price, stock, sold, discount, tags, desciprtion)
    add_item(new_product)


# this method would generate a product-picture relation and add it to the database
def create_product_picture(pic_link, pro_id):
    new_pic_pro = Product_picture(pic_link, pro_id)
    add_item(new_pic_pro)


# this method would generate a order-products relation and add it to the database
def create_op(o_id, p_id, quant):
    new_op = Order_products(o_id, p_id, quant)
    add_item(new_op)


# if purchase history with u_id, p_id alrady exist, then only the quantity will increase
# else this method would generate a purchase history and add it to the database
def create_Purchase_history(u_id, p_id, quant):
    ph = Purchase_history.query.filter_by(U_id=u_id, p_id=p_id).first()
    if ph is None:
        new_ph = Purchase_history(u_id, p_id, quant)
        add_item(new_ph)
    else:
        ph.quantity = ph.quantity + quant
        db.session.commit()


# this method would generate a admin and add it to the database
def creatte_admin(em, passs):
    new_adm = Admin(em, passs)
    add_item(new_adm)


# this method would find the product_picture by the product id
# it would return the list of the picture link
def find_pics(pr_id):
    l_of_link = []
    pics = Product_picture.query.filter_by(pro_id=pr_id).all()
    for p in pics:
        if(p.pic_link[0] != "/"):
            l_of_link.append("/"+p.pic_link)
        else:
            l_of_link.append(p.pic_link)
    return l_of_link


# this method would find the product by the product id
# it would return the list of the products
def find_usages(id):
    product = Product.query.filter_by(pro_id=id).first()
    return product.tags.split(",")


# this method would put the product information into a dict
# it would return the generated dict
def product_to_dict(product):
    pics = find_pics(product.pro_id)
    usages = find_usages(product.pro_id)
    return {
        "title": product.name,
        "price": product.price,
        "product_ID": product.pro_id,
        "image": pics,
        "stock": product.stock,
        "discount": product.discount,
        "usage": usages,
        "description": product.description,
        "is_visible": product.if_shown}


# this method would put the product information into a dict by the order
# it would return the generated dict
def order_to_dict(order):
    user = User.query.filter_by(U_id=order.U_id).first()
    ops = Order_products.query.filter_by(o_id=order.id).all()
    products = []
    prods = []
    quantity = []
    for op in ops:
        pro = Product.query.filter_by(pro_id=op.p_id).first()
        products.append(pro)
        quantity.append(op.quantity)
    for p in products:
        prods.append(product_to_dict(p))
    return {"order_ID": order.id,
            "customer": user_to_dict(user),
            "product": prods,
            "quantity": quantity,
            "phone": order.mobile,
            "email": order.email,
            "address": order.reciever + "\nat\n" + order.address,
            "status": order.status,
            "track_number": order.track_number}


# this method would put the user information into a dict by the user
# it would return the generated dict
def user_to_dict(user):
    orders = Order.query.filter_by(U_id=user.U_id).all()
    o_ids = []
    for order in orders:
        o_ids.append(order.id)
    o_ids.sort(reverse=True)
    return {"id": user.U_id, "address": user.address, "orders": o_ids, "name": user.nickname,
            "email": user.email, "phone": user.mobile}


# this method would get the product by id
# it would return the product
def getProductById(id):
    return Product.query.filter_by(pro_id=int(id)).first()
