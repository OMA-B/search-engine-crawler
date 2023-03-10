import random
from flask import Flask, request, jsonify,render_template,send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
# from werkzeug.serving import run_with_reloader

from crawler import run_crawler


app = Flask('Search Engine Crawler')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)
db = SQLAlchemy(app)

@app.route('/scrape',methods=['POST'])
def scrape():
	if request.method == 'POST':
		info = request.get_json()
		search_engine_name=info['search_option']
		search_phrase = info['keyword']
		page_depth_num = info['page_depth']
		max_search_num = info['max_search_number']
		print('Scrape in progress....')
		if info:
			run_crawler(search_engine_name=search_engine_name,search_phrase=search_phrase,page_depth_num=page_depth_num,max_search_num=max_search_num)			
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
	# use.admin=True
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

	is_user = User.query.filter_by(email=email).first()
	if is_user is not None:
		info = {'message': 'This email already exists.'}
		return jsonify(info)
	else:
		if len(User.query.all()) == 5:
			return jsonify({'message':'Max Users limit reached.'})
		else:
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
		if exists.id < 5 and exists.id != 1:
			new_id = random.randint(exists.id+1, 5)
		elif exists.id > 1:
			new_id = random.randint(1, 4)
		else:
			new_id = random.randint(2, 5)
		new=User.query.filter_by(id=new_id)
		
		# db.session.commit()
		# if new:
		exists.admin=False
		new.admin=True
		db.session.delete(exists)
		db.session.commit()
		new_admin_email = new['email']
		return jsonify({'message':f'Admin {email} Deleted. New admin is {new_admin_email}.'})
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

	return jsonify(json_arr)


if __name__ == '__main__':
	app.run(debug=True)