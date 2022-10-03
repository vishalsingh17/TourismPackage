import logging
import sys

from tourism.components.data_ingestion import DataIngestion
from tourism.components.data_transformation import DataTransformation
from tourism.components.data_validation import DataValidation
from tourism.components.model_trainer import ModelTrainer
from tourism.exception import TourismException
from tourism.utils.main_utils import MainUtils
from tourism.utils.read_params import read_params

log_writer = logging.getLogger(__name__)


class TrainPipeline:
    def __init__(self):
        self.config = read_params()

        self.utils = MainUtils()

        self.artifacts_dir = self.config["artifacts_dir"]

    @staticmethod
    def start_data_ingestion():
        log_writer.info("Entered the start_data_ingestion method of Pipeline class")

        try:
            log_writer.info("Getting the data from mongodb")

            data_ingestion = DataIngestion()

            df = data_ingestion.get_data_from_mongodb()

            train_set, test_set = data_ingestion.split_data_as_train_test(df)

            log_writer.info("Got the data from mongodb")

            log_writer.info("Exited the start_data_ingestion method of Pipeline class")

            return train_set, test_set

        except Exception as e:
            raise TourismException(e, sys) from e

    @staticmethod
    def start_data_validation(train_set, test_set):
        try:
            data_validation = DataValidation(train_set, test_set)

            return data_validation.initiate_data_validation()

        except Exception as e:
            raise TourismException(e, sys) from e

    @staticmethod
    def start_data_transformation(train_set, test_set):
        try:
            data_transformation = DataTransformation()

            train_set, test_set = data_transformation.initiate_data_transformation(
                train_set, test_set
            )

            return train_set, test_set

        except Exception as e:
            raise TourismException(e, sys) from e

    @staticmethod
    def start_model_trainer(train_set, test_set):
        try:
            model_trainer = ModelTrainer()

            model_trainer.initiate_model_trainer(train_set, test_set)

            return {"status": True, "message": "Model Training completed"}

        except Exception as e:
            raise TourismException(e, sys) from e

    @staticmethod
    def start_model_pusher():
        try:
            model_trainer = ModelTrainer()

            model_trainer.initiate_model_pusher()

        except Exception as e:
            raise TourismException(e, sys) from e

    def run_pipeline(self):
        try:
            train_set, test_set = self.start_data_ingestion()

            if self.start_data_validation(train_set, test_set):

                train_set, test_set = self.start_data_transformation(
                    train_set, test_set
                )

                self.start_model_trainer(train_set, test_set)

                self.start_model_pusher()

        except Exception as e:
            raise TourismException(e, sys) from e
