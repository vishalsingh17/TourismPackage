import logging
import sys
from tourism.components.s3_operations import S3Operation
from tourism.components.tuner import ModelFinder
from tourism.exception import TourismException
from tourism.utils.main_utils import MainUtils
from tourism.utils.read_params import read_params

logger = logging.getLogger(__name__)


class TourismModel:
    def __init__(self, preprocessing_object, trained_model_object):
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, X):
        logger.info("Entered predict method of TourismModel class")

        try:
            logger.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(X)

            logger.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise TourismException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self):
        self.tuner = ModelFinder()

        self.utils = MainUtils()

        self.s3 = S3Operation()

        self.config = read_params()

        self.log_writer = logging.getLogger(__name__)

        self.artifacts_dir = self.config["artifacts_dir"]

        self.io_files_bucket = self.config["s3_bucket"]["tourism_input_files_bucket"]

        self.preprocessor_obj_file_name = self.config["preprocessor_obj_file_name"]

    def initiate_model_trainer(self, train_set, test_set):

        self.log_writer.info(
            "Entered initiate_model_trainer method of ModelTrainer class"
        )

        try:
            lst = self.tuner.get_trained_models(train_set, test_set)

            self.log_writer.info(
                "Got a list of tuple of model score,model and model name"
            )

            (
                best_model,
                best_model_score,
            ) = self.utils.get_best_model_with_name_and_score(lst)

            self.log_writer.info("Got best model score,model and model name")

            preprocessing_obj = self.utils.load_object(self.preprocessor_obj_file_name)

            self.log_writer.info("Loaded preprocessing object")

            base_model_score = self.config["base_model_score"]

            if best_model_score >= base_model_score:
                self.utils.update_model_score(best_model_score)

                self.log_writer.info("Updating model score in yaml file")

                tourism_model = TourismModel(
                    preprocessing_object=preprocessing_obj,
                    trained_model_object=best_model,
                )

                self.log_writer.info(
                    "Created tourism model object with preprocessor and model"
                )

                best_model_file_path = self.artifacts_dir + "/" + "model" + ".sav"

                self.log_writer.info("Created best model file path")

                self.utils.save_object(best_model_file_path, tourism_model)

                self.log_writer.info("Saved the best model object path")

            else:
                self.log_writer.info(
                    "No best model found with score more than base score"
                )
                raise "No best model found with score more than base score "

        except Exception as e:
            raise TourismException(e, sys) from e

    def initiate_model_pusher(self):
        self.log_writer.info(
            "Entered initiate_model_pusher method of ModelTrainer class"
        )

        try:
            self.log_writer.info("Uploading artifacts folder to s3 bucket")

            self.s3.upload_folder(self.artifacts_dir, self.io_files_bucket)

            self.log_writer.info("Uploaded artifacts folder to s3 bucket")

            self.log_writer.info(
                "Exited initiate_model_pusher method of ModelTrainer class"
            )

        except Exception as e:
            raise TourismException(e, sys) from e
