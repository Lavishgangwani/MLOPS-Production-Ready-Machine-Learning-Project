## -*- Code:Utf -*-

"""The constants are used in an ML project to store and organize configuration values and 
    constants in a centralized and easily accessible manner. 
    The __init__.py file helps in initializing the package and can also aggregate constants 
    from various files within the constants folder, making it easier to import them into your main project files."""

import os
import datetime
from datetime import date

"Initialize DB Name"
DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "visa_data"

"Initialize MongoDB Connection URL Securely using Enviournment Variable using Git Bash"
MONGODB_URL_KEY = "MONGODB_URL"

PIPELINE_NAME : str= "usvisa"
ARTIFACTS_DIR : str="artifacts"


TRAIN_FILE_NAME :str="train.csv" 
TEST_FILE_NAME :str="test.csv" 

FILE_NAME :str="US_visa.csv"
MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME="Preprocessor.pkl"
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")


"""
DATA INGESTION Related CONSTANTS start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME : str= "visa_data"
DATA_INGESTION_DIR_NAME : str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR :str="Feature_store"
DATA_INGESTION_INGESTED_DIR :str="Ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float=0.2


"""
DATA VALIDATION Related CONSTANTS starts with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME :str= "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR :str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str= "drift_report.yaml"


"""
DATA TRANSFORMATION Related CONSTANTS starts with DATA TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME :str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR :str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR :str="transformed_object"
