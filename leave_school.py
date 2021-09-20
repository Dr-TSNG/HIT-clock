import time
import os
from selenium import webdriver
import datetime
import pytz

date_string = datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y")+"年"+datetime.datetime.now(pytz.timezone('PRC')).strftime("%m")+"月"+datetime.datetime.now(pytz.timezone('PRC')).strftime("%d")+"日"
# date_string = "2021年9月20日"
print('初始化浏览器')
USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
browser = webdriver.Chrome(executable_path= '/usr/bin/chromedriver', options = option)
browser.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange')
# 将窗口最大化
browser.maximize_window()
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[1]/div[2]/button[1]').click()
time.sleep(1)
browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[1]/input").send_keys(USERNAME)
time.sleep(1)
browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]").send_keys(PASSWORD)
time.sleep(1)
browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[5]/button").click()

time.sleep(1)
browser.find_element_by_xpath("/html/body/div[1]/div[6]/a[3]").click()  # 出入校申请
#
time.sleep(1)
# browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]").click()  # 新增
browser.find_element_by_xpath("/html/body/div[2]/a/div").click()  # 新增
time.sleep(1)
# browser.switch_to.alert.accept()
time.sleep(1)
# browser.find_element_by_xpath("/html/body/div[1]/div/div[9]/div/label[1]").click()  # 勾选临时出校
# browser.find_element_by_xpath("/html/body/div[1]/div/div/label[1]").click()  # 勾选临时出校
browser.execute_script('document.getElementById("cxlx01").click()')
time.sleep(1)
js = "document.getElementById('rqlscx').removeAttribute('readonly')"
browser.execute_script(js)
browser.find_element_by_xpath("/html/body/div[1]/div/div[12]/div[2]/input").send_keys(date_string)  # 填写日期
browser.find_element_by_xpath("/html/body/div[1]/div/div[15]/textarea").send_keys("午饭晚饭西门外吃饭")  # 出校理由
browser.find_element_by_xpath("/html/body/div[3]/div[1]/input").click()  # 勾选一堆东西
browser.find_element_by_xpath("/html/body/div[3]/div[2]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[3]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[4]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[5]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[6]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[7]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[8]/input").click()
browser.find_element_by_xpath("/html/body/div[3]/div[9]/input").click()
browser.find_element_by_xpath("/html/body/div[6]").click()  # 提交

time.sleep(1)
browser.find_element_by_xpath("/html/body/div[11]/div[3]/a[2]").click()
time.sleep(1)
print(date_string + "出校申请成功")

browser.quit()

