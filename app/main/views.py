from flask import render_template, session, redirect, url_for, current_app
from .. import db
from .. models import User
from .. email import send_email
from . import main
from . forms import NameForm
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
from jinja2 import Markup

#def get_stock_name(stock_code):
#    stock_dict={"绿地控股":"600606","民生银行":"600016"}


def get_price(stock_code):
    stock_price = ts.get_hist_data(stock_code, ktype='M')
    stock_price.to_csv('stock_price.csv')
    price_online = pd.read_csv('stock_price.csv', dtype={'code': np.str})
    price_online_bf =price_online.loc[(price_online['open'] != 0),['date','open','high','close','low']]
    price_online_bf.to_csv('stock_price_online.csv')
    df = pd.read_csv('stock_price_online.csv')
#    print(df.head(2))
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date') # 将date设置为index
    date_array=('2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010')
    date_list=['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
    min_array_list=[]
    max_array_list=[]
    mean_array_list=[]
    for each in date_array:
#        print(df[each])
        price_min=df[each].low.min()
        min_array_list.append(price_min)
#        print(price_min)
        price_max=df[each].high.max()
#        print(price_max)
        max_array_list.append(price_max)
        price_mean=df[each].close.mean()
#        print(round(price_mean,2))
        mean_array_list.append(round(price_mean,2))
#        print(min_array_list)
    own_dataframe={'date':date_list,'high':max_array_list,'low':min_array_list,'mean':mean_array_list}
    df2=pd.DataFrame(own_dataframe)

    c = (
           Bar()
            .add_xaxis(["2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"])
            .add_yaxis("最高价", df2['high'].tolist())
            .add_yaxis("最低价", df2['low'].tolist())
            .add_yaxis("平均价", df2['mean'].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=stock_code))
    )
    return c

@main.route('/stock/<stock_code>')
def stocklist20(stock_code):
    c = get_price(stock_code)
    return render_template('index.html')
    return Markup(c.render_embed())
		

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['ZSD_ADMIN']:
                send_email(current_app.config['ZSD_ADMIN'],'新用户来了','mail/new_user',user=user)
        else :
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'),known =session.get('known',False))
