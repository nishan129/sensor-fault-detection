from sensor.utils.main_utils import load_numpy_array_data
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
import os,sys
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_obj, load_object,write_yaml_file
from sensor.ml.model.estimator import ModelResolver
import shutil

class ModelPusher:
    
    def __init__(self, model_pusher_config:ModelPusherConfig,
                 model_eval_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
            
        except Exception as e:
            raise SensorException(e,sys)
            
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            
            #creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)
            
            #save model dir
            save_model_path = self.model_pusher_config.save_model_path
            os.makedirs(os.path.dirname(save_model_path,),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=save_model_path)
            
            #prepare artifacts
            model_pusher_artifact = ModelPusherArtifact(save_model_path=save_model_path,model_file_path=model_file_path)
            logging.info(f"model pusher is complete model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)