import logging
import os
import sys
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PowerTransformer

from tourism.components.data_ingestion import DataIngestion
from tourism.exception import TourismException
from tourism.utils.main_utils import MainUtils
from tourism.utils.read_params import read_params

logger = logging.getLogger(__name__)


class DataTransformation:
    def __init__(self):
        self.schema_config = read_params("tourism/config/schema.yaml")

        self.data_ingestion = DataIngestion()

        self.utils = MainUtils()

        self.config = read_params()

        self.artifacts_dir = self.config["artifacts_dir"]

        os.makedirs(self.artifacts_dir, exist_ok=True)

    def get_data_transformer_object(self):
        logger.info(
            "Entered get_data_transformer_object method of Data_Ingestion class"
        )

        try:
            disc_feature = self.schema_config["disc_feature"]

            continuous_features = self.schema_config["continuous_features"]

            cat_features = self.schema_config["cat_features"]

            transform_features = self.schema_config["transform_features"]

            logger.info(
                "Got numerical cols,one hot cols,binary cols from schema config"
            )

            logger.info("Initialized Data Transformer pipeline.")

            discrete_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("scaler", StandardScaler()),
                ]
            )

            continuous_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            transform_pipe = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("transformer", PowerTransformer(standardize=True)),
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("Discrete_Pipeline", discrete_pipeline, disc_feature),
                    ("Continuous_Pipeline", continuous_pipeline, continuous_features),
                    ("Categorical_Pipeline", cat_pipeline, cat_features),
                    ("Power_Transformation", transform_pipe, transform_features),
                ]
            )

            logger.info("Created preprocessor object from ColumnTransformer")

            logger.info(
                "Exited get_data_transformer_object method of Data_Ingestion class"
            )

            return preprocessor

        except Exception as e:
            raise TourismException(e, sys) from e

    @staticmethod
    def _outlier_capping(col, df):

        logger.info("Entered _outlier_capping method of Data_Transformation class")

        try:
            logger.info("Performing _outlier_capping for columns in the dataframe")

            upper_limit = df[col].mean() + 3 * df[col].std()

            lower_limit = df[col].mean() - 3 * df[col].std()

            df = df[(df[col] < upper_limit) & (df[col] > lower_limit)]

            logger.info(
                "Performed _outlier_capping method of Data_Transformation class"
            )

            logger.info("Exited _outlier_capping method of Data_Transformation class")

            return df

        except Exception as e:
            raise TourismException(e, sys) from e

    def initiate_data_transformation(self, train_set, test_set):
        logger.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )

        try:
            preprocessor = self.get_data_transformer_object()

            logger.info("Got the preprocessor object")

            target_column_name = self.schema_config["target_column"]

            numerical_columns = self.schema_config["numerical_columns"]

            logger.info(
                "Got target column name and numerical columns from schema config"
            )

            continuous_columns = self.schema_config["continuous_features"]

            logger.info("Got a list of continuous_columns")

            [self._outlier_capping(col, train_set) for col in continuous_columns]

            logger.info("Outlier capped in train df")

            [self._outlier_capping(col, test_set) for col in continuous_columns]

            logger.info("Outlier capped in test df")

            input_feature_train_df = train_set.drop(
                columns=[target_column_name], axis=1
            )

            target_feature_train_df = train_set[target_column_name]

            logger.info("Got train features and test features")

            input_feature_test_df = test_set.drop(columns=[target_column_name], axis=1)

            target_feature_test_df = test_set[target_column_name]

            logger.info("Got test features and test features")

            logger.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logger.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            logger.info("Used the preprocessor object to transform the test features")

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logger.info("Created train array and test array")

            preprocessor_obj_file_name = (
                self.artifacts_dir + "/" + "preprocessor" + ".pkl"
            )

            self.utils.save_object(preprocessor_obj_file_name, preprocessor)

            logger.info("Saved the preprocessor object")

            logger.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )

            return train_arr, test_arr

        except Exception as e:
            raise TourismException(e, sys) from e
