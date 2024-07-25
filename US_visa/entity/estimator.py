# -*- Code:Utf -*-


import pandas as pd
from sklearn.pipeline import Pipeline

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
    


        
