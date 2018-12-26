#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
#get all files recursively
def get_file_list(src_path):
    ret = []
    for root, dirs, files in os.walk(src_path):
        '''
        for dir in dirs:
            for name in get_file_list(root+'\\'+dir):
                ret.append(dir+'\\'+name)
        '''
        for name in files:
            ret.append(root+'\\'+name)
    return ret


def get_id_list(filepath):
    id_list = []
    idx = 0
    with open(filepath, 'r', encoding='gbk') as f:
        header = f.readline()
        for line in f.readlines():
            #print(line)
            items = line.strip().strip('\n').split(' ')
            if len(items):
                id_list.append(int(items[idx]))
    return id_list


def write_file(file_name, lines):
    with open(file_name, 'w') as dst_f:
        for line in lines:
            dst_f.write(line + '\n')
class DirConf:
    root_dir   = 'F:\\personal\\ylm\\'
    input_dir  = root_dir + 'input\\'
    output_dir = root_dir + 'out\\'
    #---------------------------------------------
    rain_input_dir = input_dir + 'rain_csv\\一小时降水\\'
    rain5_dir  = rain_input_dir + '5\\'
    rain10_dir = rain_input_dir + '10\\'

    rain_out_dir = output_dir + 'rain_out\\'
    rain5_out_file  = rain_out_dir + 'rain5_out.csv'
    rain10_out_file = rain_out_dir + 'rain10_out.csv'

    station_data_rain5  = rain_out_dir + 'station_data_rain5.csv'
    station_data_rain10 = rain_out_dir + 'station_data_rain10.csv'

    param_data_rain5  = rain_out_dir + 'param_data_rain5.csv'
    param_data_rain10 = rain_out_dir + 'param_data_rain10.csv'
    # ---------------------------------------------
    weather_in_file = input_dir + '强对流_积雪_闪电_大风_扬沙.csv'

    weather_out_dir = output_dir + 'weather_out\\'

    weather_out_lightning = weather_out_dir + 'lightning.csv'
    weather_out_thunderstorm = weather_out_dir + 'thunderstorm.csv'
    weather_out_hail = weather_out_dir + 'hail.csv'
    weather_out_snow = weather_out_dir + 'snow.csv'
    weather_out_sand = weather_out_dir + 'sand.csv'

    station_data_lightning = weather_out_dir + 'station_data_lightning.csv'
    station_data_thunderstorm = weather_out_dir + 'station_data_thunderstorm.csv'
    station_data_hail = weather_out_dir + 'station_data_hail.csv'
    station_data_snow = weather_out_dir + 'station_data_snow.csv'
    station_data_sand = weather_out_dir + 'station_data_sand.csv'

    param_data_lightning = weather_out_dir + 'param_data_lightning.csv'
    param_data_thunderstorm = weather_out_dir + 'param_data_thunderstorm.csv'
    param_data_hail = weather_out_dir + 'param_data_hail.csv'
    param_data_snow = weather_out_dir + 'param_data_snow.csv'
    param_data_sand = weather_out_dir + 'param_data_sand.csv'
    # ---------------------------------------------
    station_input_08 = input_dir + 'tlogp08\\'
    station_input_20 = input_dir + 'tlogp20\\'

    station_out_dir = output_dir + 'station_out\\'

    station_out_08 = station_out_dir + '\\station_08.csv'
    station_out_20 = station_out_dir + '\\station_20.csv'

    param_out_08 = station_out_dir + '\\param_08.csv'
    param_out_20 = station_out_dir + '\\param_20.csv'
    # ---------------------------------------------
    station_file = input_dir + '西藏常规地面站39s.dat'

sep_char = ','



