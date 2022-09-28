import logging
import sys
from json import loads
import os

import pandas as pd
from pymongo import MongoClient

from tourism.exception import TourismException

logger = logging.getLogger(__name__)


class MongoDBOperation:
    """
    Description :   This method is used for all mongodb operations
    Written by  :   iNeuron Intelligence

    Version     :   1.0
    Revisions   :   None
    """

    def __init__(self):
        self.DB_URL = f'mongodb+srv://iNeuron:{os.environ["iNeuronDBPassword"]}@ineuron-ai-projects.7eh1w4s.mongodb.net/?retryWrites=true&w=majority'

        self.client = MongoClient(self.DB_URL)

    def get_database(self, db_name):
        """
        Method Name :   get_database
        Description :   This method gets database from MongoDB from the db_name

        Output      :   A database is created in MongoDB with name as db_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.0
        Revisions   :   None
        """
        logger.info("Entered get_database method of MongoDB_Operation class")

        try:
            db = self.client[db_name]

            logger.info(f"Created {db_name} database in MongoDB")

            logger.info("Exited get_database method MongoDB_Operation class")

            return db

        except Exception as e:
            raise TourismException(e, sys) from e

    def get_collection(self, database, collection_name):
        """
        Method Name :   get_collection
        Description :   This method gets collection from the particular database and collection name

        Output      :   A collection is returned from database with name as collection name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.0
        Revisions   :   None
        """
        logger.info("Entered get_collection method of MongoDB_Operation class")

        try:
            collection = database[collection_name]

            logger.info(f"Created {collection_name} collection in mongodb")

            logger.info("Exited get_collection method of MongoDB_Operation class ")

            return collection

        except Exception as e:
            raise TourismException(e, sys) from e

    def get_collection_as_dataframe(self, db_name, collection_name):
        """
        Method Name :   get_collection_as_dataframe
        Description :   This method is used for converting the selected collection to dataframe

        Output      :   A collection is returned from the selected db_name and collection_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.0
        Written by  :   iNeuron Intelligence
        Revisions   :   None
        """
        logger.info(
            "Entered get_collection_as_dataframe method of MongoDB_Operation class"
        )

        try:
            database = self.get_database(db_name)

            collection = database.get_collection(name=collection_name)

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            logger.info("Converted collection to dataframe")

            logger.info(
                "Exited get_collection_as_dataframe method of MongoDB_Operation class"
            )

            return df

        except Exception as e:
            raise TourismException(e, sys) from e

    def insert_dataframe_as_record(self, data_frame, db_name, collection_name):
        """
        Method Name :   insert_dataframe_as_record
        Description :   This method inserts the dataframe as record in database collection

        Output      :   The dataframe is inserted in database collection
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.0
        Revisions   :   None
        """
        logger.info("Entered insert_dataframe_as_record method of MongoDB_Operation")

        try:
            records = loads(data_frame.T.to_json()).values()

            logger.info(f"Converted dataframe to json records")

            database = self.get_database(db_name)

            collection = database.get_collection(collection_name)

            logger.info(
                "Inserting records to MongoDB",
            )

            collection.insert_many(records)

            logger.info("Inserted records to MongoDB")

            logger.info(
                "Exited the insert_dataframe_as_record method of MongoDB_Operation"
            )

        except Exception as e:
            raise TourismException(e, sys) from e
