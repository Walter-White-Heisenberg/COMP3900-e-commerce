from db import *
from user_function import *
from admin_function import *
from json import dumps
import random
import wikipedia

welcome_mode = 0
recommendation = 1
search_mode = 2
detail_recommendation = 3
user_detail = 4
user_status = {}    

welcome = "Hi, I'm chatbot for Blue five petal, my job is to help you get the information of our store, products and ----happiness."
confuse = "sorry, I can't understand your response"
start_question = "Type 0 anytime to restart the conversation again from beginning <br>Type 1 if you want to get BFP recommended product <br>type 2 if you wanna search a certain product <br>Type 3 if you want to tell us about person who you want to buy flower for and we can tell you which are best for him/her <br>Type 4 to know user detail"
word_list = ["cock", "scum", "piss", "drop dead","jerk off", "get lost", "@$$hole", "81tch", "fuccckkkk", "niggger", "Bich", "fack off", "suk my dik", "fuck", "dick", "bitch", "nigger", "asshole", "pussy", "whole", "stupid", "dump", "shit", "slut", "sissy"]
greeting_word_list = ["hi ", "hello", "nice to meet", "how are you", "hi,", "hi ,"]
discount_list = ["discount of ", "discounts of" , "discount about "]
discount = ["'s discount", "s discount"]
people = ["girlfriend", " gf ", "gf ", "mom", "mother", "father", "dad", "teacher"]
price_list =  ["price of ", "cost of ", "value of ", "prices of ", "costs of ", "values of ","price about ", "cost about ", "value about "]
usage_list = ["usage of ", "category of ", "tag of ", "usages of ", "categories of ", "tags of ", "categorys of "]
description_list = ["information of ", "desciption of ", "detail of ", "informations of ", "desciptions of ", "details of "]
random_chosen = ["Interesting","maybe you should type 0 to restart","How do you feel when you say that?", "Let's change focus a bit... Tell me about your family.", "Can you elaborate on that?", "Let's change focus a bit... Tell me about your family.", "How does that make you feel?"]
ask_yourself = ["how many", "how much", "why", "how could", "what is", "what are", "what will", "when could"]
your_opinion = ["why did you say", "what 's your opinion about ", "I want to know your thought about"]
love_term = ["love you", "in love with you", "like you"]
gratitute = ["thank", "THX", "thks"]
#前后端链接的时候可以用不同的数字的代表不同的类型
def product_with_name_exist(name):
    products = Product.query.filter_by().all()
    for p in products:
        if p.name.lower().replace(' ', '') == name.lower().replace(' ', ''):
            return p
    return None
def try_to_search(product_keyword):
    product_dict = find_product_by_tags_or_name(product_keyword, None, "both", True)
    if len(product_dict['products']) == 0:
        return {'response': random_chosen[random_product_id(7, 1)[0]], 'products': []}
    return {'response': "We found those products you might be interested", 'products': product_dict['products'][:14]}

def find_discount(product_name):
    product = product_with_name_exist(product_name)
    if product == None:
        return try_to_search(product_name)
    return {'response': "discount of " + product.name + " is $" + str(product.discount), 'products': []}

def find_price(product_name):
    product = product_with_name_exist(product_name)
    if product == None:
        return try_to_search(product_name)
    return {'response': "price of " + product.name + " is $" + str(product.price), 'products': []}

def find_usage(product_name):
    product = product_with_name_exist(product_name)
    if product == None:
        return try_to_search(product_name)
    return {'response': "usage of " + product.name + " is " + product.tags.replace(',', ' <br>'), 'products': []}

def find_description(product_name):
    product = product_with_name_exist(product_name)
    if product == None:
        return try_to_search(product_name)
    return {'response': "description of " + product.name + " is " + product.description, 'products': []}

def basic_process(msg):
    msg = msg.lower()
    for word in discount_list:
        if word in msg:
            return find_discount(msg.split(word)[-1])
    for word in price_list:
        if word in msg:
            return find_price(msg.split(word)[-1])
    for word in usage_list:
        if word in msg:
            return find_usage(msg.split(word)[-1])
    for word in description_list:
        if word in msg:
            return find_description(msg.split(word)[-1])
    return None

def daily_detect(context):
    context = context.lower()
    for word in greeting_word_list:
        if word in context:
            return True
    return False

def offensive(context):
    for word in word_list:
        if word in context:
            return True
    return False

