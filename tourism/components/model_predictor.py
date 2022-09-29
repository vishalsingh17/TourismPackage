import logging
import sys

import pandas as pd

from car_price.components.s3_operations import S3Operation
from car_price.exception import CarException
from car_price.utils.main_utils import MainUtils
from car_price.utils.read_params import read_params

log_writer = logging.getLogger(__name__)


class CarPriceData:
    def __init__(
        self,
        car_name,
        vehicle_age,
        km_driven,
        seller_type,
        fuel_type,
        transmission_type,
        mileage,
        engine,
        max_power,
        seats,
    ):
        self.car_name = car_name

        self.vehicle_age = vehicle_age

        self.km_driven = km_driven

        self.seller_type = seller_type

        self.fuel_type = fuel_type

        self.transmission_type = transmission_type

        self.mileage = mileage

        self.engine = engine

        self.max_power = max_power

        self.seats = seats

    def get_carprice_input_data_frame(self):

        log_writer.info(
            "Entered get_carprice_input_data_frame method of CarPriceData class"
        )

        try:
            carprice_input_dict = self.get_car_data_as_dict()

            log_writer.info("Got car data as dict")

            log_writer.info(
                "Exited get_carprice_input_data_frame method of CarPriceData class"
            )

            return pd.DataFrame(carprice_input_dict)

        except Exception as e:
            raise CarException(e, sys) from e

    def get_car_data_as_dict(self):
        log_writer.info("Entered get_car_data_as_dict method as CarPriceData class")

        try:
            input_data = {
                "car_name": [self.car_name],
                "vehicle_age": [self.vehicle_age],
                "km_driven": [self.km_driven],
                "seller_type": [self.seller_type],
                "fuel_type": [self.fuel_type],
                "transmission_type": [self.transmission_type],
                "mileage": [self.mileage],
                "engine": [self.engine],
                "max_power": [self.max_power],
                "seats": [self.seats],
            }

            log_writer.info("Created car data dict")

            input_data = pd.DataFrame(input_data)

            log_writer.info("Created a dataframe of car data")

            log_writer.info("Exited get_car_data_as_dict method as CarPriceData class")

            return input_data

        except Exception as e:
            raise CarException(e, sys) from e


class CarPricePredictor:
    def __init__(self):
        self.utils = MainUtils()

        self.s3 = S3Operation()

        self.config = read_params()

        self.model_file = self.config["model_file_name"]

        self.io_files_bucket = self.config["s3_bucket"]["car_price_input_files_bucket"]

    def predict(self, X):
        log_writer.info("Entered predict method of CarPricePredictor class")

        try:
            best_model = self.s3.load_model(self.model_file, self.io_files_bucket)

            log_writer.info("Loaded best model from s3 bucket")

            selling_price_pred = best_model.predict(X)

            log_writer.info("Used best model to get predictions")

            log_writer.info("Exited predict method of CarPricePredictor class")

            return selling_price_pred

        except Exception as e:
            raise CarException(e, sys) from e