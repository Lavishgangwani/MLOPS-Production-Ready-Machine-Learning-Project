## -*- Code:Utf -*-

import os
import sys
from US_visa.logger import logging
from US_visa.exception import USVisaException

from US_visa.entity.config_entity import (DataIngestionConfig,
                                          DataValidationConfig,
                                          DataTransformationConfig)

from US_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact,
                                            DataTransformationArtifact)

from US_visa.components.data_ingestion import DataIngestion
from US_visa.components.data_validation import DataValidation
from US_visa.components.data_transformation import DataTransformation


class TrainPipeline:
    """
    TrainPipeline class orchestrates the training pipeline workflow.

    Attributes
    ----------
    data_ingestion_config : DataIngestionConfig
        Configuration for data ingestion.
    data_validation_config : DataValidationConfig
        Configuration for data validation.
    data_transformation_config : DataTransformationConfig
        Configuration for data transformation.
    """

    def __init__(self):
        """
        Initializes the TrainPipeline with data ingestion, validation, and transformation configurations.
        """
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion process and fetches the data from MongoDB.

        Returns
        -------
        DataIngestionArtifact
            Contains paths to the ingested training and testing datasets.

        Raises
        ------
        USVisaException
            If any error occurs during data ingestion.
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from MongoDB")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from MongoDB")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact

        except Exception as e:
            logging.error(f"Error occurred during start_data_ingestion: {e}")
            raise USVisaException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Starts the data validation process.

        Parameters
        ----------
        data_ingestion_artifact : DataIngestionArtifact
            An artifact containing paths to the ingested training and testing datasets.

        Returns
        -------
        DataValidationArtifact
            An artifact containing the validation status and report of the ingested data.

        Raises
        ------
        USVisaException
            If any error occurs during data validation.
        """
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validation_artifact

        except Exception as e:
            raise USVisaException(e, sys) from e

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        Starts the data transformation process.

        Parameters
        ----------
        data_ingestion_artifact : DataIngestionArtifact
            An artifact containing paths to the ingested training and testing datasets.
        data_validation_artifact : DataValidationArtifact
            An artifact containing the validation status and report of the ingested data.

        Returns
        -------
        DataTransformationArtifact
            An artifact containing the paths to the transformed training and testing datasets,
            and the preprocessor object.

        Raises
        ------
        USVisaException
            If any error occurs during data transformation.
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact

        except Exception as e:
            logging.error(f"Error During start data transformation: {e}")
            raise USVisaException(e, sys) from e

    def run_pipeline(self) -> None:
        """
        Executes the entire training pipeline.

        Raises
        ------
        USVisaException
            If any error occurs during the pipeline execution.
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact)

        except Exception as e:
            raise USVisaException(e, sys)
