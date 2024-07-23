## -*- Code :Utf -*-


import os
import sys

from US_visa.logger import logging
from US_visa.exception import USVisaException

from US_visa.entity.config_entity import DataValidationConfig
from US_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from pandas import DataFrame
import json

from US_visa.constants import SCHEMA_FILE_PATH
from US_visa.utils.main_utils import read_yaml_file,write_yaml_file

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

import pandas as pd

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        """
        param:data_ingestion_artifact -> Output reference of data ingestion artifact stage
        param:data_validation_config -> Configuration for data validation
        """
        try:
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_config= data_validation_config
            self._schema_config = read_yaml_file(filepath=SCHEMA_FILE_PATH)
        except Exception as e:
            logging.error(f"Error Unable to read YAML File: {e}")
            raise USVisaException(e,sys)
        

    def validate_number_of_columns(self, dataframe:DataFrame) ->bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try :
            status= len(dataframe.columns) == len(self._schema_config['columns'])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            logging.error(f"Error Unable to validate_number_of_columns: {e}")
            raise USVisaException(e,sys)
        
        
        
