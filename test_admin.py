import sys
import db
from json import dumps
from datetime import datetime
import time
import uuid
import re
import hashlib
# from flask_cors import CORS
from flask import Flask, request, jsonify
from db import *
from user_function import *
import os
from admin_function import *

def drop_order():
    for i in Order.query.all():
        print(i.U_id)
        db.session.delete(i)
        db.session.commit()
    for i in Order_products.query.all():
        db.session.delete(i)
        db.session.commit()
    for i in User.query.all():
        print(i.U_id)
        db.session.delete(i)
        db.session.commit()
def order_test():
    #db.drop_all()
    #db.create_all()
    token_str = encode({"id":1})
    #create_user(10000, '1234567', 'nickname', False, "Phranqueli@gmail.com", "123123", "123123", '0405075066')
    create_user(0, get_token(0), "Yun Li", False, "Phranqueli@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address 20 Ocean Street SYDNEY NSW 2000", "(02) 8649 1522")
    create_user(1, get_token(1), "Haowei Lou", False, "louhaowei@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address 8 Hideaway Cl, Narangba, QLD 4504", "(02) 9522 6439")
    create_user(2, get_token(2), "Yan Yan", False, "yanyan@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address 62 Edward St, Sylvania, NSW 2224", "(07) 3886 8073")
    print(User.query.first().U_id)

    create_order(0, "Yun Li", "0456456456", "Phranqueli@gmail.com", 'paid', '2021/08/30', 'Street Address 20 Ocean Street SYDNEY NSW 2000', 'Good', 'None')
    create_order(1, "Haowei Lou", "0456458886", "louhaowei@gmail.com", 'cancelled', '2021/08/31', 'Street Address 8 Somali Cl, Diamond Creek, VIC 3089', 'No problem', 'None')
    create_order(2, "Yan Yan", "0456787856", "yanyan@gmail.com", 'paid', '2021/08/31', 'Street Address 1 Schouten Crs, Swansea, TAS 7190', 'Good website', 'None')
    create_op(1, 3, 20)
    create_op(2, 7, 11)
    create_op(2, 9, 1)
    create_op(3, 19, 4)

    print(admin_orders_result(token_str))

def conversion_from_dict():
    #db.drop_all()
    #db.create_all()
    #load_data()
    token_str = encode({"id":1})

    
    create_op(1, 123, 998)
    create_op(0, 123, 778)
    create_op(1, 111, 321)
    print(Product.query.filter_by(pro_id = 123).first())
    print(admin_orders_result(token_str))
def print_o():
    for i in Order.query.all():
        print(i.id, "  3333333  ", i.U_id)
    for i in User.query.all():
        print(i.U_id)
def init():
    for i in range(0,15):
        create_Purchase_history(round(random.uniform(0,3)), round(random.uniform(0,100)), round(random.uniform(0,200)))

def drop():
    for i in range(0,15):
        create_Click_history(round(random.uniform(0,3)), round(random.uniform(0,100)))
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    load_data()
    #drop_order()
    order_test()  
    conversion_from_dict()
    print_o()
    init()
    drop()
    

