from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path :str
    test_file_path :str
    
    
@dataclass
class DataValidationArtifact:
    validation_status: bool
    validation_train_file_path :str
    validation_test_file_path :str
    invalid_train_file_path :str
    invalid_test_file_path :str
    drif_report_file_path :str
    
    
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path : str
    transformed_train_file_path :str
    transformed_test_file_path :str
    
@dataclass
class ClassificationMetric:
    f1_score: float
    precision_score: float
    recall_score: float
      
@dataclass
class ModelTrainerArtifact:
    trainde_model_file_path : str
    train_metric_artifact: ClassificationMetric
    test_metric_artifact: ClassificationMetric