# mongodb
# from sensor.configuration.mongo_db_connection import MongoDBClient

# if __name__ == '__main__':
#     mongodb_clint = MongoDBClient()
#     print(mongodb_clint.database.list_collection_names())


#for exception handling
# import sys
# from sensor.exception import SensorException

# def test_exception():
#     try:
#         x=1/0
#     except Exception as e:
#         raise SensorException(e,sys)
    
# if __name__ == '__main__':
#     try:
#         test_exception()
        
#     except Exception as e:
#         print(e)



# # for logging
from sensor.logger import logging

# logging.info("We have divieding by zero")

#for check data ingention and components
# from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

# if __name__ == '__main__':
#     training_pipeline_config = TrainingPipelineConfig()
#     data_ingention_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
#     print(data_ingention_config.__dict__)
    
#for test trainingpipeline 
from sensor.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        logging.exception(e)