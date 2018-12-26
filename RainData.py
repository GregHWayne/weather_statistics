#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.mylib import *

# contain all date:cnt pair for one station
txt_template = "{:0>8d}" + sep_char + "{}" + sep_char + "{}"
class StationRainData:
    def __init__(self, id_int):
        self.id = id_int
        self.date_dict = {}

    def parse(self, items):
        if len(items) != 3:
            print("wrong format of rain_out_data, items num ", len(items))
            return None
        date_txt = items[0]
        self.date_dict[date_txt] = int(items[2])

    def add_rain(self, date_txt):
        if date_txt not in self.date_dict:
            self.date_dict[date_txt] = 1
        else:
            self.date_dict[date_txt] += 1

    # date, id, cnt
    def to_string_list(self):
        ret_list = []
        for date_int in self.date_dict.keys().sort():
            ret_list.append(txt_template.format(date_int, self.id, self.date_dict[date_int]))
        return ret_list

# return {id, StationRainData}
def load_rain_data_from_file(rain_out_file):
    rain_data_dict = {} # id, rain_data
    with open(rain_out_file, 'r') as f:
        for line in f.readlines()[2:]:
            items = line.strip('\n').split(sep_char) # date,hour,id,value
            id_int = int(items[2])
            date_int = int(items[0])
            if id_int not in rain_data_dict:
                rain_data_dict[id_int] = StationRainData(id_int)
            rain_data_dict.get(id_int).add_rain(date_int)
    return rain_data_dict

# get detail information of rain from data directories into csv files
out_template = "{}" + sep_char + "{}" + sep_char + "{}" + sep_char + "{}\n"
def get_rain_data_from_dir(src_dir, dst_file):
    with open(dst_file, 'w') as of:
        of.write(out_template.format("date", "hour", "id", "value"))
        for filepath in get_file_list(src_dir):
            filename = filepath.split('\\')[-1]
            date_hour = filename.split('_')[0]
            date_txt = date_hour[0:8]
            hour_txt = date_hour[8:]
            with open(filepath, 'r', encoding='UTF-8') as f:
                for line in f.readlines():
                    items = line.split('\n')[0].split(sep_char)
                    # if items[1] != "U4319":
                    if items[1].isdigit():
                        #print(items[1])
                        of.write(out_template.format(date_txt, hour_txt, items[1], items[4]))



if __name__ == '__main__':
    #get_rain_data_from_dir(DirConf.rain5_dir, DirConf.rain5_out_file)
    #get_rain_data_from_dir(DirConf.rain10_dir, DirConf.rain10_out_file)
    rain_data_dict5 = load_rain_data_from_file(DirConf.rain5_out_file)
    #rain_data_dict10 = load_rain_data_from_file(DirConf.rain10_out_file)