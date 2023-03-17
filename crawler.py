import selenium, pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def scrape_web(search_engine, URL, input_selector, keyword, search_result_title, next_selector, page_depth_num, max_search_num):
    # set up headless driver
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # get the search engine website
    driver.get(url=URL)
    wait = WebDriverWait(driver=driver, timeout=60.0)

    search_bar = wait.until(EC.presence_of_element_located((input_selector[0], input_selector[1])))
    search_bar.send_keys(keyword, Keys.ENTER)

    titles = []

    # fetch 100+ results
    if 'duckduckgo' == search_engine:
        for num in range(max_search_num):
            try:
                def click_next():
                    next_button = wait.until(EC.presence_of_element_located((next_selector[0], next_selector[1])))
                    next_button.click()
                
                click_next()
            except selenium.common.exceptions.ElementClickInterceptedException or selenium.common.exceptions.TimeoutException:
                try:
                    click_next()
                except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.TimeoutException:
                    break

        title_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, search_result_title)))

        titles = [(title.text, title.get_attribute('href')) for title in title_tags]
    else:
        for num in range(max_search_num):
            try:
                title_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, search_result_title)))
            except selenium.common.exceptions.TimeoutException:
                break
            
            for title in title_tags:
                if search_engine == 'yahoo':
                    titles.append((title.text.splitlines()[1], title.get_attribute('href')))
                elif search_engine == 'brave':
                    titles.append((title.text.splitlines()[0], title.get_attribute('href')))
                else:
                    titles.append((title.text, title.get_attribute('href')))

            try:
                def click_next():
                    next_button = wait.until(EC.presence_of_element_located((next_selector[0], next_selector[1])))
                    next_button.click()
                
                click_next()
            except selenium.common.exceptions.ElementClickInterceptedException or selenium.common.exceptions.TimeoutException:
                try:
                    click_next()
                except:
                    break

    driver.quit()

    required_list = []

    for tuple in titles:
        title = tuple[0]
        title_link = tuple[1]
        page_depth = 0
    
        for character in title_link:
            if character == '/':
                page_depth += 1

        for num in range(1, page_depth_num + 1):
            if num + 2 == page_depth:
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
    search_engine_result.to_csv(f'search_engine_result.csv')

def run_crawler(search_engine_name, search_phrase, page_depth_num, max_search_num):
    # search engines dictionary for reference to be able get respective data
    search_engines = {
        'yahoo': ('https://search.yahoo.com/', [By.CSS_SELECTOR, '#yschsp'], '.relsrch .title a', [By.LINK_TEXT, 'Next']),
        'bing': ('https://www.bing.com/', [By.CSS_SELECTOR, '#sb_form_q'], 'h2 a', [By.CSS_SELECTOR, 'a.sb_pagN_bp.sb_bp']),
        'duckduckgo': ('https://duckduckgo.com/', [By.CSS_SELECTOR, '#search_form_input_homepage'], 'h2 a', [By.LINK_TEXT, 'More Results']),
        'brave': ('https://search.brave.com/', [By.CSS_SELECTOR, '#searchbox'], '.result-header', [By.LINK_TEXT, 'Next']),
        'gigablast': ('https://gigablast.com/', [By.CSS_SELECTOR, 'input#q'], '.result .title', [By.LINK_TEXT, 'Next 25 Results']),
        'lycos': ('https://www.lycos.com/', [By.CSS_SELECTOR, '.search-input'], '.result-title a', [By.LINK_TEXT, 'Next']),
        'aol': ('https://www.aol.com/', [By.CSS_SELECTOR, '#header-form-search-input'], '.searchCenterMiddle h3.title a', [By.LINK_TEXT, 'Next']),
        'neeva': ('https://neeva.com/', [By.CSS_SELECTOR, '.search-bar_searchInput__X3uLy'], '.lib-doc-title__link-1b9rC', [By.LINK_TEXT, 'Next']),
    }

    search_engine = search_engine_name
    keyword = search_phrase
    page_depth_number = int(page_depth_num)
    max_search_number = int(int(max_search_num)/10)

    requirements = search_engines[search_engine]
    scrape_web(search_engine=search_engine, URL=requirements[0], input_selector=requirements[1], keyword=keyword, search_result_title=requirements[2], next_selector=requirements[3], page_depth_num=page_depth_number, max_search_num=max_search_number)
