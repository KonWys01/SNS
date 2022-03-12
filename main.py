from datetime import datetime, timedelta

import numpy as np

from python.read_yuma import read_yuma
from python.date2tow import date2tow


class Satellites:
    def __init__(self, file_name: str):
        self.file = file_name
        self.naval = self.read_file()
        self.start_date = datetime(year=2022, month=2, day=25)
        self.end_date = datetime(year=2022, month=2, day=26)

    def read_file(self):
        return read_yuma(self.file)

    def set_start_end_dates(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date


if __name__ == "__main__":
    sat = Satellites(file_name='almanac.yuma.week0150.589824.txt')

