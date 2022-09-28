import logging
import sys

from tourism.exception import TourismException
from tourism.utils.read_params import read_params

logger = logging.getLogger(__name__)

schema_config = read_params("tourism/config/schema.yaml")

def validate_schema_columns(df):
    try:
        try:
            if len(df.columns) == len(schema_config["columns"]):
                validation_status = True
            else:
                validation_status = False
        except Exception as e:
            validation_status = False

        return validation_status
    except Exception as e:
        raise TourismException(e, sys) from e

def validate_schema_for_numerical_datatype(df):
    try:
        for column in schema_config["numerical_columns"]:
            try:
                if column in df.columns:
                    validation_status = True
                else:
                    validation_status = False

            except:
                validation_status = False

        return validation_status

    except Exception as e:
        raise TourismException(e, sys) from e

def validate_schema_for_categorical_datatype(df):
    try:
        for column in schema_config["categorical_columns"]:
            try:
                if column in df.columns:
                    validation_status = True
                else:
                    validation_status = False

            except:
                validation_status = False

        return validation_status

    except Exception as e:
        raise TourismException(e, sys) from e