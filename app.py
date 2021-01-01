import flask
from flask import Flask, redirect, render_template, request
from flask import Markup
import json
import sqlite3
import random
from flask_pymongo import pymongo
from bson.json_util import dumps, loads

ALLOWED_EXTENSIONS = set(['txt', 'html'])

client = pymongo.MongoClient(connection_to_mongo_atlas)
db = client.get_database('blog_api')
print(db)
user_collection = pymongo.collection.Collection(db, 'user_collection')
mm = db.db.collection
# nn = db.blog_api
# db.db.collection.insert_one({"name":"GDB"})
# db.blog_api.insert_one({"id_num":25600000 , "last_blog_name": "sample"})
app = Flask(__name__)

# Unfortunately for now, I am removing the feature of adding the blog page directly to the website. I will add the feature here, later for sure.
global_id_variable = 0
k = 0
id_val = 0
list_title = []
list_synopsis = []
list_file_name = []

def getting_last_id_of_blog():
    global k, global_id_variable, id_val
    id_val = db.db.collection.find({}, {'_id': '{$gt: 0}'})

    # global_id_variable = id_val['id_num'] + 1
    print(id_val)
    for m in id_val:
        print(m)
        k = m['_id']
        print(m)
        print(k)
    global_id_variable = k + 1
    print(global_id_variable)
    # print(list_synopsis)

def making_list_for_homepage():
    global list_title, list_synopsis, list_file_name
    list_synopsis = []
    list_title = []
    list_file_name = []
    all_val = db.db.collection.find({})
    for gg in all_val:
        print(gg['blog_title'])
        list_title.append(gg['blog_title'])
        list_synopsis.append(gg['synopsis'])
        list_file_name.append(gg['file_name'])


getting_last_id_of_blog()
##### No need of the function given below

#
# def updating_last_id_of_blog(last_blog_name):
#     global_id_variable
#     id_val = db.blog_api.find_one()
#     # k =
#     db.blog_api.update_one(id_val, {"$set": {"id_num": global_id_variable, "last_blog_name": last_blog_name}})


#I will try to create a redis database containing the last number of global_id_variable. This is so because heroku severs automatically shut down and thus, I need to preserve the ID number


# The function to generate a random key of more than 5 digits
m = 0
key_now = 0

def key_for_api():
    global m
    m = random.randint(10000, 99999999)
    return m

blog_data_list = []
def blog_info_list():
    global blog_data_list
    x = mm.find()
    json_data = dumps(list(x))
    print(json_data)
    blog_data_list.append(json_data)
    # print(blog_data_list[]['file_name'])


# client = pymongo.MongoClient("mongodb+srv://admin_user101:<password>@cluster0.xcgis.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test



@app.route('/')
@app.route('/home')
def home_func():
    # list_title = [id_val['blog_title'], id_val['synopsis']]
    making_list_for_homepage()
    ### We will access the mongoDB database here, retrieve the data as Json and then dump it on home page
    abcdefgh = Markup("<h1> Hello There </h1>")
    xyz = len(list_synopsis)
    return render_template('home_main.html', blog_title = list_title, blog_synopsis = list_synopsis, blog_data=[list_title, list_synopsis, list_file_name], xyz=xyz)



@app.route('/keyforapi/retrieve')
def key_for_upload():
    global key_now
    p = key_for_api()
    key_now = p
    print(key_now)
    return str(p)

# Sample variable for testing out HTML file read and display
sample_variable = 0

# The above variable needs to be deleted before final deployment




@app.route('/keyforapi/retrieve/<int:key_value>', methods=['GET', 'POST'])
def the_option_to_alter_json(key_value):
    global key_now, global_id_variable, sample_variable
    if key_value == key_now and key_now != 0:
        # The function and parameters to alter the MongoDB will come here
        print(key_now)
        print(key_value)
        if request.method == 'GET':
            getting_last_id_of_blog()
            getting_last_id_of_blog()
            return render_template('form_for_api_update.html')
        elif request.method == 'POST':
            admin_form_data = request.form
            admin_form_file_name = admin_form_data['file_name']
            print(admin_form_file_name)
            admin_form_blog_title = admin_form_data['blog_title']
            print(admin_form_blog_title)
            admin_form_author_name = admin_form_data['author_name']
            print(admin_form_author_name)
            admin_form_synopsis = admin_form_data['synopsis']
            print(admin_form_synopsis)

            # in the below commented lines, I was trying to add the feature of adding the file directly to the application website. For now I'm stripping the idea.
            # For now, the blog pages will be displayed directly from the templates directory on the Github.

            # blog_file = request.files['blog_file']
            # m = blog_file.filename
            # k = str(blog_file.read())
            # # k.decode('utf8')
            # k = k.replace('\n', '')
            # k = k.replace('\r', '')
            # k = k.replace('\b', '')
            # sample_variable = Markup(k)
            # print(k)
            # print(m)


            dict_of_form = {"_id": global_id_variable, "file_name": admin_form_file_name,"blog_title": admin_form_blog_title, "author_name": admin_form_author_name, "synopsis": admin_form_synopsis}
            # li_of_form_json = json.dumps(li_of_form)
            global_id_variable = global_id_variable + 1
            print(dict_of_form)
            # print(li_of_form_json)
            # db.db.collection.insert_one({li_of_form})

            db.db.collection.insert_one(dict_of_form)
            key_now = 0

            return "Form submission succesful. Make sure you put that HTML file in the Templates directory of the Github Repo"
    else:
        print(key_now)
        return "Don't be smart. You don't have access to that page"


# @app.route('/sample')
# def sample_function():
#     return render_template('sample_temp.html', abcdefg=sample_variable)


@app.route('/keyforapi/retrieve/<int:key_value>/current_json_data', methods=['GET'])
def current_json_data(key_value):
    blog_info_list()
    global key_now, blog_data_list
    if key_value == key_now:
        # x = mm.find()
        # json_data = dumps(list(x), indent=2)
        # print(json_data)
        # # for n in mm:
        # #     print(n)
        key_now = 0

        # return render_template('blog_data.html', blog_data = blog_data_list)
        return str(blog_data_list)
    else:
        return "bye"

@app.errorhandler(404)
def func_error(error):
    return "Error 404: Page not found"




if __name__ == '__main__':
    getting_last_id_of_blog()
    key_for_api()
    app.run(debug=True)
