from flask import Flask, request, jsonify,render_template,send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


app = Flask('Search Engine Crawler')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	admin = db.Column(db.Boolean,default=False)
	

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
		return jsonify(info), 409

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


@app.route('/login', methods=['OPTIONS'])
def handle_options():
	response = app.make_default_options_response()
	response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
	return response


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		auth_info = request.get_json()
		email = auth_info['email']
		password = auth_info['password']
		user = User.query.filter_by(email=email,password=password).first()
		user_dict= {'username':user.username,'email':user.email,'admin':user.admin}
		if user and authenticate(email,password):
			return jsonify(user_dict)
		else:
			return jsonify({'message':'Invalid email or password.'})

	return jsonify({'message':'Create User account first'})


#Password auth
def authenticate(email,password):
	user = User.query.filter_by(email=email,password=password).first()
	if user:
		return bool(user.email==email and user.password==password)
	return False


#Home ROute
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')




if __name__ == '__main__':
	app.run(debug=True)