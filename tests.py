# testing
# run_crawler(search_engine_name='bing', search_phrase='atlantic ocean', page_depth_num=3, max_search_num=10)


# for google // captcha issue
# get the search engine website
# driver.get(url='https://www.google.com/')

# time.sleep(5)
# search_bar = driver.find_element(By.NAME, 'q')
# search_bar.send_keys('hakuna matata', Keys.ENTER)

# # link = driver.find_element(By.CSS_SELECTOR, '.yuRUbf a')
# title = driver.find_element(By.CSS_SELECTOR, '.yuRUbf a h3')

# # print(link.text)
# print(title.text)

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
