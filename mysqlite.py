#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python内部自带的数据库，不用单独安装插件
# 可以参考https://docs.python.org/2/library/sqlite3.html

'''
注释
def create_table():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE COMPANY
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);")
    conn.commit()
    conn.close()
    
def insert():
    conn = sqlite3.connect('test.db')
    c = conn.cursor() # 每次都要声明表格的所有字段？
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )")
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
    c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
    conn.commit()
    conn.close()
    
def select():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print("ID = ", row[0])
        print( "NAME = ", row[1])
        print( "ADDRESS = ", row[2])
        print( "SALARY = ", row[3])
    conn.close()
    
def update():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
    conn.commit()
    print("Total number of rows updated :", conn.total_changes)

    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print("ID = ", row[0])
        print( "NAME = ", row[1])
        print( "ADDRESS = ", row[2])
        print( "SALARY = ", row[3])
    conn.close()

def delete():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("DELETE from COMPANY where ID=2;")
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)

    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print("ID = ", row[0])
        print( "NAME = ", row[1])
        print( "ADDRESS = ", row[2])
        print( "SALARY = ", row[3])
    conn.close()
'''


from src.mylib import *
import csv, sqlite3

def csv_to_sqlite3(db_name, table_name, data_file):
    con = sqlite3.connect(db_name)
    with open(data_file,'r') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        header = dr.fieldnames
        col_name = ""
        col_value = ""
        for key in header:
            col_name += "{},".format(key)
            col_value += "?,"
        table_create = "DROP TABLE IF EXISTS {0};CREATE TABLE {0}({1});".format(table_name, col_name.strip(","))
        table_insert = "INSERT INTO {} VALUES ({});".format(table_name, col_value.strip(","))
        to_db = []
        for i in dr:
            record = []
            for key in header:
                record.append(i[key])
            to_db.append(record)

        cur = con.cursor()
        cur.executescript(table_create.format(header))
        cur.executemany(table_insert, to_db)
        con.commit()
    con.close()

def load_data_into_sqlite(dbname='test.db'):
    csv_to_sqlite3(dbname, "rain5_out_file", DirConf.rain5_out_file)
    csv_to_sqlite3(dbname, "rain10_out_file", DirConf.rain10_out_file)
    csv_to_sqlite3(dbname, "weather_out_hail", DirConf.weather_out_hail)
    csv_to_sqlite3(dbname, "weather_out_lightning", DirConf.weather_out_lightning)
    csv_to_sqlite3(dbname, "weather_out_sand", DirConf.weather_out_sand)
    csv_to_sqlite3(dbname, "weather_out_snow", DirConf.weather_out_snow)
    csv_to_sqlite3(dbname, "weather_out_thunderstorm", DirConf.weather_out_thunderstorm)

def get_tables(db_file='test.db'):
    conn = sqlite3.connect(db_file) # 连接数据库
    cur = conn.cursor() # 获取操作符
    cur.execute("select name from sqlite_master where type='table'")
    # sqlite_master is the main table for all tables in database
    ret = cur.fetchall()
    conn.close()
    return ret

def drop_table(db_file='test.db', table_name='t'):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS {0};".format(table_name))
    conn.commit()
    conn.close()

def select(db_file, table_name, date_txt, id_txt):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    records = cursor.execute("SELECT * from {2} where id='{0}' and date='{1}';".format(id_txt, date_txt, table_name))
    conn.close()
    return records


if __name__ == '__main__':
    dbname = 'test.db'
    print('tables list:', get_tables(dbname))
    '''
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    records = c.execute("SELECT * from {} ;".format("rain5_out_file"))
    conn.close()
    for record in records:
        station_data_list = select('test.db', 'rain5_out_file', record[0], record[1])
        print(station_data_list)
        '''
    '''
    print(get_tables(dbname))
    '''
    '''
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    cursor = c.execute("SELECT id from t")
    for row in cursor:
        print("ID = ", row[0])
    conn.close()
    '''