#-*-coding=utf-8-*-
__author__ = 'zhangshengdong'
'''
个人技术博客:http://blog.chinaunix.net/uid/26446098.html
联系方式: sdzhang@cashq.ac.cn
'''
import sys
import tushare as ts
import pandas as pd
import os, sys, datetime, time,Queue, codecs
import numpy as np
from threading import Thread
from pandas import Series
import tushare as ts

reload(sys)
sys.setdefaultencoding('utf8')

def read_stock(name):
    f = open(name)
    stock_list = []

    for s in f.readlines():
        s = s.strip()
        row = s.split(';')
         #print row
        print "code :",row[0]
        print "price_down :",row[1]
        print "price_up :",row[2]
        stock_list.append(row)
    return stock_list

def main():
        code_array_list=[]
        price_d_array_list=[]
        price_up_array_list=[]
        profit_array_list=[]
        stock_array_list=[]
        stock_lists_price = read_stock('price.txt')
        for each_stock in stock_lists_price:
                code = each_stock[0]
                code_array_list.append(code)
                price_down = float(each_stock[1])
                price_d_array_list.append(price_down)
                price_up = float(each_stock[2])
                price_up_array_list.append(price_up)
                stock_name=each_stock[3]
                stock_array_list.append(stock_name)
                profit=price_up/price_down
                profit_array_list.append(round(profit,2))
        own_dataframe={'code':code_array_list,'price_d':price_d_array_list,'price_up':price_up_array_list,'stock_name':stock_array_list,'profit':profit_array_list}
        df2=pd.DataFrame(own_dataframe)
        print(df2)
        df2.to_csv('stock_profit.csv',encoding='utf_8_sig')


if __name__ == '__main__':
    path=os.path.join(os.getcwd(),'data')
    if os.path.exists(path)==False:
         os.mkdir(path)
    os.chdir(path)

    main()
