import mysql.connector
import logging

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


def fetch_from_database(query : str) -> tuple:
    try:
        mydb.ping(reconnect=True, attempts=1, delay=0)
        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug("Succusfuly fetched data from the database")
        return result
    except Exception as ex:
        logging.error("Failed to fetch the database "+str(ex))
        return  None

def fetch_from_database_values(query : str, values : tuple) -> tuple:
    try:
        mydb.ping(reconnect=True, attempts=1, delay=0)
        cursor.execute(query, values)
        result = cursor.fetchall()
        logging.debug("Succusfuly fetched data from the database")
        return result
    except Exception as ex:
        logging.error("Failed to fetch the database "+str(ex))
        return  None

def commit_to_database_values(query : str, values : tuple):
    try:
        mydb.ping(reconnect=True, attempts=1, delay=0)
        cursor.execute(query, values)
        mydb.commit()
        logging.debug("Succusfuly commited to the database")

    except Exception as ex:
        logging.error("Failed to commit to the database "+str(ex))

def commit_to_database(query : str):
    try:
        mydb.ping(reconnect=True, attempts=1, delay=0)
        cursor.execute(query)
        mydb.commit()
        logging.debug("Succusfuly commited to the database")

    except Exception as ex:
        logging.error("Failed to commit to the database "+str(ex))

if __name__ == "__main__":
    '''
    commit_to_database_values("""INSERT INTO users (username, password_hash, 1_1, 1_2, 1_3, 1_4, 1_5, 1_6, 1_7, 1_8, 1_9, 1_10, 1_11, 1_12, 2_1, 2_2, 2_3, 2_4,
        2_5, 2_6, 2_7, 2_8, 2_9, 2_10, 2_11, 2_12, 3_1, 3_2, 3_3, 3_4, 3_5, 3_6, 3_7, 3_8, 3_9, 3_10, 3_11, 3_12, 4_1, 4_2, 4_3, 4_4, 4_5, 4_6, 4_7, 4_8, 4_9, 4_10,
        4_11, 4_12, 5_1, 5_2, 5_3, 5_4, 5_5, 5_6, 5_7, 5_8, 5_9, 5_10, 5_11, 5_12, 6_1, 6_2, 6_3, 6_4, 6_5, 6_6, 6_7, 6_8, 6_9, 6_10, 6_11, 6_12, is_admin) VALUES (%s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", ("tomer", "7ec72f22806b02797e66bfe2cf0ce5585c9dae59b7125b41efa1bb9eae32f66d", '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'))
    '''
    db_result = fetch_from_database_values("SELECT * FROM users WHERE username=%s AND password_hash=%s;", ("tomer", "55eea69fbcc97f88dc0843cb70d4b260f6139b530674d322dbea1bd4993bc907"))
    print(db_result)
    

            