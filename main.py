import json
from flask import Flask, request, jsonify,render_template,send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

# set up headless driver
chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(chrome_options=chrome_options)



app = Flask('Search Engine Crawler')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)
db = SQLAlchemy(app)

@app.route('/scrape',methods=['POST'])
def scrape():
	if request.method == 'POST':
		info = request.get_json()
		search_engine_name=info['search_engine_name']
		search_phrase = info['search_phrase']
		page_depth_num = info['page_depth_num']
		max_search_num = info['max_search_num']
		print('Scrape in progress....')
		if info:
			return run_crawler(search_engine_name=search_engine_name,search_phrase=search_phrase,page_depth_num=page_depth_num,max_search_num=max_search_num)
	return jsonify({'message':'Post requests only'})

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	admin = db.Column(db.Boolean,default=False)

	def __repr__(self) -> str:
		return '<User %r>' % self.admin
with app.app_context():
	print(User.query.all(),'!')
	use=User.query.filter_by(id=2).first()
	use.admin=True
	db.session.commit()
	print(User.query.all(),'@')


@app.route('/signup', methods=['POST'])
def create_user():
	if not inspect(db.engine).has_table('user'):
		db.create_all()
	auth_info = request.get_json()
	email = auth_info['email']
	password = auth_info['password']
	username = auth_info['username']

	is_user = User.query.filter_by(username=username, email=email).first()
	if is_user is not None:
		info = {'message': 'User already exists'}
		return jsonify(info)
	if len(User.query.all()) == 5:
		return jsonify({'message':'Max User limit'})
	user = User(
		username=username,
		email=email,
		password=password
	)
	db.session.add(user)
	db.session.commit()

	if user.id == 1:
		user.admin = True
		db.session.commit()

	info = {'message': 'User created', 'admin': user.admin}
	return jsonify(info), 200

@app.route('/delete',methods=['POST'])
def delete_user():
	email=request.get_json()['email']
	exists = User.query.filter_by(email=email).first()
	if is_admin(email):
		new=User.query.filter_by(id=int(exists.id)+1)
		db.session.delete(exists)
		db.session.commit()
		if new:
			exists.admin=False
			new.admin=True
			db.session.commit()
		return jsonify({'message':f'Admin {exists} Deleted\nNew admin is {new}'})
	if exists:
		user=exists.username
		db.session.delete(exists)
		db.session.commit()
		return jsonify({'message':f'User {user} Deleted'})

@app.route('/login', methods=['OPTIONS'])
def handle_options():
	response = app.make_default_options_response()
	response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
	return response


@app.route('/login', methods=['GET', 'POST'])
def login():
	if not inspect(db.engine).has_table('user'):
		db.create_all()
	if request.method == 'POST':
		auth_info = request.get_json()
		email = auth_info['email']
		password = auth_info['password']
		user = User.query.filter_by(email=email,password=password).first()
		if user and authenticate(email,password):
			user_dict= {'username':user.username,'email':user.email,'admin':user.admin}
			return jsonify(user_dict)
		else:
			return jsonify({'message':'Invalid email or password.'})

	return jsonify({'message':'Create User account first'})


#Password auth
def authenticate(email,password):
	user = User.query.filter_by(email=email,password=password).first()
	if user:
		return bool(user.email==email and user.password==password)
	print(user)
	return False

def is_admin(email):
	user=User.query.filter_by(email=email).first()
	return user.admin

#Home ROute
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')


@app.route('/users',methods=['GET'])
def get_all():
	users = User.query.all()
	json_arr  = []
	for user in users:
		json_arr.append(
			{
			'username':user.username,
			'email':user.email,
			'admin':user.admin,
			'password': user.password
			}
		)

	with open('users.json','w') as file:
		json.dump(json_arr,file)
	with open('users.json','r') as json_out_file:
		out=json.load(json_out_file)
	return jsonify(out)



def scrape_web(search_engine, URL, input_selector, keyword, search_result_title, next_selector, page_depth_num, max_search_num):
	# get the search engine website
	driver.get(url=URL)
	wait = WebDriverWait(driver=driver, timeout=10.0)

	search_bar = wait.until(EC.presence_of_element_located((input_selector[0], input_selector[1])))
	search_bar.send_keys(keyword, Keys.ENTER)

	titles = []

	# fetch 100+ results
	if 'duckduckgo' == search_engine:
		for num in range(max_search_num): # 10 will be replaced with max search number
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
		for num in range(max_search_num): # 10 will be replaced with max search number
			try:
				title_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, search_result_title)))
			except selenium.common.exceptions.TimeoutException:
				break
			
			for title in title_tags:
				if search_engine == 'yahoo':
					titles.append((title.text.splitlines()[1], title.get_attribute('href')))
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

	required_list = []

	for tuple in titles:
		title = tuple[0]
		title_link = tuple[1]
		page_depth = 0
	
		for character in title_link:
			if character == '/':
				page_depth += 1 

		if page_depth_num + 2 == page_depth:
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
	scrape_web(search_engine=search_engine, URL=requirements[0], input_selector=requirements[1], keyword=keyword, search_result_title=requirements[2], next_selector=requirements[3], page_depth_num=page_depth_number, max_search_num=max_search_number)
	driver.quit()





if __name__ == '__main__':
	app.run(debug=True)