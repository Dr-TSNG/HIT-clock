import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

print('初始化浏览器')
USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']
LOCATION   = os.environ['LOCATION']
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 MicroMessenger/6.3.27 NetType/WIFI Language/zh_CN'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
driver = webdriver.Chrome(executable_path= '/usr/bin/chromedriver', options = option)

date_string = time.strftime("%Y", time.localtime())+"年"+time.strftime("%m", time.localtime())+"月"+time.strftime("%d", time.localtime())+"日"
print('正在进行出校申请：',date_string)
driver.get('https://ids.hit.edu.cn/authserver/')
driver.find_element_by_id('mobileUsername').send_keys(USERNAME)
driver.find_element_by_id('mobilePassword').send_keys(PASSWORD)
driver.find_element_by_id('load').click()

success = False
for i in range (0, 5):
	try:
		driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsCxsq')
		driver.find_element_by_xpath("/html/body/div[2]/a/div").click()
		driver.find_element_by_xpath("/html/body/div[1]/div/div[9]/div/label[1]").click()
		driver.execute_script('document.getElementById("rqlscx").removeAttribute("readonly")')
		driver.find_element_by_xpath("/html/body/div[1]/div/div[12]/div[2]/input").send_keys(date_string)  # 填写日期
        driver.find_element_by_xpath("/html/body/div[1]/div/div[15]/textarea").send_keys("午饭晚饭西门外吃饭")  # 出校理由
        driver.find_element_by_xpath("/html/body/div[3]/div[1]/input").click()  # 勾选一堆东西
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[3]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[4]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[5]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[6]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[7]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[8]/input").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[9]/input").click()
        driver.find_element_by_xpath("/html/body/div[6]").click()  # 提交
		success = True
		break
	except:
		print('失败' + str(i+1) + '次，正在重试...')
driver.quit()
if success:
	print('离校申请完成')
else:
	raise Exception('离校申请多次失败，可能学工系统已更新')
