from selenium import webdriver
from time import sleep

# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# driver = webdriver.Chrome(options=option)
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://weixin.sogou.com/weixin?type=2&s_from=input&query=lol&ie=utf8&_sug_=n&_sug_type_=')
elem = driver.find_element_by_xpath('//*[@class="news-list"]/li/div[2]/div/a').click()
# print(elem.get_attribute('href'))
# print(elem.click())
# print(elem)
sleep(15)
print(driver.page_source)
# print(driver.page_source)