#-*-coding=utf-8-*-
__author__ = 'zhangshengdong'
'''
个人技术博客:http://blog.chinaunix.net/uid/26446098.html
联系方式: sdzhang@cashq.ac.cn
'''
import os
import time
import sys
import smtplib
import logging
import logging.config
import tushare as ts
from Ztoolkit import Toolkit as TK
from email.mime.text import MIMEText
from email import Encoders, Utils

reload(sys)
sys.setdefaultencoding('utf8')
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('stock_memssage')

class MailSend():
    def __init__(self, smtp_server, from_mail, password, to_mail):
        self.server = smtp_server
        self.username = from_mail.split("@")[0]
        self.from_mail = from_mail
        self.password = password
        self.to_mail = to_mail

    def send_txt(self, name, real_price,price, percent, status):
        if 'up' == status:
#            content = 'stock name:%s current price: %.2f higher than price up:%.2f , ratio:%.2f' % (name, real_price,price, percent)
             content = '证券名称:%s 当前价格: %.2f 高于 定价模型上限价格:%.2f , 可卖出 预计盈利率:%.2f' %(name, real_price,price, percent+15)
        if 'down' == status:
#            content = 'stock name:%s current price: %.2f lower than price down:%.2f , 盈利率:%.2f' % (name, real_price,price, percent)
             content = '证券名称:%s 当前价格: %.2f 低于 定价模型下限价格:%.2f , 可买入 预计盈利率:%.2f' %(name, real_price,price, percent+15)
        content = content + '%'
        print content
        subject = '%s' % name
        self.msg = MIMEText(content, 'plain', 'utf-8')
        self.msg['to'] = self.to_mail
        self.msg['from'] = self.from_mail
        self.msg['Subject'] = subject
        self.msg['Date'] = Utils.formatdate(localtime=1)
        try:

            self.smtp = smtplib.SMTP_SSL(port=465)
            self.smtp.connect(self.server)
            self.smtp.login(self.username, self.password)
            self.smtp.sendmail(self.msg['from'], self.msg['to'], self.msg.as_string())
            self.smtp.quit()
            print "sent"
        except smtplib.SMTPException, e:
            print e
            return 0

def push_msg(name, real_price,price, percent, status):
    cfg = TK.getUserData('data.cfg')
    from_mail = cfg['from_mail']
    password = cfg['password']
    to_mail = cfg['to_mail']
    obj = MailSend('smtp.qq.com', from_mail, password, to_mail)
    obj.send_txt(name,real_price, price, percent, status)

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

def compare_price(code, price_down, price_up):
    try:
        df = ts.get_realtime_quotes(code)
    except Exception, e:
        print e
        time.sleep(5)
        return 0
    real_price = df['price'].values[0]
    name = df['name'].values[0]
    real_price = float(real_price)
    pre_close = float(df['pre_close'].values[0])
    time.sleep(1)
    logger.info('证券名称:%s 当前价格:%.2f ,昨日收盘价:%.2f', name, real_price,pre_close)
    if real_price == 0:
        print '%s real_price %.2f is zero,go on' % (name, real_price),
        return 0
    if real_price >= price_up:
        percent_up = (real_price - price_up) / price_up * 100
        print 'percent : %.2f\n' % (percent_up),
        print '%s real_price %.2f higher than price_up %.2f , %.2f' % (name, real_price, price_up,percent_up),
        print '%'
        push_msg(name, real_price,price_up, percent_up, 'up')
        return 1
    if real_price <= price_down:
        percent_down = (price_down - real_price) / price_down * 100
        print '%s real_price %.2f lower than price_down %.2f , %.2f' % (name, real_price, price_down,percent_down),
        print '%'
        push_msg(name, real_price,price_down, percent_down, 'down')
        return 1

def main():
    #read_stock('price.txt')
    # choice = input("Input your choice:\n")

    # if str(choice) == '1':
        stock_lists_price = read_stock('price.txt')
        while 1:
            t = 0
            for each_stock in stock_lists_price:
                code = each_stock[0]
                price_down = float(each_stock[1])
                price_up = float(each_stock[2])
                t = compare_price(code, price_down, price_up)
                if t:
                    stock_lists_price.remove(each_stock)

if __name__ == '__main__':
    path=os.path.join(os.getcwd(),'data')
    if os.path.exists(path)==False:
         os.mkdir(path)
    os.chdir(path)

    main()
