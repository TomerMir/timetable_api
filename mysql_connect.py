import mysql.connector
import logging

mydb = None
cursor = None

def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MirmoDB2004",
            database="timetable_database"
        )
        logging.info("Connected to database")
        cursor = mydb.cursor()
        logging.debug("Got cursor")

    except:
        logging.critical("Failed to connect to the database")
        exit()

connect_to_database()

def ping_database():
    if(not mydb.is_connected()):
        connect_to_database()


def fetch_from_database(query : str) -> tuple:
    try:
        ping_database()
        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug("Succusfuly fetched data from the database")
        return result
    except Exception as ex:
        logging.error("Failed to fetch the database "+str(ex))
        return  None

def fetch_from_database_values(query : str, values : tuple) -> tuple:
    try:
        ping_database()
        cursor.execute(query, values)
        result = cursor.fetchall()
        logging.debug("Succusfuly fetched data from the database")
        return result
    except Exception as ex:
        logging.error("Failed to fetch the database "+str(ex))
        return  None

def commit_to_database_values(query : str, values : tuple):
    try:
        ping_database()
        cursor.execute(query, values)
        mydb.commit()
        logging.debug("Succusfuly commited to the database")

    except Exception as ex:
        logging.error("Failed to commit to the database "+str(ex))

def commit_to_database(query : str):
    try:
        ping_database()
        cursor.execute(query)
        mydb.commit()
        logging.debug("Succusfuly commited to the database")

    except Exception as ex:
        logging.error("Failed to commit to the database "+str(ex))

if __name__ == "__main__":
    db_result = fetch_from_database_values("SELECT * FROM users WHERE username=%s;", ("tomer",))
    db_result = list(db_result[0])[3:]
    print(len(db_result))
    print(db_result)
    

            