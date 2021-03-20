
from flask import Flask, jsonify, request
from mysql_connect import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "g8@)#Eh?AufQv#Z@#(76*gsd,s`,z"  #IDC if you are seeing thins...
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():  
    username = request.json.get("username")
    password = request.json.get("password")
    
    app.logger.debug("New login request from username "+username)

    db_result = fetch_from_database_values("SELECT * FROM users WHERE username=%s AND password_hash=%s;", (username, password))
    if len(db_result) == 0:
        return jsonify(status=False)

    access_token = create_access_token(identity=username)
    return jsonify(status=True, exp=15, token=access_token)

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    logging.debug("New register request for username", username) 
    db_result = fetch_from_database_values("SELECT * FROM users WHERE username=%s;", (username,))
    if db_result != None and len(db_result) > 0: 
        return jsonify(status=False)

    commit_to_database_values("INSERT INTO users (username, password_hash) VALUES (%s, %s);", (username, password))
    return jsonify(status=True)

if __name__ == "__main__":
    app.run()