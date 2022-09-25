import os
import traceback
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import datetime
import random


reasons = ['吃饭','睡觉','去哈工大中心参观','看病']

# brower = webdriver.Chrome()
# brower.get('https://www.csdn.net/')
import os 

USERNAME = ''
PASSWORD = ''


ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 NetType/WIFI Language/zh_CN'
app = 'HuaWei-AnyOffice/1.0.0/cn.edu.hit.welink'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
driver = webdriver.Chrome(options=option)
# driver = webdriver.Chrome(executable_path= '/usr/local/bin/chromedriver', options = option)

driver.get('https://ids.hit.edu.cn/authserver/login')
driver.find_element(By.ID, 'username').send_keys(USERNAME)
driver.find_element(By.ID,'password').send_keys(PASSWORD)
driver.find_element(By.ID,'login_submit').click()

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua + ' ' + app})

def tryClick(id):
    try:
        driver.execute_script(f'document.getElementById("{id}").click()')
    except:
        print(f'No Such Checkbox:{id}')
        pass

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua + ' ' + app})


driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsCxsq/index')
driver.maximize_window()
driver.set_window_size(800,600)
driver.find_element(By.CLASS_NAME,'right_btn').click()
driver.find_element(By.XPATH,"//label[@for='cxlx01']").click()


jscode = 'document.getElementById("rqlscx").removeAttribute("readonly");'
driver.execute_script(jscode)
datestr = str(datetime.date.today().year)+'年'+str(datetime.date.today().month)+'月'+str(datetime.date.today().day)+'日'
driver.find_element(By.ID,'rqlscx').send_keys(datestr)
driver.find_element(By.ID,'cxly').send_keys(reasons[random.randint(0, 3)])
for i in range(1,10):
    tryClick(f'checkbox{i}')
driver.find_element(By.XPATH,"//div[@onclick='save()']").click()
sleep(1)
driver.find_element(By.XPATH,"//a[@class='weui-dialog__btn primary']").click()
sleep(5)
