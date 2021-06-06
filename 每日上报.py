import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

print('初始化浏览器')
USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']
LOCATION   = os.environ['LOCATION']
driver = None
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.3.27 NetType/WIFI Language/zh_CN'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
driver = webdriver.Chrome(executable_path= '/usr/bin/chromedriver', options = option)

print('正在上报')
driver.get('https://ids.hit.edu.cn/authserver/')
driver.find_element_by_id('mobileUsername').send_keys(USERNAME)
driver.find_element_by_id('mobilePassword').send_keys(PASSWORD)
driver.find_element_by_id('load').click()
driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
driver.find_element_by_class_name('right_btn').click()
sleep(1)
alert = EC.alert_is_present()(driver)
if alert:
	alert.accept()
	driver.find_element_by_id('center').find_elements_by_tag_name('div')[5].click()
loc = driver.find_element_by_id('gnxxdz')
driver.execute_script('arguments[0].value="'+LOCATION+'"', loc)
driver.find_element_by_id('checkbox').click()
driver.execute_script('save()')
driver.execute_script('document.getElementsByClassName("weui-dialog__btn primary")[0].click()')

print('正在申请两天后出校')
# 直接访问会报错，因此通过每日上报间接访问
# driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsCxsq')
driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
driver.find_element_by_class_name('footer_img1').click()
sleep(1)
driver.execute_script('wjdc()')
sleep(1)
print(driver.current_url)
driver.find_element_by_class_name('right_btn').click() #
sleep(1)
alert = EC.alert_is_present()(driver)
if alert:
	alert.accept()
	driver.find_element_by_id('center').find_elements_by_tag_name('div')[5].click()

lx_type = driver.find_element_by_id('cxlx01')
driver.execute_script("arguments[0].checked = true;", lx_type)

time.timezone = -28800  # 北京时间
date = time.localtime(time.time() + 3600 * 24 * 2)
lx_date = driver.find_element_by_id('rqlscx')
driver.execute_script('arguments[0].value="%s年%s月%s日"'%(date.tm_year, date.tm_mon, date.tm_mday), lx_date)

lx_reason = driver.find_element_by_id('cxly')
driver.execute_script('arguments[0].value="吃饭"', lx_reason)

for i in range(1, 10):
	driver.find_element_by_id('checkbox%d'%i).click()
driver.execute_script('save()')
driver.execute_script('document.getElementsByClassName("weui-dialog__btn primary")[0].click()')

driver.quit()

print('上报完成')
