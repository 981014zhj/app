import os
import  socket
import subprocess
import threading
import time

from woniu44.day27.cloud.onestr import OneStrokeTest


class AppiumCloud:
    def __init__(self):
        pass

    #通过一个list对象构建设备列表，包含设备编号，版本号，端口号
    def build_decive(self):
        list=[]
        port=5000
        bpport=8000
        devices=subprocess.check_output('adb devices').decode().strip().split('\r\n')
        for i in range(1,len(devices)):
            udid=devices[i].split('\t')[0]
            if udid!='':
                version=subprocess.check_output("adb -s "+udid+" shell getprop ro.build.version.release").decode().strip()
                port=self.find_port(port)
                bpport=self.find_port(bpport)
                list.append(udid+"##"+version+"##"+str(port)+"##"+str(bpport))
                bpport+=1
                port+=1
        return list

    def find_port(self,port):#寻找端口
        while True:
            if self.check_port(port):
                port+=1
            else:
                break
        return port

    def check_port(self,port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#基于传输层TCP协议
        try:
            s.connect('127.0.0.1',port)
            s.shutdown(2)
            return True
        except:
            return False

    def start_appium(self,udid,version,port,bpport):
        cmd="start /b appium -a 127.0.0.1 -p %s -bp %s --udid %s" \
            " --platform-version %s"%(port,bpport,udid,version)
        print(cmd)
        os.system(cmd)
        time.sleep(10)
        #直接调用测试脚本（见后面的测试脚本类OneStrokeTest）
        ost=OneStrokeTest()
        ost.start_test(udid,version,port)





if __name__ == '__main__':
    ac=AppiumCloud()
    devices=ac.build_decive()
    threads=[]
    for i in range(len(devices)):
        device_info=devices[i].split('##')
        udid=device_info[0]
        version=device_info[1]
        port=device_info[2]
        bpport=device_info[3]
        thread=threading.Thread(target=ac.start_appium,args=(udid,version,port,bpport))
        threads.append(thread)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    print("测试完成了")