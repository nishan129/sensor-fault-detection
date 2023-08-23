from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataValidationConfig
from sensor.exception import SensorException
import sys,os
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.components.data_ingestion import DataIngenstion
from sensor.components.data_validation import DataValidation
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME

class TrainingPipeline:
    
    def __init__(self):
        
        self.training_pipeline_config = TrainingPipelineConfig()
        
        #self.training_pipeline_config = training_pipeline_config
        
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingenstion = DataIngenstion(data_ingestion_config=self.data_ingestion_config)
            data_ingenstion_artifact = data_ingenstion.initiate_data_ingestion()
            
            logging.info(f"Data ingestion completed and artifact: {data_ingenstion_artifact}")
            return data_ingenstion_artifact
        
        except Exception as e:
            raise SensorException(e,sys)
        
    
    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data validation")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config = data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)
    
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            raise SensorException(e,sys)
        