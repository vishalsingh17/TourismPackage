import logging
import sys

from tourism.exception import TourismException
from tourism.utils.main_utils import MainUtils
from tourism.utils.read_params import read_params

logger = logging.getLogger(__name__)


class ModelFinder:
    def __init__(self):
        self.config = read_params()

        self.utils = MainUtils()

    def get_trained_models(self, X_data, Y_data):
        try:
            models_lst = list(self.config["train_model"].keys())

            x_train, y_train, x_test, y_test = (
                X_data[:, :-1],
                X_data[:, -1],
                Y_data[:, :-1],
                Y_data[:, -1],
            )

            lst = [
                (
                    self.utils.get_tuned_model(
                        model_name,
                        x_train,
                        y_train,
                        x_test,
                        y_test,
                    )
                )
                for model_name in models_lst
            ]

            return lst

        except Exception as e:
            raise TourismException(e, sys) from e
