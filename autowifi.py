# coding:utf-8
import time  #时间
import pywifi  #破解wifi
from pywifi import const  #引用一些定义
from asyncio.tasks import sleep
import sys

class AutoWifi():
    def __init__(self,path):
        self.accesslist=set()
        with open(path,"r",errors="ignore") as file:
            while True:
                pwd = file.readline()[:-1]
                if not pwd:
                    break
                self.accesslist.add(pwd)
                # print(pwd)
        for it in self.accesslist:
            print(it)
        wifi = pywifi.PyWiFi() #抓取网卡接口
        self.iface = wifi.interfaces()[0]#抓取第一个无限网卡

    def connect(self):
        self.iface.scan()
        time.sleep(1)
        # print(self.iface.status())
        result = self.iface.scan_results()
        if result is not None:
            for profile in result:
                ssid = profile.ssid
                if ssid in self.accesslist:
                    self.iface.connect(profile)
                    time.sleep(1)
                if self.iface.status()==const.IFACE_CONNECTED:
                    print('success connect')
                    break

    def getstatus(self,i):
        if i==const.IFACE_CONNECTED:
            return 'IFACE_CONNECTED'
        elif i==const.IFACE_CONNECTING:
            return 'IFACE_CONNECTING'
        elif i==const.IFACE_DISCONNECTED:
            return 'IFACE_DISCONNECTED'
        elif i==const.IFACE_INACTIVE:
            return 'IFACE_INACTIVE'
        elif i==const.IFACE_SCANNING:
            return 'IFACE_SCANNING'

    def start(self):
        print(self.getstatus(self.iface.status()))
        while True:
            # print('listening')
            if self.iface.status() in [const.IFACE_DISCONNECTED,const.IFACE_INACTIVE]:
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(localtime + ' found disconnect')
                self.connect()
            time.sleep(5)

if __name__ == "__main__":
    autowifi = AutoWifi('wifi.txt')
    autowifi.start()
