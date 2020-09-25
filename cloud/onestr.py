import time
from appium import webdriver
import os

class OneStrokeTest:
    def __init__(self):
        self.driver=None
        self.desired_caps={}

    def start_test(self,udid,version,port):
        self.desired_caps={}
        self.desired_caps['platformName']='Android'
        self.desired_caps['platformVersion']=version
        self.desired_caps['deviceName']='Appium'
        self.desired_caps['unicodeKeyboard']=True
        self.desired_caps['noReset']=True
        self.desired_caps['appPackage']='com.miui.calculator'
        self.desired_caps['appActivity']='.cal.CalculatorActivity'#应用程序线程名
        self.desired_caps['udid']=udid
        app_path=os.path.abspath('.')+ '\com.miui.calculator.apk'
        self.desired_caps['app']=app_path
        self.driver=webdriver.Remote('http://127.0.0.1:'+port+'/wd/hub',self.desired_caps)
        time.sleep(10)
        self.driver.find_element_by_id('com.miui.calculator:id/btn_7_s').click()
        ele1=self.driver.find_element_by_id('com.miui.calculator:id/btn_7_s')
        ll=ele1.get_attribute("text")
        self.driver.find_element_by_id('com.miui.calculator:id/btn_plus_s').click()
        self.driver.find_element_by_id('com.miui.calculator:id/btn_7_s').click()
        ele2=self.driver.find_element_by_id('com.miui.calculator:id/btn_7_s')
        le=ele2.get_attribute("text")
        self.driver.find_element_by_id('com.miui.calculator:id/btn_equal_s').click()
        time.sleep(5)
        ele3=self.driver.find_element_by_id('com.miui.calculator:id/result')
        lr=ele3.get_attribute("text")
        lr1=lr.split("= ")
        if int(le)+int(ll)==int(lr1[1]):
            print("pass")
        else:
            print('fail')
        self.driver.quit()
