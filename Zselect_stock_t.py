# -*-coding=utf-8-*-
import sys
import tushare as ts
import pandas as pd
import os, sys, datetime, time,Queue, codecs
import numpy as np
from threading import Thread
from pandas import Series
q=Queue.Queue()
reload(sys)
sys.setdefaultencoding('utf-8')

pd.set_option('max_rows',None)
class select_class():
    def __init__(self):
        self.bases_save=ts.get_stock_basics()
        self.bases_save.to_csv('bases.csv')

        # 因为网速问题，手动从本地抓取
        self.today = time.strftime("%Y-%m-%d", time.localtime())
        self.base = pd.read_csv('bases.csv', dtype={'code': np.str})
        self.all_code = self.base['code'].values

    def get_pe(self,writeable=False):
        all_stock=ts.get_stock_basics()
        all_stock.to_csv('all_stock.csv')
        stock_online = pd.read_csv('all_stock.csv', dtype={'code': np.str})
        #两数相乘
        pepb= stock_online['pe']*stock_online['pb']
        #插入一个列至列表中
        stock_online['pepb']= pepb
#        stock_online.to_csv('zsd2.csv')
        #策略思想1，小于22.5倍
#        select_stock = stock_online.loc[(stock_online['pepb'] < 22.5) & (stock_online['pepb'] >0)]
#        select_stock.to_csv('select.csv',encoding='gbk')
        #策略思想2，pe小于15倍，pb小于1.5倍
        select_stock2 = stock_online.loc[(stock_online['pe'] < 15) & (stock_online['pe'] >0) & (stock_online['pb'] < 1.5) & (stock_online['gpr']!=0)]
        select_stock3 = stock_online.loc[(stock_online['pe'] < 15) & (stock_online['pe'] >0) & (stock_online['pb'] < 1.5) & (stock_online['gpr']!=0),["code","name","industry", "area","pe","pb"]]
        select_stock3.to_csv('select_stock_prod.csv',encoding='gbk')
#        select_stock2.to_csv('select_stock.csv',encoding='gbk')

        list_stock_code=select_stock2['code'].values
        for each in list_stock_code:
            print each
#           print type(each)
#        all_stock_growth=ts.get_growth_data(2015,4)
#        all_stock_growth.to_csv('stock_growth.csv',encoding='gbk')
#        stock_growth_online =pd.read_csv('stock_growth.csv', dtype={'code': np.str})
#        stock_growth_online2 =stock_growth_online.loc[stock_growth_online['code'] = list_stock_code]
#		stock_growth_online2.to_csv('stock_growth2.csv',encoding='gbk')
        return list_stock_code


def main():
    current = os.getcwd()
    folder = os.path.join(current, 'data')
    if os.path.exists(folder) == False:
        os.mkdir(folder)
    os.chdir(folder)

    obj = select_class()
    df=obj.get_pe()


if __name__ == "__main__":
    start_time=datetime.datetime.now()
    main()
    end_time=datetime.datetime.now()
    print "time use : ", (end_time-start_time).seconds,"s"
