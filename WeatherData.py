#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.mylib import *

NORMAL = -1
LIGHTNING = 0
THUNDERSTORM = 1
HAIL = 2
SNOW = 3
SAND = 4
weather_dict = {LIGHTNING : 'lightning', THUNDERSTORM : 'thunderstorm',
                HAIL : 'hail', SNOW : 'snow', SAND : 'sand'}
date_template = "{:4d}{:0>2d}{:0>2d}"
txt_template = "{}"+sep_char+"{}"

class WeatherData:
    def __init__(self, id_int=0, date_int=99999999):
        self.station_id = id_int
        self.date_txt = date_int
        self.type = []

    def weather_normal(self):
        return len(self.type) == 0

    def get_type_list(self): # type list
        return self.type

    def parse(self, items):
        if len(items) != 12:
            print("wrong format for WeatherData, get ", len(items))
            return False
        self.station_id = int(items[0])
        self.date_txt = date_template.format(int(items[4]), int(items[5]), int(items[6]))
        self.type.clear()
        if int(items[7]):
            self.type.append(LIGHTNING)
        if int(items[8]):
            self.type.append(THUNDERSTORM)
        if int(items[9]):
            self.type.append(HAIL)
        if int(items[10]):
            self.type.append(SNOW)
        if int(items[11]):
            self.type.append(SAND)
        return True

    # date,id
    def to_string(self):
        return txt_template.format(self.date_txt, self.station_id)
    @staticmethod
    def header_string():
        return txt_template.format("date", "id")

def get_weather_data_from_file(src_cvs, dst_dir):
    data = WeatherData()
    out_txt_dict = {}
    for key in weather_dict.keys():
        out_txt_dict[key] = [WeatherData.header_string()]

    with open(src_cvs, 'r', encoding='gbk') as src_f:
        header = src_f.readline()
        for line in src_f.readlines():
            items = line.strip('\\n').split(sep_char)
            if data.parse(items) and not data.weather_normal():
                for type in data.get_type_list():
                    out_txt_dict[type].append(data.to_string())

    out_name_temp = dst_dir + '{0}.csv'
    for key in out_txt_dict.keys():
        dst_file_name = out_name_temp.format(weather_dict[key])
        write_file(dst_file_name, out_txt_dict[key])


class StationWeatherData:
    def __init__(self, id_int):
        self.id = id_int
        self.date_list = []

    def parse(self, items):
        if len(items) != 2:
            print("wrong format of weather_out_data, items num ", len(items))
            return None
        self.date_list.append(items[0])

# return {id, StationWeatherData}
def load_weather_data_from_file(weather_out_file):
    weather_data_dict = {}
    with open(weather_out_file, 'r') as f:
        for line in f.readlines()[2:]:
            items = line.strip('\n').split()
            id_int = int(items[1])
            if id_int not in weather_data_dict:
                weather_data_dict[id_int] = StationWeatherData(id_int)
            weather_data_dict[id_int].parse(items)
    return weather_data_dict

if __name__ == '__main__':
    get_weather_data_from_file(DirConf.weather_in_file, DirConf.weather_out_dir)