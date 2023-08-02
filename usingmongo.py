import certifi
import flask
from flask import Flask
from pymongo import MongoClient
from pymongo.errors import BulkWriteError


app = Flask(__name__)
client = MongoClient("mongodb+srv://basitabass27411:iamahacker313@baiq.o4c0pn6.mongodb.net/?retryWrites=true&w=majority", tlsCAFile = certifi.where())

database = client['my_database']
coll = database['collection']

@app.route('/')
def home():
    todos = coll.find()
    return flask.jsonify([todo for todo in todos])

@app.route('/add_one')
def add_one():
    coll.insert_one({'title':"function", "todo body":"gtting ready for khalid bayas marriage"})
    return flask.jsonify(message = "success")

@app.route('/add_many')
def add_many():
    coll.insert_many([
        {'_id': 1, 'title': 'Study', "todo body": "studying for at-least 3 hours in morning"},
        {'_id': 2, 'title': 'food', "todo body": "food in the afternoon"},
        {'_id': 3, 'title': 'playing', "todo body": "playing in te evening"},
        {'_id': 4, 'title': 'Study', "todo body": "studying for at-least 3 hours in late night"}

    ])
    return "done inserting in the database"

@app.route('/add_unique_many')
def add_unique_many():
    try:
        coll.insert_many([
            {'_id': 1, 'title': 'Study', "todo body": "studying for at-least 3 hours in morning"},
            {'_id': 2, 'title': 'food', "todo body": "food in the afternoon"},
            {'_id': 3, 'title': 'playing', "todo body": "playing in te evening"},
            {'_id': 4, 'title': 'Study', "todo body": "studying for at-least 3 hours in late night"},
            {'_id': 5, 'title': 'sleep', 'todo body': 'sleeping for 8 hours'},
            {'_id': 6, 'title': 'exercise', 'todo body': 'exercise for 2 hours'}
        ], ordered=False)
    except BulkWriteError as e:
        return flask.jsonify(message = "duplicates encountered and ignored",
                             details = e.details,
                             inserted = e.details['nInserted'],
                             duplicates = [x['op'] for x in e.details['writeErrors']])

    return flask.jsonify(message = "success")

@app.route("/get_todo/<int:todoId>")
def insert_one(todoId):
    todo = coll.find_one({"_id": todoId})
    return todo

@app.route("/replace_todo/<int:todoId>")
def replace_one(todoId):
    result = database.coll.replace_one({'_id': todoId}, {'todo body': 'lunch in the afternoon'})
    return "updated"

@app.route('/new_replace/<int:todoId>')
def new_replace(todoId):
    todo = coll.find_one_and_replace({'_id': todoId}, {'todo body': 'lunch in the afternoon'})
    return todo

@app.route('/update_one/<int:todoId>')
def update_one(todoId):
    result = coll.update_one({'_id': todoId}, {'$set': {'todo body': 'exercise for 3 hours in the morning'}})
    return "updated"

@app.route('/new_update/<int:todoId>')
def new_update(todoId):
    result = coll.find_one_and_update({'_id': todoId}, {'$set':{'todo body': 'sleeping for 4 hours only now'}})
    return result

@app.route('/delete_todo/<int:todoId>')
def delete_one(todoId):
    todo = coll.find_one_and_delete({'_id': todoId})
    if todo is not None:
        return todo
    return "Id does not exist"





if __name__ == "__main__":
    app.run(debug=True)


