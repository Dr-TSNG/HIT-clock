import os
import traceback
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
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
driver.find_element_by_id('username').send_keys(USERNAME)
driver.find_element_by_id('password').send_keys(PASSWORD)
driver.find_element_by_id('login_submit').click()

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
		driver.save_screenshot('E:\\printscreen.png') 
		imgelement = driver.find_element_by_xpath('//*[@id="imgObjjgRegist"]')  # 定位验证码
		location = imgelement.location  # 获取验证码x,y轴坐标
		size = imgelement.size  # 获取验证码的长宽
		rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
			  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
		i = Image.open("E:\\printscreen.png")
		frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
		frame4.save('E:\\save.jpg') # 保存我们接下来的验证码图片 进行打码
		
		# 验证码识别
		ocr = ddddocr.DdddOcr()
		with open('./save.png', 'rb') as f:
    			img_bytes = f.read()
			res = ocr.classification(img_bytes)
		driver.find_element_by_id('yzm').send_keys(res)
		driver.find_element_by_id('pass-dialog').click()
	except Exception as e:
		print(e)

success = False
for i in range (0, 5):
	try:
		driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew/edit')
		driver.execute_script(f'kzl10 = "{LOCATION}"')
# 		driver.execute_script('document.getElementById("kzl18-0").checked = true')
# 		driver.execute_script('document.getElementById("kzl32-2").checked = true')
		tryClick("txfscheckbox")
		tryClick("txfscheckbox1")
		tryClick("txfscheckbox2")
		tryClick("txfscheckbox3")
		driver.find_element_by_class_name('submit').click()
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
