#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from src.StationData import *

def speed_translate(nautical_mile_per_hour):
    return nautical_mile_per_hour * 1852.0 / 3600

speed_15_mile = speed_translate(15)


class Pamameter:
    def __init__(self, station_hour_data):
        self.station_hour_data = station_hour_data
        self.t_500 = c
        self.t_850 = self.station_hour_data.get_t(850)
        self.td_850 = self.station_hour_data.get_td(850)

    # 850 cloud temperature, 500 env temperature
    def get_SI(self):
        return self.t_500 - self.td_850

    def get_LI(self, li_td):
        return self.t_500 - li_td

    # 100-700 / 50 ??? hpa_keys = [1000,925,850,700,500,400,300,250,200,150,100], need Interpolation?
    def get_BLI(self):
        bli = 10000
        for i in range(100, 700, 50):
            mid_td = self.station_hour_data.get_t(i)
            t_li = self.get_LI(mid_td)
            bli = min(bli, t_li)
        return bli

    def get_K(self, hpa_key):
        t_hpa = self.station_hour_data.get_t(hpa_key)
        td_hpa = self.station_hour_data.get_td(hpa_key)
        return (self.t_850 - self.t_500) + self.td_850 - (t_hpa - td_hpa)

    def get_MK(self, dt_0, dt_850, t_500, hpa_key):
        t_0 = ground_t
        td_0 = ground_td
        t_hpa = self.station_hour_data.get_t(hpa_key)
        td_hpa = self.station_hour_data.get_td(hpa_key)
        return 0.5*(t_0 + self.t_850) + 0.5*(td_0 + self.td_850) - self.t_500 - (t_hpa - td_hpa)

    def get_TT(self):
        return self.t_850 + self.td_850 - 2 * self.t_500

    # if dt_850 < 0, config 0
    def get_SWEAT(self):
        tt = self.get_TT()
        f_850_mps = self.station_hour_data.get_ws(850)
        f_500_mps = self.station_hour_data.get_ws(500)
        wind_direction = 0
        a_850 = self.station_hour_data.get_wa(850)
        a_500 = self.station_hour_data.get_wa(500)

        if 130 <= a_850 <= 250 and 210 <= a_500 <= 310 and a_500 > a_850 \
                and a_500 >= speed_15_mile and a_850 >= speed_15_mile:
            wind_direction = 125 * (math.sin(a_500 - a_850) + 0.2)
        return 12*max(self.td_850, 0) + 20*max(tt - 49, 0) + 2*f_850_mps + f_500_mps + wind_direction

    def get_DCI(self):
        t_900 = self.station_hour_data.get_t(900) # ????
        return self.t_850 + self.td_850 - self.get_LI(t_900)

    # Tvp Tve meaning?
    @staticmethod
    def get_CAPE(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_BCAPE(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_DCAPE(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_SSI(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_BRN(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_RSH(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_EHI(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_CIN(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

    @staticmethod
    def get_ZHT(t_850, dt_850, t_500, t_900):
        return t_850 + dt_850 - Pamameter.get_LI(t_500, t_900)

if __name__ == '__main__':
    print(speed_translate(15))