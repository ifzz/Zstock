#coding=utf-8
#!/usr/bin/python
import pyautogui
import os
import time
import pywinauto
import pywinauto.clipboard
import logging
import logging.config
import tushare as ts
import sys

reload(sys)
sys.setdefaultencoding('utf8')
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('stock_memssage')

class HTClientTrader():
    @property
    def broker_type(self):
        return 'ht'
    def login(self, user, password, exe_path, comm_password=None):
        """
        :param user: 用户名
        :param password: 密码
        :param exe_path: 客户端路径
        :param comm_password:
        :return:
        """
        if comm_password is None:
            raise ValueError('华泰客户端必须设置通讯密码')

        try:
            self._app = pywinauto.Application().connect(path=self._run_exe_path(exe_path), timeout=0.5)
        except Exception:
            self._app = pywinauto.Application().start(exe_path)

            self._app.top_window().Edit1.type_keys(user)
            self._app.top_window().Edit2.type_keys(password)

            self._app.top_window().Edit3.type_keys(comm_password)

            self._app.top_window().type_keys('%Y')

            # detect login is success or not
            self._app.top_window().wait_not('exists', 10)
    def buy(self, code, price, count,secs_between_keys):
#       self._app.top_window().Edit1.type_keys(code)
#       self._app.top_window().Edit2.type_keys('')
       pyautogui.typewrite(code, interval=secs_between_keys)
       pyautogui.typewrite(['tab'], interval=secs_between_keys)
       pyautogui.typewrite(['backspace'], interval=secs_between_keys)
       pyautogui.typewrite(['backspace'], interval=secs_between_keys)
       pyautogui.typewrite(['backspace'], interval=secs_between_keys)
       pyautogui.typewrite(['backspace'], interval=secs_between_keys)
       pyautogui.typewrite(['backspace'], interval=secs_between_keys)
#      self._app.top_window().Edit2.type_keys(price)
       pyautogui.typewrite(price, interval=secs_between_keys)
       pyautogui.typewrite(['tab'], interval=secs_between_keys)
#      self._app.top_window().Edit3.type_keys(count)
       pyautogui.typewrite(count, interval=secs_between_keys)
       pyautogui.typewrite(['tab'], interval=secs_between_keys)
       pyautogui.typewrite(['B'], interval=secs_between_keys)
       pyautogui.typewrite(['Y'], interval=secs_between_keys)

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
        return 1
    if real_price <= price_down:
        percent_down = (price_down - real_price) / price_down * 100
        print '%s real_price %.2f lower than price_down %.2f , %.2f' % (name, real_price, price_down,percent_down),
        print '%'
        app_dir = r'C:\htzqzyb2\xiadan.exe'
        user='xxx'
        passwd='xxx'
        comm_password='xxx@7101'
        app=HTClientTrader()
        app.login(user,passwd,app_dir,comm_password)
        secs_between_keys = 1
        pyautogui.typewrite(['f1'], interval=secs_between_keys)
        real_price = str(real_price)
        app.buy(code,real_price, '500',0.05)
        time.sleep(5)
        os.system("taskkill /F /IM xiadan.exe")
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
