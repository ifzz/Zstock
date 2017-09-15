# -*-coding=utf-8-*-
__author__ = 'zhangshengdong'
'''
个人技术博客:http://blog.chinaunix.net/uid/26446098.html
联系方式: sdzhang@cashq.ac.cn
'''
class Toolkit():

    @staticmethod
    def getUserData(cfg_file):
        f=open(cfg_file,'r')
        account={}
        for i in f.readlines():
            ctype,passwd=i.split('=')
            #print ctype
            #print passwd
            account[ctype.strip()]=passwd.strip()
        return account