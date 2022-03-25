from datetime import datetime, timedelta

import numpy as np

from python.read_yuma import read_yuma
from python.date2tow import date2tow


class Satellites:
    def __init__(self, file_name: str, start_date: datetime, mask: int, observer_pos: list):
        self.file = file_name
        self.naval = self.read_file()
        self.start_date = start_date
        self.end_date = self.start_date + timedelta(days=1)
        self.interval = timedelta(minutes=15)
        self.mask = mask
        print(self.mask)
        self.r_neu = self.r_neu(observer_pos[0], observer_pos[1], observer_pos[2])

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

    @staticmethod
    def satellite_xyz(week: int, tow: int, nav: np.ndarray):
        id, health, e, toa, i, omega_dot, sqrta, Omega, omega, m0, alfa, alfa1, gps_week = nav

        t = week * 7 * 86400 + tow
        toa_weeks = gps_week * 7 * 86400 + toa
        tk = t - toa_weeks

        """algorytm"""
        u = 3.986005 * (10 ** 14)
        omega_e = 7.2921151467 * (10 ** -5)
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

    @staticmethod
    def phi_lamda_to_xyz(phi: float, lamda: float, height: float):
        a = 6378137
        e2 = 0.00669438002290
        phi = np.deg2rad(phi)
        lamda = np.deg2rad(lamda)
        N = a / (np.sqrt(1 - e2*(np.sin(phi)**2)))

        x = (N + height)*np.cos(phi)*np.cos(lamda)
        y = (N + height)*np.cos(phi)*np.sin(lamda)
        z = (N*(1-e2) + height)*np.sin(phi)
        return x, y, z

    @staticmethod
    def r_neu(phi: float, lamda: float, height: float):
        phi = np.deg2rad(phi)
        lamda = np.deg2rad(lamda)
        matrix = np.array([[-np.sin(phi)*np.cos(lamda), -np.sin(lamda), np.cos(phi)*np.cos(lamda)],
                           [-np.sin(phi)*np.sin(lamda), np.cos(lamda), np.cos(phi)*np.sin(lamda)],
                           [np.cos(phi), 0, np.sin(phi)]])
        return matrix

    @staticmethod
    def neu(r_neu: np.array, Xsr: list):
        r_neu = np.transpose(r_neu)
        return np.dot(r_neu, Xsr)

    def satellites_coordinates(self):
        A = np.zeros((0, 4))
        number_of_satellites = self.naval.shape[0]
        era_date = self.start_date
        while era_date <= self.end_date:
            data = self.datetime_to_list(era_date)
            week, tow = date2tow(data)

            for id in range(number_of_satellites):
                nav = self.naval[id, :]

                Xs = self.satellite_xyz(week, tow, nav)  # satellite xyz
                Xr = self.phi_lamda_to_xyz(52, 21, 100)
                Xsr = [i - j for i, j in zip(Xs, Xr)]

                neu = self.neu(self.r_neu, Xsr)  # satellite neu
                n, e, u = neu

                Az = np.arctan2(e, n)  # arctan(e/n)
                Az = np.degrees(Az)
                el = np.arcsin(u / (np.sqrt(n ** 2 + e ** 2 + u ** 2)))  # elewacja
                el = np.degrees(el)

                r = np.sqrt(Xsr[0] ** 2 + Xsr[1] ** 2 + Xsr[2] ** 2)
                if el > self.mask:
                    A1 = np.array([(-(Xs[0]-Xr[0]) / r),
                                   (-(Xs[1] - Xr[1]) / r),
                                   (-(Xs[2] - Xr[2]) / r),
                                   1])
                    A = np.vstack([A, A1])
                era_date += self.interval
                # break
            break
        print(A)
        # print('a', A)
        Q = np.linalg.inv(np.dot(A.transpose(), A))
        # print('q', Q)
        qx, qy, qz, qt = Q.diagonal()
        Qxyz = Q[:3, :3]
        # print('Qxyz', Qxyz)

        PDOP = np.sqrt(qx + qy + qz)
        TDOP = np.sqrt(qt)
        GDOP = np.sqrt(PDOP**2 + TDOP**2)
        # print(GDOP, PDOP, TDOP)

        Qneu = self.r_neu.transpose() @ Qxyz @ self.r_neu
        # print('Qneu', Qneu)
        qn, qe, qu = Qneu.diagonal()
        HDOP = np.sqrt(qn + qe)
        VDOP = np.sqrt(qu)
        PDOPneu = np.sqrt(HDOP**2 + VDOP**2)
        print('hdop', HDOP, 'vdop', VDOP, 'pdopneu', PDOPneu)

    def set_interval(self, interval: timedelta):
        self.interval = interval


if __name__ == "__main__":
    sat = Satellites(file_name='almanac.yuma.week0150.589824.txt', start_date=datetime(year=2002, month=10, day=10), mask=10, observer_pos=[50,20,100])
    # sat.set_start_end_dates(datetime(year=2022, month=2, day=25), datetime(year=2022, month=2, day=25))
    sat.satellites_coordinates()
