from server import *
from admin_function import decode
#&Code for Haowei
def validToken(token):
    try:
        return decode(token)['id'] == 1
    except Exception:
        return False
    
@app.route('/admin',methods=['GET'])
def admin():
    return render_template("/Haowei/admin/admin_login.html")

@app.route('/admin_portal',methods=['GET'])
def admin_portal():
    token = request.args.get("token")
    print(token)
    if(validToken(token)):
        return render_template("/Haowei/admin/admin_portal.html")
    else:
        return render_template("/Haowei/admin/admin_login.html")

@app.route('/cart',methods=['GET'])
def cart():
    return render_template("/Haowei/cart.html")

@app.route('/productList',methods=['GET'])
def productList():
    token = request.args.get("token")
    products=[]
    products = (admin_products_result(token))['products']
    return render_template("/Haowei/admin/product_list.html",products=products)

@app.route('/checkout',methods=['GET'])
def checkout():
    return render_template("/Haowei/checkout.html")


@app.route("/manageProduct",methods=['GET'])
def manageProduct():
    token = request.args.get("token")
    id = request.args.get("id")
    product = {}
    if(id is not None):
        product = product_to_dict(getProductById(id))
    print(json.dumps(product,indent=4))
    print(product,"ssssssssssssssssssssssssss")
    return render_template("/Haowei/admin/manage_product.html",product=product)

@app.route('/customerList',methods=['GET'])
def customerList():
    token = request.args.get("token")
    customers = (admin_user_result(token))['customers']
    if(customers==[]):
        create_user(0, "13421234123412341234", "frank", False, "Phranqueli@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address111%%%Suburb111%%%Zip111%%%State111", "1339121234")
        create_user(1, "1342123412341234123412341234", "david", False, "Phranqueli123@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address222%%%Suburb222%%%Zip222%%%State222", "0455555666")
        create_user(2, "13421234123412341234123412341234", "tony", False, "Phranqueli14123@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address333%%%Suburb333%%%Zip333%%%State333", "0468987654")

    print(customers)
    #print(customers)
    '''test_data = {
        "id":0,
        "name": "haowei lou",
        "email": "louhaowei@gmail.com",
        "phone": "0406111111",
        "address":"Haymarkey, Sydney, 2000, NSW",
        "orders":["0"]
    }
    customers.append(test_data)'''
    return render_template("/Haowei/admin/customer_list.html",customers=customers)

@app.route('/manageCustomer',methods=['GET'])
def manageCustomer():
    token = request.args.get("token")
    id = request.args.get("id")
    user = User.query.filter_by(U_id = int(id)).first()
    customer = user_to_dict(user)

    return render_template("/Haowei/admin/manage_customer.html",customer=customer)

@app.route('/orderList',methods=['GET'])
def orderList():
    token = request.args.get("token")
    products=[]
    orders = (admin_orders_result(token))['orders']
    return render_template("/Haowei/admin/order_list.html",orders=orders)

@app.route('/manageOrder',methods=['GET'])
def manageOrder():
    token = request.args.get("token")
    id = request.args.get("id")
    order = (get_order(int(id)))['order']
    print(order)
    return render_template("/Haowei/admin/manage_order.html",order=order)

@app.route('/chatBot',methods=['GET'])
def chatBot():
    token = request.args.get("token")
    return render_template("/Haowei/bot.html")

@app.route('/adminAnalytic',methods=['GET'])
def adminAnalytic():
    token = request.args.get("token")
    graph_generated()
    return render_template("/Haowei/admin/admin_analytic.html")

#YanYan's code

@app.route('/',methods=['GET'])
def home():
    return render_template("/Yanyan/home.html")
    
#return login page
@app.route('/login',methods=['GET'])
def login():
    return render_template("/Yanyan/login.html")

@app.route('/register',methods=['GET'])
def register():
    return render_template("/Yanyan/register.html")

@app.route('/shop',methods=['GET'])
def shop():
    return render_template("/Yanyan/product.html")

@app.route('/product_detail',methods=['GET'])
def singleproduct():
    return render_template("/Yanyan/productDetail.html")

@app.route('/category',methods=['GET'])
def category():
    return render_template("/Yanyan/category.html")

@app.route('/mine',methods=['GET'])
def mine():
    return render_template("/Yanyan/mine.html")

'''@app.route('/cart',methods=['GET'])
def cart():
    return render_template("/Yanyan/cart.html")
'''
@app.route('/aboutUs',methods=['GET'])
def aboutUs():
    return render_template("/Yanyan/aboutUs.html")

@app.route('/myOrders',methods=['GET'])
def myOrders():
    return render_template("/Yanyan/myOrders.html")

