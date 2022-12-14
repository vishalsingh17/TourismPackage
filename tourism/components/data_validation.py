import json
import logging
import sys

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from tourism.exception import TourismException
from tourism.utils.data_validation_utils import *
from tourism.utils.read_params import read_params

logger = logging.getLogger(__name__)


class DataValidation:
    def __init__(self, train_set, test_set):
        self.schema_config = read_params("tourism/config/schema.yaml")

        self.train_set = train_set

        self.test_set = test_set

        self.validation_status = False

    def validate_dataset_schema_columns(self):
        logger.info(
            "Entered validate_dataset_schema_columns method of Data_Validation class"
        )

        try:
            logger.info("Validating dataset schema columns")

            train_schema_status = validate_schema_columns(self.train_set)

            logger.info("Validated dataset schema columns on the train set")

            test_schema_status = validate_schema_columns(self.test_set)

            logger.info("Validated dataset schema columns on the test set")

            logger.info("Validated dataset schema columns")

            return train_schema_status, test_schema_status

        except Exception as e:
            raise TourismException(e, sys) from e

    def validate_dataset_schema_for_numerical_datatype(self):
        logger.info(
            "Entered validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
        )

        try:
            logger.info("Validating dataset schema for numerical datatype")

            train_num_datatype_status = validate_schema_for_numerical_datatype(
                self.train_set
            )

            logger.info("Validated dataset schema for numerical datatype for train set")

            test_num_datatype_status = validate_schema_for_numerical_datatype(
                self.test_set
            )

            logger.info("Validated dataset schema for numerical datatype for test set")

            logger.info(
                "Exited validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
            )

            return train_num_datatype_status, test_num_datatype_status

        except Exception as e:
            raise TourismException(e, sys) from e

    def validate_dataset_schema_for_categorical_datatype(self):
        logger.info(
            "Entered validate_dataset_schema_for_categorical_datatype method of Data_Validation class"
        )

        try:
            logger.info("Validating dataset schema for categorical datatype")

            train_cat_cols = validate_schema_for_categorical_datatype(self.train_set)

            logger.info(
                "Validated dataset schema for catergorical datatype on the train set"
            )

            test_cat_cols = validate_schema_for_categorical_datatype(self.test_set)

            logger.info(
                "Validated dataset schema for catergorical datatype on the test set"
            )

            logger.info("Validated dataset schema for categorical datatype")

            logger.info(
                "Exited validate_dataset_schema_for_categorical_datatype method of Data_Validation class"
            )

            return train_cat_cols, test_cat_cols

        except Exception as e:
            raise TourismException(e, sys) from e

    @staticmethod
    def detect_dataset_drift(reference, production, get_ratio=False):
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference, production)

            report = data_drift_profile.json()

            json_report = json.loads(report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]

            n_drifted_features = json_report["data_drift"]["data"]["metrics"][
                "n_drifted_features"
            ]

            if get_ratio:
                return n_drifted_features / n_features

            else:
                return json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

        except Exception as e:
            raise TourismException(e, sys) from e

    def initiate_data_validation(self):
        logger.info("Entered initiate_data_validation method of Data_Validation class")

        try:
            logger.info("Initiated data validation for the dataset")

            train_df = self.train_set
            test_df = self.test_set

            drift = self.detect_dataset_drift(train_df, test_df)

            if drift is False:
                (
                    schema_train_col_status,
                    schema_test_col_status,
                ) = self.validate_dataset_schema_columns()

                logger.info(
                    f"Schema train cols status is {schema_train_col_status} and schema test cols status is {schema_test_col_status}"
                )

                logger.info("Validated dataset schema columns")

                (
                    schema_train_cat_cols_status,
                    schema_test_cat_cols_status,
                ) = self.validate_dataset_schema_for_categorical_datatype()

                logger.info(
                    f"Schema train cat cols status is {schema_train_cat_cols_status} and schema test cat cols status is {schema_test_cat_cols_status}"
                )

                logger.info("Validated dataset schema for catergorical datatype")

                (
                    schema_train_num_cols_status,
                    schema_test_num_cols_status,
                ) = self.validate_dataset_schema_for_numerical_datatype()

                logger.info(
                    f"Schema train numerical cols status is {schema_train_num_cols_status} and schema test numerical cols status is {schema_test_num_cols_status}"
                )

                logger.info("Validated dataset schema for numerical datatype")

                if (
                    schema_train_cat_cols_status is True
                    and schema_test_cat_cols_status is True
                    and schema_train_num_cols_status is True
                    and schema_test_num_cols_status is True
                    and schema_train_col_status is True
                    and schema_test_col_status is True
                ):
                    logger.info("Dataset schema validation completed")
                    return True
                else:
                    logger.info("Dataset schema validation Stopped")
                    return False
            else:
                logger.info("Data Drift detected, data validation stopped")

                return False

        except Exception as e:
            raise TourismException(e, sys) from e
