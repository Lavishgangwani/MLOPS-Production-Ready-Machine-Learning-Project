## -*- Code:Utf  -*-

import sys
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from pandas import DataFrame

from US_visa.constants import SCHEMA_FILE_PATH, TARGET_COLUMN, CURRENT_YEAR
from US_visa.entity.config_entity import DataTransformationConfig
from US_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from US_visa.logger import logging
from US_visa.exception import USVisaException
from US_visa.utils.main_utils import save_object, save_numpy_array_data, drop_columns, read_yaml_file
from US_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    """
    A class used to handle the data transformation process for the US Visa classification problem.

    Attributes
    ----------
    data_ingestion_artifact : DataIngestionArtifact
        An artifact containing the paths to the ingested training and testing data.
    data_validation_artifact : DataValidationArtifact
        An artifact containing the validation status of the ingested data.
    data_transformation_config : DataTransformationConfig
        A configuration object for data transformation parameters.
    _schema_config : dict
        A dictionary containing the schema configuration read from a YAML file.

    Methods
    -------
    read_data(file_path) -> DataFrame:
        Reads the CSV file from the given file path and returns a pandas DataFrame.
    get_data_transformer_object() -> Pipeline:
        Creates and returns a preprocessor pipeline for transforming the data.
    initiate_data_transformation() -> DataTransformationArtifact:
        Initiates the data transformation process and returns a DataTransformationArtifact.
    """

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
        Initializes the DataTransformation object with ingestion, validation, and transformation artifacts.

        Parameters
        ----------
        data_ingestion_artifact : DataIngestionArtifact
            An artifact containing the paths to the ingested training and testing data.
        data_validation_artifact : DataValidationArtifact
            An artifact containing the validation status of the ingested data.
        data_transformation_config : DataTransformationConfig
            A configuration object for data transformation parameters.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(filepath=SCHEMA_FILE_PATH)

        except Exception as e:
            logging.error(f"Error during Initialization : {e}")
            raise USVisaException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        """
        Reads the CSV file from the given file path and returns a pandas DataFrame.

        Parameters
        ----------
        file_path : str
            The path to the CSV file.

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the data from the CSV file.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error during Read Data : {e}")
            raise USVisaException(e, sys) from e

    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates and returns a preprocessor pipeline for transforming the data.

        The pipeline includes steps for standard scaling, one-hot encoding, ordinal encoding,
        and power transformation based on the schema configuration.

        Returns
        -------
        Pipeline
            A scikit-learn Pipeline object for data transformation.
        """
        logging.info("Entered get_data_transformer_object of DataTransformation class")

        try:
            logging.info("Got the numerical columns from Schema.yaml file design")

            numeric_transformer = StandardScaler()
            ohe_transformer = OneHotEncoder()
            oe_transformer = OrdinalEncoder()

            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            ohe_columns = self._schema_config['ohe_columns']
            oe_columns = self._schema_config['oe_columns']
            transform_columns = self._schema_config['transform_columns']
            num_columns = self._schema_config['num_features']

            logging.info("Initialize PowerTransformer")

            transform_pipeline = Pipeline(steps=[
                ("transformer", PowerTransformer(method='yeo-johnson'))
            ])

            preprocessor = ColumnTransformer(transformers=[
                ("OneHotEncoder", ohe_transformer, ohe_columns),
                ("OrdinalEncoder", oe_transformer, oe_columns),
                ("Transformer", transform_pipeline, transform_columns),
                ("StandardScaler", numeric_transformer, num_columns)
            ])

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info("Exited get_data_transformer_object method of DataTransformation class")
            return preprocessor

        except Exception as e:
            logging.error(f"Error during Creating Preprocessor Pipeline : {e}")
            raise USVisaException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation process and returns a DataTransformationArtifact.

        The process includes reading data, preprocessing, applying SMOTEENN for handling class imbalance,
        and saving the transformed data and preprocessor object.

        Returns
        -------
        DataTransformationArtifact
            An artifact containing the paths to the transformed training and testing data,
            and the preprocessor object.
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Fetched the preprocessor object")

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                logging.info("Read the Data from Train and Test File Path..!")

                input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]

                logging.info("Got train features and target features of Training dataset")

                input_features_train_df['company_age'] = CURRENT_YEAR - input_features_train_df['yr_of_estab']
                logging.info("Added company_age column to the Training dataset")

                drop_cols = self._schema_config['drop_columns']
                logging.info("Drop the columns in drop_cols of Training dataset")

                input_features_train_df = drop_columns(df=input_features_train_df, cols = drop_cols)
                
                target_feature_train_df = target_feature_train_df.replace(TargetValueMapping()._asdict())
                logging.info("Target Variable Mapping is Done..!!")

                input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]

                input_features_test_df['company_age'] = CURRENT_YEAR - input_features_test_df['yr_of_estab']
                logging.info("Added company_age column to the Test dataset")

                target_feature_test_df = target_feature_test_df.replace(TargetValueMapping()._asdict())

                logging.info("Got train features and target features of Testing dataset")
                logging.info("Applying preprocessing object on training dataframe and testing dataframe")

                input_features_train_arr = preprocessor.fit_transform(input_features_train_df)
                logging.info("TRANSFORMED the preprocessor object to fit transform the train features")

                input_features_test_arr = preprocessor.transform(input_features_test_df)
                logging.info("TRANSFORMED the preprocessor object to transform the test features")

                logging.info("Applying SMOTEENN on Training dataset")
                smt = SMOTEENN(sampling_strategy='minority')

                input_features_train_final, target_feature_train_final = smt.fit_resample(
                    input_features_train_arr, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                logging.info("Applying SMOTEENN on testing dataset")
                input_features_test_final, target_feature_test_final = smt.fit_resample(
                    input_features_test_arr, target_feature_test_df
                )

                logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")
                train_arr = np.c_[
                    input_features_train_final, np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                    input_features_test_final, np.array(target_feature_test_final)
                ]

                save_object(filepath=self.data_transformation_config.transformed_object_file_path, obj=preprocessor)
                save_numpy_array_data(filepath=self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(filepath=self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("Saved the preprocessor object")

                logging.info("Exited initiate_data_transformation method of DataTransformation class")

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )

                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)

        except Exception as e:
            logging.error(f"Error During Initiating Data Transformation : {e}")
            raise USVisaException(e, sys) from e
