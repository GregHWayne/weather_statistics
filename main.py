#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.StationData import *
from src.WeatherData import *
from src.RainData import *
from src.mylib import *

station_id_list = get_id_list(DirConf.station_file) # int

def filter_weather_station_data(out_weather_data, station_data_dict, out_station_data):
    weather_data_dict = load_weather_data_from_file(out_weather_data)
    with open(out_station_data, mode='w', encoding='UTF-8') as out_f:
        for id_int in weather_data_dict.keys():
            weather_data = weather_data_dict.get(id_int)
            station_data = station_data_dict.get(id_int)
            for date_int in weather_data.date_list:
                station_date_data = station_data.date_dict.get(date_int)
                date_str = str(date_int) + sep_char
                for line in station_date_data.to_string_list():
                    out_f.write(date_str + line + '\n')


def filter_rain_station_data(rain_out_file, station_data_dict, out_station_data):
    rain_data_dict = load_rain_data_from_file(rain_out_file)
    with open(out_station_data, mode='w', encoding='UTF-8') as out_f:
        for id_int in rain_data_dict.keys():
            rain_data = rain_data_dict.get(id_int)
            station_data = station_data_dict.get(id_int)
            for date_int in rain_data.date_dict.keys().sort():
                rain_cnt = rain_data.date_dict.get(date_int)
                date_str = str(date_int) + sep_char + str(rain_cnt) + sep_char
                station_date_data = station_data.date_dict.get(date_int)
                for line in station_date_data.to_string_list():
                    out_f.write(date_str + line + '\n')

if __name__ == '__main__':
    #station_out_files = [DirConf.station_out_08, DirConf.station_out_20]
    station_out_files = [DirConf.station_out_08]
    station_data_dict = load_hpa_data_from_files(station_out_files)
    filter_weather_station_data(DirConf.weather_out_lightning, station_data_dict, DirConf.lightning_station_data)
    '''
    filter_weather_station_data(DirConf.weather_out_thunderstorm, station_data_dict, DirConf.thunderstorm_station_data)
    filter_weather_station_data(DirConf.weather_out_hail, station_data_dict, DirConf.hail_station_data)
    filter_weather_station_data(DirConf.weather_out_snow, station_data_dict, DirConf.snow_station_data)
    filter_weather_station_data(DirConf.weather_out_sand, station_data_dict, DirConf.sand_station_data)

    filter_rain_station_data(DirConf.rain5_out_file, station_data_dict, DirConf.rain5_station_data)
    filter_rain_station_data(rain10_out_file, station_data_dict, DirConf.rain10_station_data)
    '''