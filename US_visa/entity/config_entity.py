## -*- Code : Utf -*-

"""
    A config entity refers to a configuration class or data structure that holds configuration settings 
    for different parts of the ML project. These settings can include hyperparameters, file paths, database credentials, 
    or any other configuration data required to run the project.
"""


import os
from US_visa.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP :str= datetime.now().strftime("%m_%d_%Y_%H_%M_%S") 


@dataclass
class TrainingPipelineConfig:
    pipeline_name :str=PIPELINE_NAME
    artifacts_dir :str=os.path.join(ARTIFACTS_DIR, TIMESTAMP)
    timestamp :str=TIMESTAMP

training_pipeline_config : TrainingPipelineConfig=TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir :str= os.path.join(training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path :str= os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    training_file_path :str= os.path.join(data_ingestion_dir,DATA_INGESTION_DIR_NAME,TRAIN_FILE_NAME)
    testing_file_path :str= os.path.join(data_ingestion_dir,DATA_INGESTION_DIR_NAME,TEST_FILE_NAME)
    train_split_test_ratio_path :float= DATA_INGESTION_TRAIN_AND_TEST_SPLIT_RATIO
    collection_name_path :str= DATA_INGESTION_COLLECTION_NAME