def daily_mode(context):
    low_ver = context.lower()
    if low_ver == "hi" or daily_detect(low_ver) == True:
        return  {'response': "hello, nice to meet you", "products" : []}
    if low_ver == "no" or low_ver == "nope":
        return  {'response': "please tell me why", "products" : []}
    if "haha" in low_ver or "hhh" in low_ver:
        return  {'response': "hahahaha", "products" : []}
    if "how old are you" in low_ver:
        return  {'response': "less than 1 year", "products" : []}
    for word in love_term:
        if word in low_ver:
            return {'response': "me too", "products" : []}
    for word in gratitute:
        if word in low_ver:
            return {'response': "my pleasure", "products" : []}
    for word in people:
        if word in low_ver:
            return {'response': "Do you want to buy flowers for your " + word.replace(' ', '') + "? type 2 or 3 to search the flower.", "products" : []}
    for word in ask_yourself:
        if word in low_ver:
            low_ver.replace(word, '')
            wiki_search = wikipedia.search(context, results=5) 
            if wiki_search == None:
                return  {'response': "sorry, I m just a chatbot, the question is too hard", "products" : []}
            else :
                result_str = 'I found foolowing result on wiki: <br>'
                for term in wiki_search:
                    result_str = result_str + "https://en.wikipedia.org/wiki/" + term + " <br>"
                return  {'response': result_str, "products" : []}
    #print("1231231231")
    x = round(random.uniform(2, 6) * random.uniform(3, 9))
    if x < 25 or len(context.split(' ')) < 2:
        return_msg = your_opinion[random_product_id(3, 1)[0]] + '"' + context.split(' ')[-1] + '"'
    else:
        return_msg = random_chosen[random_product_id(7, 1)[0]]
    #print("asdfasdfasdfasdf")
    return  {'response': return_msg, "products" : []}
    
    int_to_cate = {
            '1': "Love flowers",
            '2': "Friendship flowers",
            '3': "Birthday flowers",
            '4': "Greeting flowers",
            '5': "Repay the teacher",
            '6': "Visiting and condolences",
            '7': "Apology flowers",
            '8': "Wedding flowers"}
def get_order_detail(id, token):
    id = int(id)
    order = Order.query.filter_by(id = id).first()
    
    user = User.query.filter_by(token = token).first()
    orders = Order.query.filter_by(U_id = user.U_id).all()
    if order == None or user.U_id != order.U_id:
        return None
    result_str = "order status: " + order.status + " <br>order time : " + order.time
    result_str = result_str + " <br>order address : " + order.address
    result_str = result_str + " <br>your written comment' : " + order.comment
    result_str = result_str + " <br>reciever's name : " + order.reciever
    result_str = result_str + "<br>more detail about product are in your acct page"
    return result_str

def get_user_detail(token):
    user = User.query.filter_by(token = token).first()
    result_str = "your acct name: " + user.nickname + " <br>your email : " + user.email
    result_str = result_str + " <br>your address : " + user.address
    result_str = result_str + " <br>your mobile' : " + user.mobile
    return result_str


