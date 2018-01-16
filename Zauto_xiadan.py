#coding=utf-8
#!/usr/bin/python
import pyautogui
import os
import time
import pywinauto
import pywinauto.clipboard
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
            self._app = pywinauto.Application().connect(path=self._run_exe_path(exe_path), timeout=1)
        except Exception:
            self._app = pywinauto.Application().start(exe_path)

            self._app.top_window().Edit1.type_keys(user)
            self._app.top_window().Edit2.type_keys(password)

            self._app.top_window().Edit3.type_keys(comm_password)

            self._app.top_window().type_keys('%Y')

            # detect login is success or not
            self._app.top_window().wait_not('exists', 10)
    def buy(self,code,count):
       self._app.top_window().Edit1.type_keys(code)
       self._app.top_window().Edit2.type_keys('')
       self._app.top_window().Edit3.type_keys(count)
       pyautogui.typewrite(['B'], interval=secs_between_keys)
       pyautogui.typewrite(['Y'], interval=secs_between_keys)

if __name__ == "__main__":
#######华泰客户端登录
    app_dir = r'C:\htzqzyb2\xiadan.exe'
    user='xxxxxx'
    passwd='xxxx'
    comm_password='xxxxxxxxx'
    app=HTClientTrader()
    app.login(user,passwd,app_dir,comm_password)
    secs_between_keys = 0.5
    pyautogui.typewrite(['f1'], interval=secs_between_keys)
    app.buy('600170',500)
    time.sleep(5)
    
    os.system("taskkill /F /IM xiadan.exe")
