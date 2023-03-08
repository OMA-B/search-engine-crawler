import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# set up driver
driver = webdriver.Chrome()

def scrape_web(search_engine, URL, input_selector, keyword, search_result_title, next_selector, max_search_num):
    # get the search engine website
    driver.get(url=URL)

    # time.sleep(5)
    search_bar = driver.find_element(input_selector[0], input_selector[1])
    search_bar.send_keys(keyword, Keys.ENTER)

    titles = []

    # fetch 100+ results
    if 'duckduckgo' == search_engine:
        for num in range(max_search_num): # 10 will be replaced with max search number
            try:
                def click_next():
                    time.sleep(2)
                    next_button = driver.find_element(next_selector[0], next_selector[1])
                    next_button.click()
                
                click_next()
            except selenium.common.exceptions.ElementClickInterceptedException:
                try:
                    click_next()
                except selenium.common.exceptions.NoSuchElementException:
                    break

        title_tags = driver.find_elements(By.CSS_SELECTOR, search_result_title)

        titles = [(title.text, title.get_attribute('href')) for title in title_tags]
    else:
        for num in range(max_search_num): # 10 will be replaced with max search number
            time.sleep(2)

            title_tags = driver.find_elements(By.CSS_SELECTOR, search_result_title)
            
            for title in title_tags:
                if search_engine == 'yahoo':
                    titles.append((title.text.splitlines()[1], title.get_attribute('href')))
                else:
                    titles.append((title.text, title.get_attribute('href')))

            try:
                def click_next():
                    time.sleep(5)
                    next_button = driver.find_element(next_selector[0], next_selector[1])
                    next_button.click()
                
                click_next()
            except selenium.common.exceptions.ElementClickInterceptedException:
                try:
                    click_next()
                except:
                    break

    required_list = []

    for tuple in titles:
        title = tuple[0]
        title_link = tuple[1]
        page_depth = 0
    
        for character in title_link:
            if character == '/':
                page_depth += 1 

        required_list.append((title, title_link, page_depth - 2))

    # now store data retrived in a file
    search_result_data = {
        'Search Engine': [search_engine for item in required_list],
        'Keyword Phrase': [keyword for item in required_list],
        'Site Title': [item[0] for item in required_list],
        'Site Url': [item[1] for item in required_list],
        'Page Depth Number': [item[2] for item in required_list],
    }
    
    # convert data to csv file
    search_engine_result = pd.DataFrame(data=search_result_data)
    path = search_engine_result.to_csv(f'search_engine_result.csv')
    return path

def run_crawler(search_engine_name, search_phrase, page_depth_num, max_search_num):
    # search engines dictionary for reference to be able get respective data
    search_engines = {
        'google': ('https://www.google.com/', [By.NAME, 'q'], '.yuRUbf a h3', [By.LINK_TEXT, 'Next']),
        'yahoo': ('https://search.yahoo.com/', [By.CSS_SELECTOR, '#yschsp'], '.relsrch .title a', [By.LINK_TEXT, 'Next']),
        'bing': ('https://www.bing.com/', [By.CSS_SELECTOR, '#sb_form_q'], 'h2 a', [By.CSS_SELECTOR, 'a.sb_pagN_bp.sb_bp']),
        'duckduckgo': ('https://duckduckgo.com/', [By.CSS_SELECTOR, '#search_form_input_homepage'], 'h2 a', [By.LINK_TEXT, 'More Results']),
        'yandex': ('https://yandex.com/', [By.CSS_SELECTOR, '.input__input'], '.organic__title-wrapper a', [By.LINK_TEXT, 'next']),
        'dogpile': ('https://www.dogpile.com/', [By.CSS_SELECTOR, '.search-form-home__q'], '.web-bing__title', [By.LINK_TEXT, 'Next']),
        'ask': ('https://www.ask.com/', [By.CSS_SELECTOR, '.search-box'], '.result-link', [By.LINK_TEXT, 'Next']),
    }

    search_engine = search_engine_name
    keyword = search_phrase
    page_depth_number = page_depth_num
    max_search_number = max_search_num

    requirements = search_engines[search_engine]
    scrape_web(search_engine=search_engine, URL=requirements[0], input_selector=requirements[1], keyword=keyword, search_result_title=requirements[2], next_selector=requirements[3], max_search_num=max_search_number)

# testing
# run_crawler(search_engine_name='yahoo', search_phrase='atlantic ocean', page_depth_num=3, max_search_num=10)


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


driver.quit()