## -*- Code: Utf -*-

"""
    An artifact entity refers to the output or result produced at different stages of the ML pipeline.
"""


from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path :str
    test_file_path :str


@dataclass
class DataValidationArtifact:
    validation_status :bool
    message :str
    drift_report_file_path :str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path :str
    transformed_train_file_path :str
    transformed_test_file_path :str


@dataclass
class ClassificationMetricsArtifact:
    f1_score :float
    recall_score:float
    precision_score :float



@dataclass
class ModelTrainerArtifact:
    trained_model_file_path :str
    metrics_artifacts :ClassificationMetricsArtifact