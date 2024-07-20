## -*- Code:Utf -*-

import os
import sys
from US_visa.entity.config_entity import DataIngestionConfig
from US_visa.entity.artifact_entity import DataIngestionArtifact
from US_visa.logger import logging
from US_visa.exception import USVisaException

from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split

from US_visa.data_access.usvisa_data import USvisaData

class DataIngestion:
    """
    A class to handle the data ingestion process in a machine learning pipeline.

    Attributes:
        data_ingestion_config (DataIngestionConfig): Configuration settings for data ingestion.

    Methods:
        export_data_into_feature_store() -> DataFrame:
            Exports data from MongoDB into a feature store as a pandas DataFrame.
        split_data_as_train_test(df: DataFrame) -> None:
            Splits the data into training and testing sets and saves them to CSV files.
        initiate_data_ingestion() -> DataIngestionArtifact:
            Initiates the data ingestion process including exporting data and splitting it into training and testing sets.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initializes the DataIngestion class with the given configuration.

        Args:
            data_ingestion_config (DataIngestionConfig): Configuration settings for data ingestion. Defaults to DataIngestionConfig.

        Raises:
            USVisaException: If there is an error during initialization.
        """
        try:
            logging.info("Data Ingestion Process Entered!")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USVisaException(e, sys)

    
    
    
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Exports data from MongoDB into a feature store as a pandas DataFrame.

        Returns:
            DataFrame: The data exported from MongoDB.

        Raises:
            USVisaException: If there is an error during the export process.
        """
        try:
            logging.info("Exporting Data From MongoDB")
            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"Shape of DataFrame: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            logging.info("Initialize Directory for Raw Data")
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            logging.error(f"Error in Exporting Data into feature store: {e}")
            raise USVisaException(e, sys)

    
    
    def split_data_as_train_test(self, df: DataFrame) -> None:
        """
        Splits the data into training and testing sets and saves them to CSV files.

        Args:
            df (DataFrame): The DataFrame to split into training and testing sets.

        Raises:
            USVisaException: If there is an error during the splitting process.
        """
        try:
            logging.info("Train test split on the dataframe Started!")
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_split_test_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            logging.info("Initialize Directory for Train Data")
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            logging.info("Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
        except Exception as e:
            logging.error(f"Error in Splitting data as train & Test: {e}")
            raise USVisaException(e, sys)

    
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process including exporting data and splitting it into training and testing sets.

        Returns:
            DataIngestionArtifact: An artifact containing the paths to the training and testing data files.

        Raises:
            USVisaException: If there is an error during the data ingestion process.
        """
        try:
            logging.info("Data Ingestion Started!")
            dataframe = self.export_data_into_feature_store()
            logging.info("Fetched the Data from MongoDB")
            self.split_data_as_train_test(dataframe)
            logging.info("Performed Train & Test Split!")
            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f"Error During initiate Data Ingestion: {e}")
            raise USVisaException(e, sys)
