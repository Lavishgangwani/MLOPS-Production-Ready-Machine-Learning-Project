## -*- Code:Utf -*-

import os
import sys
from US_visa.logger import logging
from US_visa.exception import USVisaException

from US_visa.constants import DATABASE_NAME, MONGODB_URL_KEY
import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    """
     A client class to connect to a MongoDB database using credentials from environment variables.

    Attributes:
        client (pymongo.MongoClient): A static attribute to hold the MongoDB client connection.
        database_name (str): The name of the database to connect to.
        data_base (pymongo.database.Database): The database object for the given database name.
    
    Methods:
        __init__(database_name): Initializes the MongoDB client and connects to the specified database.
    """
    try:
        client = None

        def __init__(self,database_name=DATABASE_NAME) -> None:
            
            if MongoDBClient.client is None:
                mongodb_url_key = os.getenv(MONGODB_URL_KEY)
                logging.info("MongoDB Key Fetched.!")
                if mongodb_url_key is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                
                MongoDBClient.client = pymongo.MongoClient(mongodb_url_key, tlsCAFile=ca)
            
            self.client = MongoDBClient.client
            self.data_base = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB Connection Successful..!!")
    
    except Exception as e:
        logging.error(f"Error During Connection {e}")
        raise USVisaException(e,sys) from e



