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
import os,sys
# logging.info("We have divieding by zero")

#for check data ingention and components
# from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

# if __name__ == '__main__':
#     training_pipeline_config = TrainingPipelineConfig()
#     data_ingention_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
#     print(data_ingention_config.__dict__)
    
#for test trainingpipeline from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainingPipeline
import os
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, UploadFile, File
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response, FileResponse
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
env_file_path=os.path.join(os.getcwd(),"env.yaml")

# def set_env_variable(env_file_path):

#     if os.getenv('MONGO_DB_URL',None) is None:
#         env_config = read_yaml_file(env_file_path)
#         os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route(file: UploadFile = File()):
    try:
        #get data from user csv file
        data = file
        #conver csv file to dataframe

        df=pd.read_csv(data,sep="	")
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
        return FileResponse(df)
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        #set_env_variable(env_file_path)
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)
