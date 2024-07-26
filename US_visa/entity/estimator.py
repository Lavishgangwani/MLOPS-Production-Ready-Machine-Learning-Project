# -*- Code:Utf -*-

import pandas as pd
from sklearn.pipeline import Pipeline
from pandas import DataFrame
import sys

from US_visa.logger import logging
from US_visa.exception import USVisaException


class TargetValueMapping:
    """
    A class used to map target values for classification tasks.

    Attributes
    ----------
    Certified : int
        The integer value assigned to the "Certified" category.
    Denied : int
        The integer value assigned to the "Denied" category.

    Methods
    -------
    _asdict():
        Returns a dictionary representation of the class attributes.
    reverse_mapping():
        Returns a dictionary with the integer values as keys and the category names as values.
    """

    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1

    def _asdict(self):
        """Returns a dictionary representation of the class attributes."""
        return self.__dict__

    def reverse_mapping(self):
        """
        Returns a dictionary with the integer values as keys and the category names as values.
        """
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class USvisaModel:
    """
    A class used to encapsulate a machine learning model and its preprocessing steps for predicting US visa outcomes.

    Attributes
    ----------
    preprocessing_object : Pipeline
        A preprocessing pipeline to transform input data.
    trained_model_object : DataFrame
        A trained model object to make predictions.

    Methods
    -------
    predict(dataframe: DataFrame) -> DataFrame:
        Transforms the input dataframe using the preprocessing pipeline and returns predictions from the trained model.
    """

    def __init__(self, preprocessing_object: Pipeline, trained_model_object: DataFrame):
        """
        Initializes the USvisaModel with a preprocessing pipeline and a trained model.

        Parameters
        ----------
        preprocessing_object : Pipeline
            The preprocessing pipeline to transform input data.
        trained_model_object : DataFrame
            The trained model to make predictions.
        """
        try:
            self.preprocessing_object = preprocessing_object
            self.trained_model_object = trained_model_object

        except Exception as e:
            logging.error(f"Error during initializing Objects for USvisaModel class: {e}")
            raise USVisaException(e, sys) from e

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Transforms the input dataframe using the preprocessing pipeline and returns predictions from the trained model.

        Parameters
        ----------
        dataframe : DataFrame
            The input data to be transformed and used for predictions.

        Returns
        -------
        DataFrame
            The predictions made by the trained model.

        """
        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            logging.error(f"Error during prediction using USvisaModel class: {e}")
            raise USVisaException(e, sys) from e

    def __repr__(self):
        """
        Returns a string representation of the USvisaModel class.

        Returns
        -------
        str
            The string representation of the class.
        """
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        """
        Returns a string representation of the USvisaModel class.

        Returns
        -------
        str
            The string representation of the class.
        """
        return f"{type(self.trained_model_object).__name__}()"
