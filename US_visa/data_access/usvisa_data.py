## -*- Code:Utf -*-

import pandas as pd
from US_visa.configuration.mongo_db_connection import MongoDBClient
from US_visa.constants import DATABASE_NAME
import sys
from US_visa.logger import logging
from US_visa.exception import USVisaException
import numpy as np
from typing import Optional


class USvisaData:
    """
    A class to handle operations related to US visa data, specifically fetching and converting data 
    from a MongoDB collection into a pandas DataFrame.

    Attributes:
        mongo_client (MongoDBClient): An instance of the MongoDBClient class for connecting to MongoDB.

    Methods:
        export_collection_as_dataframe(collection_name, database_name=None):
            Exports a MongoDB collection as a pandas DataFrame.
    """

    def __init__(self):
        """
        Initializes the USvisaData class by setting up a MongoDB client connection.

        Raises:
            USVisaException: If there is an error while establishing a connection to MongoDB.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logging.info("Fetched data from MongoDB")
        except Exception as e:
            logging.error(f"Error fetching data from DB: {e}")
            raise USVisaException(e, sys)

    
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports a MongoDB collection as a pandas DataFrame.

        Args:
            collection_name (str): The name of the MongoDB collection to export.
            database_name (Optional[str]): The name of the MongoDB database. Defaults to None.
            
        Returns:
            pd.DataFrame: The MongoDB collection data as a pandas DataFrame.

        Raises:
            USVisaException: If there is an error during the export or conversion process.
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            logging.info("Data is converted into DataFrame")
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"nan": np.nan}, inplace=True)
            return df

        except Exception as e:
            logging.error(f"Error in converting DataFrame: {e}")
            raise USVisaException(e, sys)
