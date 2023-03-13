import selenium, random, pandas as pd, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# testing
# run_crawler(search_engine_name='bing', search_phrase='atlantic ocean', page_depth_num=3, max_search_num=10)

driver = webdriver.Chrome()

wait = WebDriverWait(driver=driver, timeout=120.0)
# for google // captcha issue
# get the search engine website
driver.get(url='https://www.lycos.com/')

# time.sleep(5)
search_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-input')))
search_bar.send_keys('stem', Keys.ENTER)

# link = driver.find_element(By.CSS_SELECTOR, '.yuRUbf a')
title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result-title a')))

print(title.get_attribute('href'))
print(title.text)

next = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Next')))
next.click()

time.sleep(5)

# for yandex //captcha issue
# get the search engine website
# driver.get(url='https://yandex.com/')

# # time.sleep(5)
# search_bar = driver.find_element(By.CSS_SELECTOR, '.input__input')
# search_bar.send_keys('hakuna matata', Keys.ENTER)

# # link = driver.find_element(By.CSS_SELECTOR, '.relsrch .title a')
# title = driver.find_element(By.CSS_SELECTOR, '.organic__title-wrapper a')

# print(title.get_attribute('href'))
# print(title.text)

# for dogpile //captcha issues
# get the search engine website
# driver.get(url='https://www.dogpile.com/')

# time.sleep(60)
# search_bar = driver.find_element(By.CSS_SELECTOR, '.search-form-home__q')
# search_bar.send_keys('hakuna matata', Keys.ENTER)

# # link = driver.find_element(By.CSS_SELECTOR, '.relsrch .title a')
# title = driver.find_element(By.CSS_SELECTOR, '.web-bing__title')

# print(title.get_attribute('href'))
# print(title.text)
