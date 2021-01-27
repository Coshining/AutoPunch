from time import sleep

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as NSEEC
from selenium.webdriver.chrome.options import Options

import SendQQEmail
import BaiDuOCR


class AutoSignIn():
    def __init__(self):
        self.codeCnt = 0
        self.refreshCnt = 0
        self.result = True

        chrome_options = Options()
        # 服务器上运行这几个参数必须要
        chrome_options.add_argument('--headless')  # 隐藏模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)  # 创建Chrome对象

    def start(self):
        self.login()
        if (self.result):
            self.codeInput()
        if (self.result):
            self.fillInForm()
        self.driver.quit()

    def login(self):
        # 操作这个对象
        try:
            self.driver.get('https://xxxxxx')  # get方式访问
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[1]/input').send_keys("xxxxx")  # 账号
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[2]/input').send_keys("xxxxxx")  # 密码
        except NSEEC:
            SendQQEmail.failure("打卡失败！", "001：\n\t登录页面找不到输入账号密码的输入框元素！")
            self.result = False

    # 验证码输入
    def codeInput(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[3]/div/input').send_keys(
                self.getVerifyCode())  # 验证码
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/button').click()  # 登录
        except NSEEC:
            SendQQEmail.failure("打卡失败！", "002：\n\t登录页面找不到验证码的输入框元素和登录按钮元素！")
            self.result = False
        sleep(0.5)  # 等待确保显示
        if self.isElementPresent("el-message--warning"):  # 如果有弹窗warning，则验证码错误
            self.codeCnt += 1
            if (self.codeCnt == 20):
                SendQQEmail.failure("打卡失败！", "003：\n\t验证码输入错误超过20次！")
                self.result = False
            else:
                # print("验证码错误")
                sleep(2)  # 等待前一个消除
                self.codeInput()

        # print("通过")

    # 获取验证码
    def getVerifyCode(self):
        self.driver.find_element_by_class_name('vcdoe-tips').click()
        sleep(1)  # 防止直接刷不出来验证码

        codeJpg = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[3]/img').get_property('src')
        # print(codeJpg)
        r = requests.get(codeJpg)
        # 将获取到的图片二进制流写入本地文件
        with open('imagevcode.jpg', 'wb') as f:
            # 对于图片类型的通过r.content方式访问响应内容，将响应内容写入imagevcode.jpg中
            f.write(r.content)

        # 识别
        verifyCode = BaiDuOCR.img_to_str('./imagevcode.jpg')
        # print(verifyCode)
        return verifyCode

    # 封装一个函数，用来判断属性值是否存在
    def isElementPresent(self, value):
        """
        用来判断元素标签是否存在，
        """
        try:
            self.driver.find_element_by_class_name(value)
        # 原文是except NoSuchElementException, e:
        except NSEEC as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    # 填充
    def fillInForm(self):
        self.refreshCnt += 1
        sleep(5)  # 等待提示消失
        try:
            # 地区选择
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]').click()
            sleep(0.5)
            # 选择省
            province = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[2]/div[1]/ul')
            self.driver.execute_script(
                "arguments[0].style = 'transform: translate3d(0px, -308px, 0px); transition-duration: 0ms; transition-property: none; line-height: 44px';",
                province)
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[2]/div[1]/ul/li[10]').click()
            sleep(0.5)
            # 选择市
            city = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[2]/div[2]/ul')
            self.driver.execute_script(
                "arguments[0].style = 'transform: translate3d(0px, -44px, 0px); transition-duration: 0ms; transition-property: none; line-height: 44px';",
                city)
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[2]/div[2]/ul/li[4]').click()
            sleep(0.5)
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/div/div[1]/button[2]').click()  # 确定
            sleep(0.5)

            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div[3]/div[2]/div/input').send_keys(
                "xxxxx")  # 详细地址
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[3]/div[2]/div[2]').click()  # 在校：否
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[4]/div[2]/div[1]').click()  # 体温正常：是
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[5]/div[2]/div[2]').click()  # 家人没从危险地区返回
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[6]/div[2]/div[2]').click()  # 家人没不良反应
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[7]/div[2]/div[2]').click()  # 家人没接触过疑似

            sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/button').click()  # 打卡
            sleep(0.5)
        except NSEEC:
            SendQQEmail.failure("打卡失败！", "004：\n\t填入信息页面出错或者已打卡！")
            self.result = False

        if self.isElementPresent("el-message--success"):  # 签到成功
            SendQQEmail.success()
        elif self.result:
            self.driver.refresh()
            if (self.refreshCnt == 10):
                SendQQEmail.failure("打卡失败！", "005：\n\t填入表单页面刷新超过10次！")
            else:
                self.fillInForm()