def logic(token, msg):  
    x = basic_process(msg)
    if x != None:
        return x
    if msg == '':
        return {'response': "Say something my friend", 'products': []}
    empty_status = {"status": welcome_mode, "categories" : None, "lower_bound" : None, "higher_bound": None, "search_term": None, "detail_status" : None}
    if token not in user_status:
        #print("1searchhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        user_status[token] = empty_status
    if msg == str(welcome_mode) and user_status[token]['status'] != detail_recommendation:
        #print("2searchhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        user_status[token] = empty_status
        return {'response': welcome + start_question, 'products': []}
    #print("#####****************", user_status[token]['status'] == welcome_mode, msg , ",,,,,,,,,,,", search_mode)
    if user_status[token]['status'] == welcome_mode:
        if msg == str(recommendation):
            product_dict = guess(token)
            user_status[token]['status'] = welcome_mode
            return {'response': "We found those 20 products you might be interested", 'products': product_dict['products']}
        elif msg == str(search_mode):
            #print("3searchhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            user_status[token]['status'] = search_mode
            return {'response': "Please type in the keyword you want to search", 'products': []}
        elif msg == str(detail_recommendation):
            user_status[token]['status'] = detail_recommendation
            ask_detail = "please type in your usage of flower <br>Please type icorresponding number, if you want to have multiple category then use comma to connnect them (like 1,4,6,8) <br>1 for Lover, 2 for friendship, 3 for Birthday, 4 for greeting, 5 for Teacher, 6 for Visiting, 7 for Apology, 8 for Wedding"
            return {'response': ask_detail, 'products': []}
        elif msg == str(user_detail):
            user = User.query.filter_by(token = token).first()
            if user == None:#or user.is_online == False
                #print(user == None)
                user_status[token]['status'] = empty_status
                return {'response': "you need to log in first", 'products': []}
            user_status[token]['status'] = user_detail
            return {'response': "please type 'order' to know order detail, or type 'myself' to know your detail", 'products': []}
    if user_status[token]['status'] == search_mode:
        product_dict = find_product_by_tags_or_name(msg, None, "both", False)
        user_status[token]['status'] = welcome_mode
        if len(product_dict['products']) == 0:
            return {'response': "sorry we didn't found any thing <br>Restarting conversation... <br>" + start_question, 'products': []}
        return {'response': "We found those products you might be interested", 'products': product_dict['products'][:10]}
    elif user_status[token]['status'] == detail_recommendation:
        if user_status[token]['categories'] == None:
            categories = msg.replace(' ', '')
            inp = categories.split(',')
            x = 0
            p_list = []
            for num in inp:
                if len(num) != 1 or ord(num) < ord('0') or ord(num) > ord('8'):
                    x = 1
            if x == 1:
                return_msg = "sorry, wrong input detected, input should be in form '1,2,4' etc, please try again or type 0 to restart<br>"
            else :
                user_status[token]['categories'] = categories
                return_msg = "categories detected, please type the lowest price you are comfortale with  (can't be smaller than 1)"
            return {'response': return_msg, 'products': []}
        elif user_status[token]['lower_bound'] == None:
            if msg.isdecimal == False:
                return_msg = "sorry, wrong input detected, please try again"
            elif float(msg) <= 0 or float(msg) >= 100000:
                return_msg = "nice joke, please try again"
            else :
                user_status[token]['lower_bound'] = msg
                return_msg = "price detected, please type the highest price you are comfortale with"
            return {'response': return_msg, 'products': []}
        elif user_status[token]['higher_bound'] == None:
            product_dict = []
            if msg.isdecimal == False:
                return_msg = "sorry, wrong input detected, please try again"
            elif float(msg) < 1 or float(msg) >= 100000:
                return_msg = "nice joke, please try again"
            elif float(msg) < float(user_status[token]['lower_bound']):
                return_msg = "I think "+ msg + " < " + user_status[token]['lower_bound'] + ", please try again"
            else :
                product_dict = sort_by_case(6, user_status[token]['lower_bound'], msg, user_status[token]['categories'])
                return_msg = "price detected, hopefully you will like the result"
                user_status[token] = empty_status
            return {'response': return_msg, 'products': product_dict['products'][:5]}
    elif user_status[token]['status'] == user_detail:
        if msg == "order":
            user_status[token]['detail_status'] = "waiting"
            return {'response': "please type in your order's id", 'products': []}
        elif msg == "myself":
            user_status[token] = empty_status
            return {'response': get_user_detail(token), 'products':[]}
        else :            
            if user_status[token]['detail_status'] == "waiting":
                if msg.isdecimal() == False:
                    return {'response': "ID need to be a number, please try again or type 0 to restart", 'products': []}
                order_detail = get_order_detail(msg, token)
                if get_order_detail(msg, token) == None:
                    return {'response': "Invalid order ID, please try again or type 0 to restart", 'products': []}
                user_status[token] = empty_status
                return {'response': order_detail, 'products': []}
            else :
                return {'response': "Type 'order' to know order detail, or type 'myself' to account detail <br>Or type 0 to restart conversation", 'products': []}
    if offensive(msg) == True: 
        user_status[token] = empty_status
        return {'response':"ohh, that's some inappropriate things to say when you buy flower", 'products' : []}
    else :
        x = daily_mode(msg)
        #print("ggggggggg", x)
        return x      
#logic if 0 then restart, check for 1 2 3 response
def chatbot(token, msg):
    try:
        return logic(token, msg)
    except:
        return {'response':"Some unexpected thing happen，please type 0 to restart", 'products' : []}
    

        

    
    
    
