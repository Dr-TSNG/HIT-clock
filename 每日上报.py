import os
import traceback
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from PIL import Image
import ddddocr

print('初始化浏览器')
USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']
LOCATION   = os.environ['LOCATION']
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 NetType/WIFI Language/zh_CN'
app = 'HuaWei-AnyOffice/1.0.0/cn.edu.hit.welink'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
driver = webdriver.Chrome(executable_path= '/usr/bin/chromedriver', options = option)

print('正在上报')
driver.get('https://ids.hit.edu.cn/authserver/login')
driver.find_element(By.ID, 'username').send_keys(USERNAME)
driver.find_element(By.ID,'password').send_keys(PASSWORD)
driver.find_element(By.ID,'login_submit').click()

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua + ' ' + app})

def tryClick(id):
	try:
		driver.execute_script(f'document.getElementById("{id}").click()')
	except:
		print(f'No such checkbox: {id}')
		pass

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua + ' ' + app})


def yzm():
	try:
		# 获取验证码
		# 获取验证码
		operation = True
		counter = 0
		while (operation):
			if counter > 5:
				operation = False
			WebDriverWait(driver, 10).until(
                		EC.presence_of_element_located((By.XPATH, "//*[@id='imgObjjgRegist']")))
			imgelement = driver.find_elements(By.XPATH, '//*[@id="imgObjjgRegist"]')  # 定位验证码
			if not imgelement:
				return
			try:
				imgelement[0].screenshot('./save.png')
			except Exception as e:
				print("截图失败")
				print(e)
				counter += 1
				continue
			# 验证码识别
			ocr = ddddocr.DdddOcr()
			with open('./save.png', 'rb') as f:
				img_bytes = f.read()
				res = ocr.classification(img_bytes)
			f.close()
			print(res)
			driver.find_element(By.ID,'yzm').send_keys(res)
			driver.find_element(By.ID,'pass-dialog').click()

			counter += 1
			sleep(1)
			if not driver.find_elements(By.CLASS_NAME, "weui-toptips_warn"):
				operation = False
	except Exception as e:
		print("验证码处理失败")
		print(e)

success = False
for i in range (0, 5):
	try:
		driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew/edit')
		driver.maximize_window()
		driver.set_window_size(800, 600)
		driver.execute_script(f'kzl10 = "{LOCATION}"')
# 		driver.execute_script('document.getElementById("kzl18-0").checked = true')
# 		driver.execute_script('document.getElementById("kzl32-2").checked = true')
		tryClick("txfscheckbox")
		tryClick("txfscheckbox1")
		tryClick("txfscheckbox2")
		tryClick("txfscheckbox3")
		driver.find_element(By.CLASS_NAME, 'submit').click()
		sleep(5) # 防止有验证码没加载
		yzm()
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
