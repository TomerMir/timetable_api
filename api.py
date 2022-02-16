from flask import Flask, jsonify, request
import flask
from mysql_connect import Database
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, verify_jwt_in_request
from flask_cors import CORS
import logging
import sys
import argparse
import os
import datetime

try: 
    #Setup flask app and CORS (Cross-origin resource sharing)
    app = Flask(__name__)
    CORS(app)

    #Setup the server loggers
    werkzeugLogger = logging.getLogger('werkzeug')
    werkzeugLogger.setLevel(logging.ERROR)

    app.logger.handlers = []

    logging.root.handlers = []
    logging.basicConfig(filename="timetable_api.log",
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='"%Y-%m-%d %H:%M:%S"',
                                level=logging.INFO)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    app.logger.addHandler(console)
    logger = logging

    # Setup the jwt
    path = "jwt_secret_key"
    if os.path.exists(path):
        with open(path ,'r') as f:
            app.config["JWT_SECRET_KEY"] = f.read()
            logger.debug("Succusfully loaded the jwt key")

    else:
        import random
        import string
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        with open(path ,'w+') as f:
            f.write(key)
        app.config["JWT_SECRET_KEY"] = key
        logger.debug("Created new jwt key")

    jwt = JWTManager(app)

    #Database initialization
    database = Database("localhost", "root", "MirmoDB2004", "timetable_database", logger)

except Exception as ex:
    logging.fatal("Error while setting up the server: "+ str(ex))
    exit()


#Login
@app.route("/api/login", methods=["POST"])
def login():  
    try:
        username = request.json.get("username")
        password = request.json.get("password")
        stayLoggedIn = request.json.get("stayLoggedIn")

        logger.info("New login request from "+username)
        db_result = database.fetch_from_database_values("SELECT * FROM users WHERE username=%s AND password_hash=%s;", (username, password))
        if len(db_result) == 0:
            return jsonify(status=False, err="Incorrect username or password")
        admin = db_result[0][-1] == 1
        if stayLoggedIn:
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=username, additional_claims={"admin" : admin}, expires_delta=expires)
            return jsonify(status=True, exp=525600, token=access_token)

        expires = datetime.timedelta(minutes=15)
        access_token = create_access_token(identity=username, additional_claims={"admin" : admin}, expires_delta=expires) 
        return jsonify(status=True, exp=15, token=access_token)

    except Exception as e:
        logger.error("Error at login " + str(e))
        return jsonify(status=False, err="Server error")

