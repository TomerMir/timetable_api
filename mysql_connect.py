import mysql.connector
import logging
import threading
import time

#The database class
class Database:
    
    #Constructor that saves all of the variables and starts the pinging thread.
    def __init__(self, host : str, user : str, password : str, database: str, logger : logging.Logger) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.logger = logger
        self.connect_to_database()
        self.start_ping_thread()

    #Set the class logger
    def set_logger(self, logger : logging.Logger):
        self.logger = logger

    #Starts the pinging thread
    def start_ping_thread(self):
        self.ping_thread = threading.Thread(target=self.ping)
        self.ping_thread.start()
        self.logger.debug("Started ping thread")
    
    #Connects to the database
    def connect_to_database(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.logger.info("Connected to database")
            self.cursor = self.mydb.cursor(buffered=True)
            self.logger.debug("Got cursor")
    
        except Exception as ex:
            self.logger.fatal("Failed to connect to the database" + str(ex))
            exit()

    #Pings the database every 2 minutes forever
    def ping(self):
        while True:
            try:
                self.cursor.execute("SELECT * FROM users WHERE username='ping';")
                self.logger.debug("Succusfuly pinged database")
            except Exception as ex:
                self.logger.error("Failed to ping database" + str(ex))
                self.logger.info("Reconnecting to database...")
                self.connect_to_database()
            time.sleep(120)
            
    #Get data from the database - execute the query
    def fetch_from_database(self, query : str) -> tuple:
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.logger.debug("Succusfuly fetched data from the database")
            return result
        except Exception as ex:
            self.logger.debug("Query error: "+query)
            self.logger.error("Failed to fetch the database "+str(ex))
            self.logger.info("Reconnecting to database...")
            self.connect_to_database()
            return  None
    
    #Get data from the database - execute the query with values tuple
    def fetch_from_database_values(self, query : str, values : tuple) -> tuple:
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchall()
            self.logger.debug("Succusfuly fetched data from the database")
            return result
        except Exception as ex:
            self.logger.debug("Query error: "+query)
            self.logger.error("Failed to fetch the database "+str(ex))
            self.logger.info("Reconnecting to database...")
            self.connect_to_database()
            return  None

    #Commit to the database - execute the query with values tuple
    def commit_to_database_values(self, query : str, values : tuple):
        try:
            self.cursor.execute(query, values)
            self.mydb.commit()
            self.logger.debug("Succusfuly commited to the database")

        except Exception as ex:
            self.logger.debug("Query error: "+query)
            self.logger.error("Failed to commit to the database "+str(ex))
            self.logger.info("Reconnecting to database...")
            self.connect_to_database()
    
    #Commit to the database - execute the query
    def commit_to_database(self, query : str):
        try:
            self.cursor.execute(query)
            self.mydb.commit()
            self.logger.debug("Succusfuly commited to the database")

        except Exception as ex:
            self.logger.debug("Query error: "+query)
            self.logger.error("Failed to commit to the database "+str(ex))
            self.logger.info("Reconnecting to database...")
            self.connect_to_database()
