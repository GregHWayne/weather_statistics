#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from src.mylib import *

hpa_keys = [1000,925,850,700,500,400,300,250,200,150,100]
hour_keys = ['08', '20']

'''
class StationInfo:
    def __init__(self):
        self.id = 0
        self.longitude = ""
        self.latitude = ""
        self.altitude = 0.0
        self.code = 0

    def parse(self, item):
        if len(item) == 5:
            self.id = int(item[0])
            self.longitude = str(item[1])
            self.latitude = str(item[2])
            self.altitude = float(item[3])
            self.code = int(item[4])
        else :
            print("wrong format")
'''

txt_template = "{}"+sep_char+"{}"+sep_char+"{}"+sep_char+"{}"+sep_char+"{}"+sep_char+"{}"
class SampleData:
    def __init__(self, hpa):
        self.theory_hpa = hpa
        self.hpa = 9999
        self.temp = 9999 # temperature
        self.dew_temp = 9999 # dew_temperature
        self.wind_angle = 9999 # wind direction，360/16 = 22.5
        self.wind_speed = 9999

    def get_t(self):
        return self.temp
    def get_td(self):
        return self.dew_temp
    def get_ws(self):
        return self.wind_speed
    def get_wa(self):
        return self.wind_angle

    def parse(self, item):
        if len(item) == 6:
            self.theory_hpa = int(item[0])
            self.hpa = int(item[1])
            self.temp = float(item[2])
            self.dew_temp = float(item[3])
            self.wind_angle = float(item[4])
            self.wind_speed = float(item[5])
        else :
            print("wrong format for SampleData, items len ", len(item))
            sys.exit(0)

    def to_string(self):
        return txt_template.format(self.theory_hpa, self.hpa,
                                    self.temp, self.dew_temp,
                                    self.wind_angle, self.wind_speed)

    @staticmethod
    def header_string(post):
        header_template = "{1}_{0},{2}_{0},{3}_{0},{4}_{0},{5}_{0},{6}_{0}"
        return header_template.format(post, "t_hpa", "hpa", "t", "dt", "wa", "ws")

class StationHourData:
    def __init__(self, id):
        self.id = id
        self.base_data = SampleData(9999)
        self.data = {}
        for key in hpa_keys:
            self.data[key] = SampleData(key)

    def get_t(self, hpa_key):
        return self.data[hpa_key].get_t()
    def get_td(self, hpa_key):
        return self.data[hpa_key].get_td()
    def get_ws(self, hpa_key):
        return self.data[hpa_key].get_ws()
    def get_wa(self, hpa_key):
        return self.data[hpa_key].get_wa()

    def parse(self, items):
        sample_len = 6
        sample_total_len = len(hpa_keys)*sample_len + sample_len
        if len(items) != sample_total_len:
            print("wrong format while parsing StationHourData, get items len:", len(items))
            sys.exit(0)
            return None
        for i in range(0, sample_total_len, sample_len):
            hpa_key = int(items[i])
            if hpa_key in hpa_keys:
                self.data[hpa_key].parse(items[i:i+sample_len])
            else:
                self.base_data.parse(items[i:i+sample_len])

    def parse_sample(self, items):
        hpa_key = int(items[0])
        if hpa_key in hpa_keys:
            self.data[hpa_key].parse(items)
        else:
            self.base_data.parse(items)

    def get_id(self):
        return self.id

    def to_string(self):
        ret_str = str(self.id) + sep_char + self.base_data.to_string()
        for key in hpa_keys:
            ret_str += sep_char + self.data[key].to_string()
        return ret_str

    @staticmethod
    def header_string():
        ret = "id" + sep_char + SampleData.header_string("base") # base station
        for key in hpa_keys:
            ret += sep_char + SampleData.header_string(key)
        return ret

    @staticmethod
    def factory_make(id_list, lines):
        data_list = []
        new_data = False
        for line in lines:
            items = line.strip().strip('\\n').split()
            if len(items) == 5:
                new_data = False
                station_id = int(items[0])
                if station_id in id_list:
                    data_list.append(StationHourData(station_id))
                    new_data = True
            elif len(items) == 6:
                if new_data:
                    data_list[-1].parse_sample(items)
            else :
                print("unsupported format ", len(items))
        return data_list


class StationDateData:
    def __init__(self, int_id):
        self.id = int_id
        self.hour_dict = {} # hour:StationHourData

    def parse(self, id, hour, items):
        if hour not in self.hour_dict:
            self.hour_dict[hour] = StationHourData(id)
        hour_data = self.hour_dict[hour]
        hour_data.parse(items)
        return None

    def to_string_list(self):
        ret_list = []
        for key in hour_keys:
            ret_list.append(key + sep_char + self.hour_dict[key].to_string())
        return ret_list

class StationData:
    def __init__(self, id):
        self.id = id
        self.date_dict = {} # date:StationDateData

    def parse(self, id, date, hour, items):
        if date not in self.date_dict:
            self.date_dict[date] = StationDateData(id)
        self.date_dict[date].parse(id, hour, items)

def load_hpa_data_from_files(src_file_list): # return object
    station_data_dict = {}
    for src_file in src_file_list:
        with open(src_file, 'r') as f:
            for line in f.readlines()[2:]:
                items = line.strip('\n').strip(sep_char).split(sep_char)
                date_txt = items[0]
                hour_txt = items[1]
                id_int = int(items[2])
                if id_int not in station_data_dict:
                    station_data_dict[id_int] = StationData(id_int)
                station_data = station_data_dict[id_int]
                station_data.parse(id_int, date_txt, hour_txt, items[3:])
    return station_data_dict

def get_hpa_data_from_dir(id_list, src_dir, dst_file):
    print("start writing into ", dst_file)
    dst_f = open(dst_file, 'w')
    dst_f.write("date" + sep_char + "hour" + sep_char + StationHourData.header_string() + '\n')
    for filepath in get_file_list(src_dir):
        filename = filepath.split('\\')[-1]
        year_txt = filename[0:2]
        if int(year_txt) > 50:
            date_txt = "19" + filename[0:6]
        else:
            date_txt = "20" + filename[0:6]
        hour_txt = filename[6:8]
        with open(filepath, 'r', encoding='gbk') as f:
            datalist = StationHourData.factory_make(id_list, f.readlines()[2:])
            for data in datalist:
                #print(data.get_id(), date_txt)
                dst_f.write(date_txt+sep_char+hour_txt+sep_char+data.to_string()+'\n')
    dst_f.close()
    print("finish writing into ", dst_file)



if __name__ == '__main__':
    print(StationHourData.header_string())
    #station_id_list = get_id_list(DirConf.station_file)
    #get_hpa_data_from_dir(station_id_list, DirConf.station_input_08, DirConf.station_out_08)
    #get_hpa_data_from_dir(station_id_list, DirConf.station_input_20, DirConf.station_out_20)
    # load weather data
    # for id in file:
    #     station_data_dict[id].getDateData(date).get_string()

    '''
    #date_temp = "{:4d}{:0>2d}{:0>2d}"
    #print(date_temp.format(1990,1,1))
    filename = src_file.split('\\')[-1]
    date_txt = filename[0:6]
    hour_txt = filename[6:8]
    '''



























