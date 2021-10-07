import db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from db import *
import random


def init():
    for i in range(0,15):
        create_Purchase_history(round(random.uniform(0,3)), round(random.uniform(0,100)), round(random.uniform(0,200)))

def drop():
    for i in range(0,15):
        create_Click_history(round(random.uniform(0,3)), round(random.uniform(0,100)))

def draw_a_graph_for_the_product_purchased_quantity():
    product_purchase_his = Purchase_history.query.filter_by().all()
    products_dict = {}
    for i in product_purchase_his:
        if i.p_id in products_dict.keys():
            products_dict[i.p_id] = products_dict[i.p_id] + i.quantity
        else :
            products_dict[i.p_id] = i.quantity
    sortedClassCount = sorted(products_dict.items(), key=lambda d: d[1], reverse=True)
    x_names = []
    y_value = []
    for i in range(0, 6):
        x_names.append(sortedClassCount[i][0])
        y_value.append(sortedClassCount[i][1])
    x_pos = range(len(x_names))
    plt.bar(x_pos, y_value, align='center', alpha=0.8, edgecolor="black", width=0.4)
    for a, b in zip(x_pos, y_value):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)

    plt.xticks(x_pos, x_names)
    plt.ylabel('Sold')
    plt.title('Sold Quantity Analytic')
    plt.savefig("static/image/analytic/quantity.png")
    plt.clf()

def draw_a_graph_for_stock():
    products = Product.query.filter_by().all()
    products_dict = {}
    for product in products:
        products_dict[str(product.pro_id)] = product.stock
    sortedClassCount = sorted(products_dict.items(), key=lambda d: d[1], reverse=True)
    x_names = []
    y_value = []
    for i in range(0, 10):
        x_names.append(sortedClassCount[i][0])
        y_value.append(sortedClassCount[i][1])
    x_pos = range(len(x_names))
    plt.bar(x_pos, y_value, align='center', alpha=0.4, edgecolor="black", width=0.4)
    for a, b in zip(x_pos, y_value):
        plt.text(a, b + 0.01, '%.0f' % b, ha='center', va='bottom', fontsize=10)

    plt.xticks(x_pos, x_names)
    plt.ylabel('Stock')
    plt.title('stock Analytic')
    plt.savefig("static/image/analytic/stock.png")
    plt.clf()

def draw_a_graph_for_clicks():
    clicks = Click_history.query.filter_by().all()
    products_dict = {}
    for i in clicks:
        pro = Product.query.filter_by(pro_id=i.P_id).first()
        if pro.pro_id in products_dict.keys():
            products_dict[pro.pro_id] = products_dict[pro.pro_id] + i.times
        else :
            products_dict[pro.pro_id] = i.times
    sortedClassCount = sorted(products_dict.items(), key=lambda d: d[1], reverse=True)
    x_names = []
    y_value = []
    for i in range(0, 10):
        x_names.append(sortedClassCount[i][0])
        y_value.append(sortedClassCount[i][1])
    x_pos = range(len(x_names))
    plt.bar(x_pos, y_value, align='center', alpha=0.8, edgecolor="black", width=0.4)
    for a, b in zip(x_pos, y_value):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.xticks(x_pos, x_names)
    plt.ylabel('Click')
    plt.title('Clicked-counting Analytic')
    plt.savefig("static/image/analytic/click.png")
    plt.clf()
 

def graph_generated():
    draw_a_graph_for_the_product_purchased_quantity()
    draw_a_graph_for_stock()
    draw_a_graph_for_clicks()
graph_generated()

