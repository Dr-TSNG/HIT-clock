import os
import traceback
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

print('初始化浏览器')
USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']
LOCATION   = os.environ['LOCATION']
wechat_ua= 'Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2889 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/3915 MicroMessenger/8.0.15.2001(0x28000F41) Process/toolsmp WeChat/arm64 Weixin GPVersion/1 NetType/WIFI Language/zh_CN ABI/arm64'
ua =wechat_ua
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
driver = webdriver.Chrome(executable_path= '/usr/bin/chromedriver', options = option)
#driver = webdriver.Chrome(executable_path= './chromedriver.exe', options = option)    #windows
print('正在上报')
driver.get('https://sso.hitsz.edu.cn:7002/cas/login')
driver.find_element(By.ID,'username').send_keys(USERNAME)
driver.find_element(By.ID,'password').send_keys(PASSWORD)
#submit login
driver.find_element_by_xpath("//*[contains(text(),'登录')]").click()

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua})

def tryClick(id):
	try:
		driver.execute_script(f'document.getElementById("{id}").click()')
	except:
		print(f'No such checkbox: {id}')
		pass

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua})

success = False
for i in range (0, 5):
	try:
		driver.get('https://student.hitsz.edu.cn/xg_mobile/xsMrsbNew/edit')
		driver.execute_script(f'kzl10 = "{LOCATION}"')

		tryClick("txfscheckbox")  # 承诺：本人已了解填写此登记表的目的及其严肃性，承诺填报信息全部真实可靠

		driver.find_element_by_class_name('submit').click()
		success = True
		break
	except:
		traceback.print_exc()
		print('失败' + str(i+1) + '次，正在重试...')
driver.quit()
if success:
	print('上报完成')
else:
	raise Exception('上报多次失败，可能学工系统已更新')