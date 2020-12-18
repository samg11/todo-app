import pymongo
import secrets

cluster = pymongo.MongoClient(secrets.readSecret('dbConectionUri'))
db = cluster["users"]
collection = db["users"]

def authenticate(username, password):
    if username and password:
        user = collection.find( {"username":username} )[0]
        if secrets.decrypt(user["password"]) == password:
            return True
        else:
            return False

def username_taken(username):
    if collection.find({ "username":username }).count():
        return True
    else:
        return False

def add_user(username, password):
    collection.insert_one({
        "username": username,
        "password": secrets.encrypt(password),
        "todos":[]
    })

def account_creation_status(username, password):
    user = collection.find({ "username":username })[0]
    if secrets.decrypt(user['password']) == password:
        return "Account created successfully"
    else:
        return "There was an error creating your account, please try again"

def submit_todo(todo, username):
    collection.update(
        {"username":username},
        {"$push": { "todos": todo } }
    )

def get_todos(username):
    user = collection.find({"username":username})
    for i in user:
        return i

def remove_todo(todo, username):
    collection.update(
        {"username":username},
        { "$pull": { "todos":  todo} }
    )