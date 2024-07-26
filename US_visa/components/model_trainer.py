## -*- Code:Utf -*-

import sys
from typing import Tuple

import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from US_visa.utils.main_utils import load_numpy_array_data, load_object, save_object, read_yaml_file

from US_visa.logger import logging
from US_visa.exception import USVisaException

from US_visa.entity.artifact_entity import (DataTransformationArtifact,
                                            ModelTrainerArtifact,
                                            ClassificationMetricsArtifact)

from US_visa.entity.config_entity import ModelTrainerConfig
from US_visa.entity.estimator import USvisaModel
from neuro_mf import ModelFactory
from pandas import DataFrame
from sklearn.pipeline import Pipeline


class ModelTrainer:
    """
    A class used to train machine learning models for US visa application outcomes.

    Attributes
    ----------
    data_transformation_artifact : DataTransformationArtifact
        An artifact containing paths to the transformed training and testing datasets.
    model_trainer_config : ModelTrainerConfig
        Configuration for the model training process.

    Methods
    -------
    get_model_object_and_report(train: np.array, test: np.array) -> Tuple[object, object]:
        Trains the model using the training data and evaluates it using the testing data.
    initiate_model_trainer() -> ModelTrainerArtifact:
        Initiates the model training process and returns an artifact containing the trained model and its metrics.
    """

    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        """
        Initializes the ModelTrainer with data transformation artifacts and model training configuration.

        Parameters
        ----------
        data_transformation_artifact : DataTransformationArtifact
            An artifact containing paths to the transformed training and testing datasets.
        model_trainer_config : ModelTrainerConfig
            Configuration for the model training process.
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """
        Trains the model using the training data and evaluates it using the testing data.

        Parameters
        ----------
        train : np.array
            The training dataset.
        test : np.array
            The testing dataset.

        Returns
        -------
        Tuple[object, object]
            A tuple containing the best model and a classification metrics artifact.

        Raises
        ------
        USVisaException
            If an error occurs during model training or evaluation.
        """
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

            best_model_detail = model_factory.get_best_model(
                X=x_train, y=y_train, base_accuracy=self.model_trainer_config.expected_accuracy
            )

            model_obj = best_model_detail.best_model

            y_pred = model_obj.predict(x_test)

            accuracy_score_ = accuracy_score(y_test, y_pred)
            f1_score_ = f1_score(y_test, y_pred)
            recall_score_ = recall_score(y_test, y_pred)
            precision_score_ = precision_score(y_test, y_pred)

            metric_artifacts = ClassificationMetricsArtifact(f1_score=f1_score_,
                                                             recall_score=recall_score_,
                                                             precision_score=precision_score_)

            return best_model_detail, metric_artifacts

        except Exception as e:
            logging.error(f"Error during get model object and report using neuro_mf: {e}")
            raise USVisaException(e, sys) from e

    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        """
        Initiates the model training process and returns an artifact containing the trained model and its metrics.

        Returns
        -------
        ModelTrainerArtifact
            An artifact containing the trained model and its metrics.

        Raises
        ------
        USVisaException
            If an error occurs during the model training process.
        """
        try:
            train_arr = load_numpy_array_data(filepath=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(filepath=self.data_transformation_artifact.transformed_test_file_path)

            best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)

            preprocessing_obj = load_object(filepath=self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            usvisa_model = USvisaModel(preprocessing_object=preprocessing_obj,
                                       trained_model_object=best_model_detail.best_model)
            logging.info("Created usvisa model object with preprocessor and model")
            logging.info("Created best model file path.")

            save_object(filepath=self.model_trainer_config.trained_model_file_path, obj=usvisa_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                          metrics_artifacts=metric_artifact)

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            logging.error(f"Error during initiating model training: {e}")
            raise USVisaException(e, sys) from e
