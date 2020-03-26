# -*-coding=utf-8-*-
import sys
import tushare as ts
import pandas as pd
import os, sys, datetime, time, codecs
import numpy as np
from threading import Thread
from pandas import Series
import tushare as ts
from pyecharts.charts import Bar
from pyecharts import options as opts

class select_class():
    def __init__(self):

        # 因为网速问题，手动从本地抓取
        self.today = time.strftime("%Y-%m-%d", time.localtime())
    def get_price(self,stock_code,stock_name):
        stock_price = ts.get_hist_data(stock_code, ktype='M')
        stock_price.to_csv('stock_price.csv')
        price_online = pd.read_csv('stock_price.csv', dtype={'code': np.str})
        price_online_bf =price_online.loc[(price_online['open'] != 0),['date','open','high','close','low']]
        price_online_bf.to_csv('stock_price_online.csv')
        df = pd.read_csv('stock_price_online.csv')
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date') # 将date设置为index
        date_array=('2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010')
        date_list=['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
        min_array_list=[]
        max_array_list=[]
        mean_array_list=[]
        for each in date_array:
           price_min=df[each].low.min()
           min_array_list.append(price_min)
           price_max=df[each].high.max()
           max_array_list.append(price_max)
           price_mean=df[each].close.mean()
           mean_array_list.append(round(price_mean,2))
        own_dataframe={'date':date_list,'high':max_array_list,'low':min_array_list,'mean':mean_array_list}
        df2=pd.DataFrame(own_dataframe)
        Zdate = df2['date']
        print(df2['high'].tolist())
        print('---------stock code---------')
        print(stock_code)
        print(stock_name) 
        print('----------------------------')
        print(df2.sort_values(by='date'))
#       df2.to_csv(stock_code+stock_name + '.csv')
        bar = (
           Bar()
            .add_xaxis(["2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"])
            .add_yaxis("最高价", df2['high'].tolist())
            .add_yaxis("最低价", df2['low'].tolist())
            .add_yaxis("平均价", df2['mean'].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=stock_name))
        )
        bar.render(stock_code+stock_name+ '.html')

#        print(df.head(2))

def main():
    current = os.getcwd()
    folder = os.path.join(current, 'app/templates')
    if os.path.exists(folder) == False:
        os.mkdir(folder)
    os.chdir(folder)
    
    obj = select_class()
    df_601318=obj.get_price('601318','中国平安')
    df_601328=obj.get_price('601328','交通银行')
    df_600016=obj.get_price('600016','民生银行')
    df_000876=obj.get_price('000876','新希望')
    df_600606=obj.get_price('600606','绿地控股')
    df_600376=obj.get_price('600376','首开股份')
    df_600823=obj.get_price('600823','世茂股份')
    df_600068=obj.get_price('600068','葛洲坝')
    df_600623=obj.get_price('600623','华谊集团')
    df_600755=obj.get_price('600755','厦门国贸')
    df_600011=obj.get_price('600011','华能国际')
    df_600027=obj.get_price('600027','华电国际')
    df_000898=obj.get_price('000898','鞍钢股份')
    df_600019=obj.get_price('600019','宝钢股份')
    df_600028=obj.get_price('600028','中国石化')
###########
    df_600635=obj.get_price('600635','南方航空')
    df_600104=obj.get_price('600104','上汽集团')	

if __name__ == "__main__":
    start_time=datetime.datetime.now()
    main()
    end_time=datetime.datetime.now()
    print ("time use : ", (end_time-start_time).seconds,"s")
