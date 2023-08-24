from sensor.exception import SensorException
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.logger import logging
import pandas as pd
import sys,os
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp

class DataValidation:
    
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
        pass
    
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            
            if len(dataframe.columns)  == number_of_columns:
                return True
        except Exception as e:
            raise SensorException(e,sys)
    
    
    def is_numerical_column_exist(self, dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']
            datafram_columns = dataframe.columns
            
            numrical_columns_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in datafram_columns:
                    numrical_columns_present=False
                    missing_numerical_columns.append(num_column)
            logging.info(f"missing numeric columns: [{missing_numerical_columns}]")
            return numrical_columns_present
        
        except Exception as e:
            raise SensorException(e,sys)
    
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                if is_same_dist.pvalue >=threshold:
                    is_found = False
                    
                else:
                    is_found = True
                    status = False
                report.update({col:{"p_value": float(is_same_dist.pvalue),
                                        "drift_status": is_found}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path   
            
            #create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(filepath=drift_report_file_path,content=report)  
            return status
        
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Read data from train and test file loaction 
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            # validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe dose not contain all columns"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe dose not contain all columns"
                
                
            # validate numerical columns
            
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe dose not contain all numerical columns"
            
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe dose not contain all numerical columns"
                
            if len(error_message)>0:
                raise Exception(error_message)
            
            # lets check data drift 
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            # if status is False:
            #     raise Exception(error)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                validation_train_file_path=self.data_ingestion_artifact.trained_file_path,
                validation_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drif_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)