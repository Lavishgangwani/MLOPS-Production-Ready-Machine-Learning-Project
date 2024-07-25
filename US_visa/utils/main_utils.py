## -*- Code : Utf -*-


import os
import dill
import yaml
import numpy as np
import sys
from pandas import DataFrame

from US_visa.logger import logging
from US_visa.exception import USVisaException



def read_yaml_file(filepath:str)->dict:
    """
    Read YAML file.
    
    Args:
        filepath (str): The filepath where the file is stored.
        
    Returns:
        dict: The content of the YAML file as a dictionary.
    """

    try:
        with open(filepath, mode='rb') as file_obj:
            logging.info(f"Reading YAML file from {filepath}")
            return yaml.safe_load(file_obj)

    except Exception as e:
        logging.error(f"Error loading object: {e}")
        raise USVisaException(e,sys) from e
    



def write_yaml_file(filepath:str, content:object, replace:bool=False)->None:
    """
    Write YAML file.
    
    Args:
        filepath (str): The path where we want to store the YAML file.
        content (object): The content to write into the YAML file.
        replace (bool): Whether to replace the existing file if it exists. Default is False.
    
    Returns:
        None
    """
    try:

        if replace:
            if (os.path.exists(filepath)):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath, mode='w') as file_obj:
            logging.info(f"Writing YAML file in : {filepath}")
            yaml.dump(content, file_obj)
        
    except Exception as e:
        logging.error(f"Error loading object: {e}")
        raise USVisaException(e,sys) from e
    



def load_object(filepath:str)-> object:
    """
    Load an object from a file using dill.
    
    Args:
        filepath: The path to the file from which the object will be loaded.
    
    Returns:
        The loaded object.
    """
    try:
        with open(filepath, "rb") as file_obj:
            logging.info(f"Loading object from {filepath}")
            return dill.load(file_obj)
    
    except Exception as e:
        logging.error(f"Error loading object: {e}")
        raise USVisaException(e, sys) from e
    


def save_object(filepath:str, obj:object)-> None:
    """
    Save an object to a file using dill.
    
    Args:
        obj: The object to be saved.
        filepath: The path to the file where the object will be saved.
    """
   
    try:
       os.makedirs(os.path.dirname(filepath),exist_ok=True)
       with open(filepath, mode='wb') as file_obj:
           logging.info(f"Saving Object {obj} to {filepath}")
           dill.dump(obj, file_obj)
    
    except Exception as e:
       logging.error(f"Error loading object: {e}")
       raise USVisaException(e,sys) from e
    


def load_numpy_array_data(filepath:str)-> np.array:
    """
    Load an Numpy array from a file

    Args:
        filepath (str):The path to the file from which the numpy array will be loaded.

    Return:
        np.array
    """

    try:
        with open(filepath, mode='rb') as file:
            logging.info(f"Loading the array file {filepath}")
            return np.load(file)
        
    except Exception as e:
        logging.error(f"Error loading object: {e}")
        raise USVisaException(e,sys) from e
    



def save_numpy_array_data(filepath:str, array:np.array):
    """
    Save an Numpy array to a file

    Args:
        filepath (str):  The path to the file from which the numpy array will be saved.
        arr (np.array): The numpy array which has to be saved
    """

    try :
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, mode='wb') as file:
            logging.info(f"Saving Numpy array to {filepath}")
            np.save(file, array)

    except Exception as e:
        logging.error(f"Saving Array Error: {e}")
        raise USVisaException(e,sys) from e


        
def drop_columns(df:DataFrame, cols:list)-> DataFrame:
    """
    Drop the List columns from Dataframe

    Args:
        df (DataFrame): The DataFrame from which Columns needs to be dropped
        cols (list): Columns in list format which need to be dropped

    Return:
        The DataFrame
    """

    try:
        df = df.drop(columns=cols, axis=1)
        logging.info(f"Dropping the Columns {cols} from dataframe")
        return df
    
    except Exception as e:
        logging.error(f"Error Dropping Columns {e}")
        raise USVisaException(e,sys) from e