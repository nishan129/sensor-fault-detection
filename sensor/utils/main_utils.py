from sensor.exception import SensorException
import yaml
import sys
from sensor.logger import logging
import os
import numpy as np
import dill

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e,sys)
    
    
def write_yaml_file(filepath: str, content:object, replace:bool = False) -> None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise SensorException(e,sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys)
    

def save_obj(file_path: str, obj:object) -> None:
    
    try:
        logging.info("Enterd the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            
        logging.info("Exited the save_object method od MainUtils class")
    except Exception as e:
        raise SensorException(e,sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) 
    
    
def load_object(file_path: str) -> object:
    try:
        if os.path.exists(file_path):
            raise Exception("file path: {file_path} is not exists")
        
        with open(file_path, "rb") as file_obj:
            dill.load(file_obj)
            return dill
        logging.info("object in loaded ")
    except Exception as e:
        raise SensorException(e, sys) 