#Register new user
@app.route("/api/register", methods=["POST"])
def register():
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        logger.info("New register request for "+username) 
        
        db_result = database.fetch_from_database_values("SELECT * FROM users WHERE username=%s;", (username,))
        if db_result != None and len(db_result) > 0: 
            return jsonify(status=False, err="Username already taken, try another one...")

        database.commit_to_database_values("""INSERT INTO users (username, password_hash, 1_1, 1_2, 1_3, 1_4, 1_5, 1_6, 1_7, 1_8, 1_9, 1_10, 1_11, 1_12, 2_1, 2_2, 2_3, 2_4,
            2_5, 2_6, 2_7, 2_8, 2_9, 2_10, 2_11, 2_12, 3_1, 3_2, 3_3, 3_4, 3_5, 3_6, 3_7, 3_8, 3_9, 3_10, 3_11, 3_12, 4_1, 4_2, 4_3, 4_4, 4_5, 4_6, 4_7, 4_8, 4_9, 4_10,
            4_11, 4_12, 5_1, 5_2, 5_3, 5_4, 5_5, 5_6, 5_7, 5_8, 5_9, 5_10, 5_11, 5_12, 6_1, 6_2, 6_3, 6_4, 6_5, 6_6, 6_7, 6_8, 6_9, 6_10, 6_11, 6_12) VALUES (%s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (username, password, '0',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '0', '0', '0'))

        return jsonify(status=True)
    
    except Exception as e:
        logger.error("Error at register " + str(e))
        return jsonify(status=False, err="Server error")

#JWT invalid route
@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify(status=False, err="Invalid token")

#JWT expired route
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(status=False, err="Token expired")

#Get the timetable
@app.route("/api/gettable", methods=["GET"])
@jwt_required()
def get_table():
    try:
        username = get_jwt_identity()
        logger.info("Get table request from "+ username) 
        db_result = database.fetch_from_database_values("SELECT * FROM users WHERE username=%s;", (username,))
        db_result = list(db_result[0])[3:]
        del db_result[-1]
        return jsonify(status=True, data=db_result)
    except Exception as e:
        logger.error("Error at get_table " + str(e))
        return jsonify(status=False, err="Server error")

#Change the timetable
@app.route("/api/changetable", methods=["POST"])
@jwt_required()
def edit_table():
    try:
        username = get_jwt_identity()
        new_data = request.json.get("data")
        if new_data == []:
            return jsonify(status=True)
        logger.info("Change table request from "+ username) 
        query = "UPDATE users SET "
        for update_values in new_data:
            column = int(update_values[0]/12)+1
            row = update_values[0]%12+1
            query += str(column) + '_' + str(row) + '=%s, ' 
        query = query[:-2] +" WHERE username=%s;"
        values = map(lambda x: x[1], new_data)
        values = list(values)
        values.append(username)
        values = tuple(values)
        database.commit_to_database_values(query, values)
        return jsonify(status=True)
    except Exception as e:
        logger.error("Error at edit_table " + str(e))
        return jsonify(status=False)

#Verify if user is admin
def verify_admin(username):
    try:
        db_result = database.fetch_from_database_values("SELECT * FROM users WHERE username=%s;", (username,))
        return db_result[0][-1] == 1
    except Exception as e:
        logger.error("Error at verify_admin " + str(e))
        return False
    
#Get the users list
@app.route("/api/getusers", methods=["GET"])
@jwt_required()
def get_users():
    try:
        username = get_jwt_identity()
        logger.info("Get users request from "+ username) 
        if not verify_admin(username):
            return jsonify(status=False, err="You are not an admin")

        db_result = database.fetch_from_database("SELECT username, is_admin FROM users;")
        return jsonify(status=True, data=db_result, your_user=username)

    except Exception as e:
        logger.error("Error at get_users " + str(e))
        return jsonify(status=False, err="Server error")

#Change role for specific user
@app.route("/api/changeadmin", methods=["POST"])
@jwt_required()
def change_admin():
    try:
        username = get_jwt_identity()
        if not verify_admin(username):
            return jsonify(status=False, err="You are not an admin")
        user_to_change = request.json.get("username")
        logger.info("%s changed %s's role" % (username, user_to_change)) 
        if user_to_change == username:
            return jsonify(status=False, err="You can't change your own role")
        db_result = database.fetch_from_database_values("SELECT * FROM users WHERE username=%s;", (user_to_change,))
        if len(db_result) == 0:
            return jsonify(status=False, err="Username does not exist")
        if db_result[0][-1] == 1:
            database.commit_to_database_values("UPDATE users SET is_admin=%s WHERE username=%s;", (None, user_to_change))
        else:
            database.commit_to_database_values("UPDATE users SET is_admin=%s WHERE username=%s;", (1, user_to_change))

        return jsonify(status=True)

    except Exception as e:
        logger.error("Error at change_admin " + str(e))
        return jsonify(status=False, err="Server error")


#Delete user
@app.route("/api/deleteuser", methods=["POST"])
@jwt_required()
def delete_user():
    try:
        username = get_jwt_identity()
        if not verify_admin(username):
            return jsonify(status=False, err="You are not an admin")
        user_to_change = request.json.get("username")
        logger.info("%s deleted %s's account" % (username, user_to_change)) 
        if user_to_change == username:
            return jsonify(status=False, err="You can't delete your own user")
        db_result = database.fetch_from_database_values("SELECT * FROM users WHERE username=%s;", (user_to_change,))
        if len(db_result) == 0:
            return jsonify(status=False, err="Username does not exist")

        database.commit_to_database_values("DELETE FROM users WHERE username=%s;", (user_to_change,))
        return jsonify(status=True)    

    except Exception as e:
        logger.error("Error at delete_user " + str(e))
        return jsonify(status=False, err="Server error")


def main():
    try:
        parser = argparse.ArgumentParser("Timetable api server")
        parser.add_argument("debug", help="""1 for debug mode. 0 or none for production mode""",nargs='?', const=1, type=int, default=0)
        args = parser.parse_args()
        global logger
        if args.debug == 1:
            logger = app.logger
            database.set_logger(logger)
            app.run(host= '127.0.0.1', port=5000, debug=True)
        else:
            from waitress import serve
            serve(app, host='127.0.0.1', port=5000) 
    except Exception as e:
        logger.fatal("Error at main " + str(e) + "\nExiting...")
    finally:
        exit()

if __name__ == "__main__":
    main()


