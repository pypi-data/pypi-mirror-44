# Gets the latest or given time featrues
import time
from copy import copy


import dask
import pandas as pd
import toolz as tz
import maya
from crayons import blue, green, red, yellow, cyan
from spaceman import Spaceman
from loguru import logger

"""
    # How Features Will Work
    ---

    ```
        features = (
            Features(host="localhost", db="global")
                .set_storage("...")
                .set_type('...')
                .set_time(now=False, back=True, month=0, day=0, hour=0, minute=30)
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .push()
        )
    ```
"""


class Features(object):
    def __init__(self):
        self.parameters = {
            "type": "general"
        }
        self.acceptable = [str, int, float, complex, list, tuple, dict, object]
        self.data_list = []
        self.space = Spaceman()
        self.merged = None
        self.current_time = maya.now()

    def set_storage(self, **kwargs):
        return self

    def set_type(self, _type, **kwargs):
        if not isinstance(_type, str):
            raise TypeError(f"The type - `{_type}` you entered isn't a `str`")
        # print({'type': _type})
        self.parameters.update({'type': _type})

        return self

    def set_time(self, is_now=True, before_now=True, after_now=False, _months=0, _days=0, _hours=0, _minutes=0, _seconds=30, **kwargs):
        if is_now == True:
            self.current_time = maya.now()
        elif is_now == True and before_now == True:
            self.current_time = maya.now()
            self.current_time.subtract(
                months=_months, days=_days, hours=_hours, minutes=_minutes, seconds=_seconds
            )
        elif is_now == True and after_now == True:
            self.current_time = maya.now()
            self.current_time.add(
                months=_months, days=_days, hours=_hours, minutes=_minutes, seconds=_seconds
            )

        return self

    def add_parameter(self, k, v):
        if type(v) not in self.acceptable:
            raise TypeError(f"Value type not acceptable {self.acceptable}")
        if (not isinstance(k, str)):
            raise TypeError("The key is not a `str`")

        self.parameters.update({k: v})
        return self

    def add_data(self, data: pd.DataFrame, ts_index=True, **kwargs):
        if isinstance(data, pd.DataFrame):
            self.data_list.append(data)
        else:
            raise TypeError("data is not a `DataFrame`")
        return self

    def smart_merge(self):
        """ Smart merge things together """

        if len(self.data_list) > 0:
            total = (
                tz.reduce(
                    lambda x, y: pd.merge(
                        x, y, how='outer', left_index=True, right_index=True),
                    self.data_list
                ).dropna()
            )

            self.merged = total

    def prepare_parameters(self):
        self.smart_merge()
        self.parameters.update(
            {"timestamp": self.current_time.__dict__["_epoch"]})

    def print_parameters(self):
        print(cyan(self.parameters))

    def save(self):
        """ Get the parameters and save it. """

        self.prepare_parameters()
        self.print_parameters()

        with self.space as space:
            if self.merged is None:
                logger.debug("No merged value. Exiting save")
                return None
            try:
                space.store(self.merged, query=self.parameters)
            except Exception as e:
                logger.exception(e)
                return None
        return self.merged

    def load(self):
        self.prepare_parameters()
        self.print_parameters()

        with self.space as space:
            try:
                self.merged = space.load(query=self.parameters)
            except Exception as e:
                logger.exception(e)
                return None
        """ Pull data according to what parameters say from the database """
        return self.merged


fd = [{"type": "one", "way": 1234}, {"type": "one", "way": 1234}]


def run_feature_address():
    """ Run the folder """
    features = (Features()
                .set_type("world")
                .set_type("hollow")
                .set_time(is_now=True, before_now=True)
                .set_storage()
                .add_parameter("four", 3)
                .add_parameter("three", 4)
                .add_data(pd.DataFrame(fd))
                .add_data(pd.DataFrame(fd))
                .load())
    print(yellow(features))


if __name__ == "__main__":
    run_feature_address()
