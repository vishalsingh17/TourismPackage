import logging
import sys
from sklearn.model_selection import train_test_split
from tourism.utils.mongo_operations import MongoDBOperation
from tourism.utils.read_params import read_params
from tourism.exception import TourismException

log_writer = logging.getLogger(__name__)

mongo_op = MongoDBOperation()


class DataIngestion:
    def __init__(self):
        self.config = read_params()

        self.schema_config = read_params("tourism/config/schema.yaml")

        self.db_name = self.config["mongo"]["db_name"]

        self.collection_name = self.config["mongo"]["collection_name"]

        self.drop_cols = list(self.schema_config["drop_columns"])

    @staticmethod
    def split_data_as_train_test(df):
        log_writer.info(
            "Entered split_data_as_train_test method of Data_Ingestion class"
        )

        try:
            train_set, test_set = train_test_split(df, test_size=0.2)

            log_writer.info("Performed train test split on the dataframe")

            log_writer.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:
            raise TourismException(e, sys) from e

    def get_data_from_mongodb(self):
        log_writer.info("Entered get_data_from_mongodb method of Data_Ingestion class")

        try:
            log_writer.info("Getting the dataframe from mongodb")

            df = mongo_op.get_collection_as_dataframe(
                self.db_name, self.collection_name
            )

            log_writer.info("Got the dataframe from mongodb")

            log_writer.info(
                "Exited the get_data_from_mongodb method of Data_Ingestion class"
            )

            return df

        except Exception as e:
            raise TourismException(e, sys) from e

    def initiate_data_ingestion(self):
        log_writer.info(
            "Entered initiate_data_ingestion method of Data_Ingestion class"
        )

        try:
            df = self.get_data_from_mongodb()

            df1 = df.drop(self.drop_cols, axis=1)

            log_writer.info("Got the data from mongodb")

            train_set, test_set = self.split_data_as_train_test(df1)

            log_writer.info("Performed train test split on the dataset")

            log_writer.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            return train_set, test_set

        except Exception as e:
            raise TourismException(e, sys) from e
