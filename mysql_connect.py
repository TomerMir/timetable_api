import mysql.connector
import logging
import threading
import time

logger = logging

def set_logger(other_logger):
    global logger
    logger = other_logger

class Database:

    def __init__(self, host : str, user : str, password : str, database: str) -> None:
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            logger.info("Connected to database")
            self.cursor = self.mydb.cursor()
            self.cursor.reset()
            logger.debug("Got cursor")
            self.start_ping_thread()

        except Exception as ex:
            logger.critical("Failed to connect to the database" + str(ex))
            exit()

    def start_ping_thread(self):
        self.ping_thread = threading.Thread(target=self.ping)
        self.ping_thread.start()
        logger.debug("Started ping thread")

    def ping(self):
        while True:
            try:
                self.cursor.execute("SELECT 1;")
            except Exception as ex:
                logger.error("Failed to ping database" + str(ex))
            time.sleep(120)

    def fetch_from_database(self, query : str) -> tuple:
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            logger.debug("Succusfuly fetched data from the database")
            return result
        except Exception as ex:
            logger.error("Failed to fetch the database "+str(ex))
            return  None

    def fetch_from_database_values(self, query : str, values : tuple) -> tuple:
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchall()
            logger.debug("Succusfuly fetched data from the database")
            return result
        except Exception as ex:
            logger.error("Failed to fetch the database "+str(ex))
            return  None

    def commit_to_database_values(self, query : str, values : tuple):
        try:
            self.cursor.execute(query, values)
            self.mydb.commit()
            logger.debug("Succusfuly commited to the database")

        except Exception as ex:
            logger.error("Failed to commit to the database "+str(ex))

    def commit_to_database(self, query : str):
        try:
            self.cursor.execute(query)
            self.mydb.commit()
            logger.debug("Succusfuly commited to the database")

        except Exception as ex:
            logger.error("Failed to commit to the database "+str(ex))

if __name__ == "__main__":
    database = Database("localhost", "root", "MirmoDB2004", "timetable_database")


"""
self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MirmoDB2004",
                database="timetable_database"
            )
"""
    
    

            