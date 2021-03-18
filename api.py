
from flask import Flask, jsonify, request
from mysql_connect import fetch_from_database
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "g8@)#Eh?AufQv#Z@#(76*gsd,s`,z"  #IDC if you are seeing thins...
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():  

    username = request.json.get("username")
    password = request.json.get("password")
    
    logging.debug("New login request from username", username)

    db_result = fetch_from_database("SELECT * FROM users WHERE username=\'" + username + "\' AND password_hash=\'" + password +'\';')
    print(db_result)
    if len(db_result) == 0:
        return jsonify(status=False)

    access_token = create_access_token(identity=username)
    return jsonify(status=True, token=access_token)

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    logging.debug("New register request for username", username)

    commit_to_database("INSERT INTO users (username, password) VALUES (%s, %s)", ("'"+username+"'", "'"+password+"'"))
    return jsonify(status=True)
    
app.run()