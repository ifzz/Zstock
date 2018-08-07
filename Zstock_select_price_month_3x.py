# -*-coding=utf-8-*-
import sys
import tushare as ts
import pandas as pd
import os, sys, datetime, time, codecs
import numpy as np
from threading import Thread
from pandas import Series
import tushare as ts

class select_class():
    def __init__(self):
        # 因为网速问题，手动从本地抓取
        self.today = time.strftime("%Y-%m-%d", time.localtime())
    def get_price(self,stock_code,stock_name):
        stock_price = ts.get_hist_data(stock_code, ktype='M')
        stock_price.to_csv('stock_price.csv')
        price_online = pd.read_csv('stock_price.csv', dtype={'code': np.str})
        price_online_bf =price_online.loc[(price_online['open'] != 0),['date','open','high','close','low']]


        print('---------stock code---------')
        print(stock_code)
        print(stock_name) 
        print('----------------------------')
        print(price_online_bf.sort_values(by='date'))
        price_online_bf.to_csv(stock_code+stock_name + '_month.csv')

def main():
    current = os.getcwd()
    folder = os.path.join(current, 'data')
    if os.path.exists(folder) == False:
        os.mkdir(folder)
    os.chdir(folder)

    obj = select_class()

    df_000625=obj.get_price('000625','长安汽车')
    df_600016=obj.get_price('600016','民生银行')
    df_000876=obj.get_price('000876','新希望')
    df_000883=obj.get_price('000883','湖北能源')
    df_600606=obj.get_price('600606','绿地控股')
    df_000729=obj.get_price('000729','燕京啤酒')
    df_600023=obj.get_price('600023','浙能电力')
    df_600611=obj.get_price('600611','大众交通')
    df_600623=obj.get_price('600623','华谊集团')
    df_600755=obj.get_price('600755','厦门国贸')
    df_600011=obj.get_price('600011','华能国际')
    df_600027=obj.get_price('600027','华电国际')
    df_600170=obj.get_price('600170','上海建工')
    df_600823=obj.get_price('600823','世茂股份')
    df_000415=obj.get_price('000415','渤海金控')
    df_600028=obj.get_price('600028','中国石化')
###########
    df_600635=obj.get_price('600635','南方航空')
    df_600104=obj.get_price('600104','上汽集团') 
	

if __name__ == "__main__":
    start_time=datetime.datetime.now()
    main()
    end_time=datetime.datetime.now()
    print ("time use : ", (end_time-start_time).seconds,"s")
