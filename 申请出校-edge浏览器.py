# @Time    : 2022-09-25 20:01
# @Author  : yink
# @Email   : yinkstudio@gmail.com

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from time import sleep

# 环境：selenium 4，使用前请先安装依赖~
# 使用前确认已经今日上报~(可配合每日上报脚本)

# 学号
USERNAME = 'your-username'
# 密码
PASSWORD = 'your-password'
# 出校理由
REASON = '出校购物'
# 停顿时间，如果运行失败请尝试增加该值，默认为2
SLEEPTIME = 2
# 要预约出校的日期，DAYS为1代表今天，为2代表明天，为3代表后天
DAYS = 2

# create driver
ua = UserAgent().edge
app = 'HuaWei-AnyOffice/1.0.0/cn.edu.hit.welink'
option = Options()
option.add_argument('user-agent='+ua)
driver = webdriver.Edge(EdgeChromiumDriverManager().install(),options=option)
driver.implicitly_wait(10)

# login
driver.get('https://ids.hit.edu.cn/authserver/login')
sleep(SLEEPTIME)
driver.find_element(By.ID, 'username').send_keys(USERNAME)
driver.find_element(By.ID,'password').send_keys(PASSWORD)
driver.find_element(By.ID,'login_submit').click()
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua + ' ' + app})

# try to click
def tryClick(id):
    try:
        driver.execute_script(f'document.getElementById("{id}").click()')
    except:
        print(f'No Such Checkbox:{id}')
        pass


# 申请出校
driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsCxsq/index')
sleep(SLEEPTIME)
driver.maximize_window()
driver.set_window_size(800,600)
driver.find_element(By.CLASS_NAME,'right_btn').click()

driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsCxsq/editCxsq?id=&zt=')
driver.find_element(By.XPATH,"//label[@for='cxlx01']").click()
driver.find_element(By.ID,"rqlscx").click()
sleep(1)
for i in range(1,DAYS):
    driver.find_elements(By.XPATH,"//div[@class='weui-picker__indicator']")[-1].click()
driver.find_element(By.LINK_TEXT,"确定").click()
sleep(0.5)
driver.find_element(By.XPATH,"//textarea[@placeholder='请如实填写出校理由及计划前往地点。']").send_keys(REASON)
for i in range(1,10):
    tryClick(f"checkbox{i}")
driver.find_element(By.XPATH,"//div[@onclick='save()']").click()
sleep(1)
driver.find_element(By.XPATH,"//a[@class='weui-dialog__btn primary']").click()
