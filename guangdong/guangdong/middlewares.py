# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import random
import settings
from selenium.webdriver.support.wait import WebDriverWait   # 等待对象
from selenium.webdriver.support import expected_conditions as EC   # 条件
from selenium.webdriver.common.by import By # 定义定位器的常量
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class GuangdongSpiderMiddleware:
    def __init__(self):
        super(GuangdongSpiderMiddleware, self).__init__()
        option = webdriver.ChromeOptions()

        option.add_argument('--disable-gpu')
        option.add_argument('lang=zh_CN.UTF-8')

        prefs = {
            "profile.managed_default_content_settings.images": 2,  # 禁止加载图片
            # 'permissions.default.stylesheet': 2,  # 禁止加载css
        }
        option.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(chrome_options=option)

        self.wait = WebDriverWait(self.browser, 20)

        self.browser.execute_script('window.open("","_blank");')
        self.locator= (By.CSS_SELECTOR, 'tbody')
        self.detailocator=(By.CLASS_NAME,'article-content')
        self.locator2=(By.CLASS_NAME,'pagination')

    def process_request(self, request, spider):

        user_agent = random.choice(settings.USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            print(f"User-Agent:{user_agent}")

        print('asdasdasdasdas'+request.url)
        if request.url == 'https://www.gd.gov.cn/gkmlpt/policy':
            if request.meta['tmp'] == 1:
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.browser.get(request.url)
                res = self.wait.until(EC.presence_of_all_elements_located((self.locator)))
                time.sleep(random.randint(3, 5))
            else:
                self.browser.switch_to.window(self.browser.window_handles[0])
                if request.meta['tmp'] <= 237:
                    print("MAIN PAGE CHANGE : " + str(request.meta['tmp']) + " / " + str(237))
                    self.browser.find_element_by_class_name('next').click()
                    res = self.wait.until(EC.presence_of_all_elements_located((self.locator2)))
                    time.sleep(random.randint(5, 7))

                else:
                    return None
        else:
            print("NEW PAGE GET : " + request.url)
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.get(request.url)
            res = self.wait.until(EC.presence_of_all_elements_located((self.detailocator)))

            time.sleep(random.randint(3,5))
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8",
                            request=request)

