# -*-coding=utf-8-*-
import sys
import tushare as ts
import pandas as pd
import os, sys, datetime, time,Queue, codecs
import numpy as np
from threading import Thread
from pandas import Series
import tushare as ts

reload(sys)
sys.setdefaultencoding('utf-8')
class select_class():
    def __init__(self):
#        self.bases_save=ts.get_stock_basics()
#        self.bases_save.to_csv('bases.csv')

        # 因为网速问题，手动从本地抓取
        self.today = time.strftime("%Y-%m-%d", time.localtime())
#        self.base = pd.read_csv('bases.csv', dtype={'code': np.str})
#        self.all_code = self.base['code'].values
    def get_price(self,stock_code,stock_name):
        stock_price = ts.get_hist_data(stock_code, ktype='M')
        stock_price.to_csv('stock_price.csv')
        price_online = pd.read_csv('stock_price.csv', dtype={'code': np.str})
        price_online_bf =price_online.loc[(price_online['open'] != 0),['date','open','high','close','low']]
        price_online_bf.to_csv('stock_price_online.csv')
        df = pd.read_csv('stock_price_online.csv')
#        print(df.head(2))
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date') # 将date设置为index
#----------测试语句------Dataframe的数据类型
#        print(df.head(2))
#        print(df.tail(2))
#        print(df.shape)
#        print(type(df))
#        print(df.index)
#        print(type(df.index))
        date_array=('2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998','1997','1996','1995','1994','1993')
        date_list=['2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998','1997','1996','1995','1994','1993']
#        print(date_array)
        min_array_list=[]
        max_array_list=[]
        mean_array_list=[]
        for each in date_array:
#           print each
#          print(df[each])
           price_min=df[each].low.min()
           min_array_list.append(price_min)
#           print(price_min)
           price_max=df[each].high.max()
#           print(price_max)
           max_array_list.append(price_max)
           price_mean=df[each].close.mean()
#           print(round(price_mean,2))
           mean_array_list.append(round(price_mean,2))
#        print(min_array_list)
        own_dataframe={'date':date_list,'high':max_array_list,'low':min_array_list,'mean':mean_array_list}
#       '平均价':mean_array_list,
        df2=pd.DataFrame(own_dataframe)
#       时间日期为第一列
#        Zdate = df2['date']
#        df2.drop(labels=['date'], axis=1,inplace = True)
#        df2.insert(0, 'date', Zdate)
        print '---------stock code---------'
        print(stock_code)
        print(unicode(stock_name,"utf-8")) 
        print '----------------------------'
        print(df2.sort_values(by='date'))
        df2.to_csv(stock_code+unicode(stock_name,"utf-8") + '.csv')
#        print(df.head(2))

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
    df_000589=obj.get_price('000589','黔轮胎A')
    df_600635=obj.get_price('600635','大众公用')

if __name__ == "__main__":
    start_time=datetime.datetime.now()
    main()
    end_time=datetime.datetime.now()
    print "time use : ", (end_time-start_time).seconds,"s"
