import subprocess
import os
import threading
import time
class MonkeyCloud:
    def __init__(self):
        pass

    def build_device(self):
        list=[]
        devices=subprocess.check_output('adb devices').decode().strip().split("\r\n")
        for i in range(1,len(devices)):
            udid=devices[i].split("\t")[0]
            if udid!='':
                list.append(udid)
        return list

    #调用moneky命令进行测试
    def start_monkey(self,udid,package,count):
        cmd="adb -s %s shell monkey -p %s %d "%(udid,package,count)
        monkey_log=subprocess.check_output(cmd)

        #将日志信息写入到文件中
        log_file=os.path.abspath('.')+'\cloud'+udid.replace(':','.')+'.log'
        report=open(log_file,mode='w',encoding='utf8')
        #将monkey日志按照\r\r\n拆分为列表，并按行写入文件中
        monkey_list=str(monkey_log).split("\\r\\r\\n")
        for i in monkey_list:
            report.writelines(i+"\r\n")
        report.close()
        time.sleep(5)

        #gu关闭应用程序并打印结果
        os.system("adb -s %s shell am force-stop %s"%(udid,package))
        self.print_result(udid)

    def print_result(self,udid):
        log_path=os.path.abspath('.')+'\cloud'+udid.replace(':','.')+'.log'
        log_file=open(log_path,mode='r',encoding='utf8')
        content=log_file.read()

        if"crashed"in content or "Crash"in content:
            print("设备 %s: 出现了crashed异常 -FAILED"%udid)
        else:
            print("设备 %s: 出现了crashed异常 -PASSED"%udid)

        if"ANR"in content:
            print("设备 %s: 出现了ANR异常 -FAILED"%udid)
        else:
            print("设备 %s: 出现了ANR异常 -PASSED"%udid)
        log_file.close()
if __name__ == '__main__':
    mc=MonkeyCloud()
    devices=mc.build_device()
    print(devices)
    threads=[]
    package="com.miui.calculator"
    count=100
    for udid in devices:
        threads.append(threading.Thread(target=mc.start_monkey,args=(udid,package,count)))

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    print("测试完成")

