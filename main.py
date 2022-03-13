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
        self.interval = timedelta(minutes=15)
        # WGS84
        self.a = 6378137
        self.e2 = 0.00669438002290

    def read_file(self):
        return read_yuma(self.file)

    def set_start_end_dates(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def datetime_to_list(date: datetime):
        date = [date.year,
                date.month,
                date.day,
                date.hour,
                date.minute,
                date.second]
        return date

    def satellite_xyz(self, week: int, tow: int, nav: np.ndarray):
        id, health, e, toa, i, omega_dot, sqrta, Omega, omega, m0, alfa, alfa1, gps_week = nav

        t = week * 7 * 86400 + tow
        toa_weeks = gps_week * 7 * 86400 + toa
        tk = t - toa_weeks
        # print(tk)

        """algorytm"""
        u = 3.986005 * (10 ** 14)
        omega_e = 7.2921151467 * (10 ** -5)
        # tk = t - toa
        a = sqrta ** 2
        n = np.sqrt(u / (a ** 3))
        Mk = m0 + n * tk

        E1 = Mk
        Ei = Mk + e * np.sin(E1)
        while np.fabs(Ei - E1) >= (10 ** -12):
            E1 = Ei
            Ei = Mk + e * np.sin(E1)

        Ek = Ei
        vk = np.arctan2(np.sqrt(1 - e ** 2) * np.sin(Ek), np.cos(Ek) - e)

        phi_k = vk + omega
        rk = a * (1 - e * np.cos(Ek))
        xk = rk * np.cos(phi_k)
        yk = rk * np.sin(phi_k)
        omega_k = Omega + (omega_dot - omega_e) * tk - omega_e * toa

        Xk = xk * np.cos(omega_k) - yk * np.cos(i) * np.sin(omega_k)
        Yk = xk * np.sin(omega_k) + yk * np.cos(i) * np.cos(omega_k)
        Zk = yk * np.sin(i)

        return Xk, Yk, Zk

    def satellites_coordinates(self):
        while self.start_date <= self.end_date:
            data = self.datetime_to_list(self.start_date)
            week, tow = date2tow(data)
            print('data:', data)

            number_of_satellites = self.naval.shape[0]
            for id in range(number_of_satellites):
                nav = self.naval[id, :]
                Xk, Yk, Zk = self.satellite_xyz(week, tow, nav)
                print(Xk, Yk, Zk)
                break

            self.start_date += self.interval

    def set_interval(self, interval: timedelta):
        self.interval = interval


if __name__ == "__main__":
    sat = Satellites(file_name='almanac.yuma.week0150.589824.txt')
    sat.satellites_coordinates()

