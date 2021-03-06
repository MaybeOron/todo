from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from flask_pymongo import PyMongo
import os
from pymongo import MongoClient
#from bson import ObjectId

app = Flask(__name__, template_folder='static')

client = MongoClient("mongodb://mongo:27017/tododb")
db = client['tododb']
todo = db['tododb']
#db = client.tododb
#app.config["MONGO_URI"] = "mongodb://mongo:mongo@mongo:27017/tododb"
#mongo = PyMongo(app)
#db = mongo.db

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def todo():
    _items = db.tododb.find()
    items = [ item for item in _items]
    return render_template("todo.html",items=items)


@app.route('/new' ,methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'description':request.form['description']
    }
    db.tododb.insert_one(item_doc)
    return redirect(url_for('todo'))

# #@app.route("/delete/<name>", methods=["DELETE"])
# @app.route("/delete/<id>", methods=["GET"])
# def delete_task(id):
#     #response = db.task.delete_one({"name":name})
#     response = db.task.delete_one({"_id": ObjectId(id)})
#     if response.deleted_count:
#         message = "Task deleted successfully!"
#     else:
#         message = "No Task found!"
#     return jsonify(
#         message=message
#     )



if __name__ == '__main__':
    app.run(debug=True)
