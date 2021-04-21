from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, session, redirect
from model.models import User, db, Role, RoleSchema, UserSchema, UserInfo, UserInfoSchema, RoleAccess, RoleAccessShema
from users import dashboard_data as dd
import os, time, json
from config.const import MODULES

users = Blueprint("users", __name__, static_folder="static", template_folder="templates")

@users.route('/dashboard')
def dashboard():
	if 'dashboard' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	if 'user' not in session:
		return redirect(url_for('users.login'))
	data = {
		"transmitter_count": dd.transmitters_count(),
		"message_count": dd.sms_count(),
		"users_count": dd.users_count(),
		"alerts_count": dd.alert_count(),
		"detection_history": dd.detection_history(),
		"users": dd.users(),
		"roles": dd.roles_(),
	}
	if 'email' not in session:
		return redirect(url_for('users.login'))
	return render_template('dashboard.html', data=data)

@users.route('/register')
def register():
	if 'users' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	role = Role.query.all()
	output = RoleSchema(many=True).dump(role)
	if not role:
		flash("You need to add roles before you can add user.")
	return render_template('register.html', roles=output)

@users.route('/store', methods=['POST'])
def store():	

	# account information
	username = request.form['username']
	email = request.form['email']
	password1 = request.form['password1']
	password2 = request.form['password2']
	role = request.form['role']

	if username and email and password1 and password2 and role:
		if password2 == password1:
			role_id = Role.query.filter(Role.role == role).first().id
			if role_id:
				user = User(
					username = username,
					email = email,
					password = password1,
					role_id = role_id, 
					status = True,
				)
				db.session.add(user)
				db.session.commit()
			else:
				return "role not found"
		else:
			return "password not matched"
	else:
		return "fields not complete"

	quser = User.query.filter(User.username == username, User.email == email).first()

	if quser:
		# user information
		image = request.files['image']
		path = os.path.join('./upload', image.filename)
		firstname = request.form['firstname']
		middlename = request.form['middlename']
		lastname = request.form['lastname']
		gender = request.form['gender']

		if image and path and firstname and middlename and lastname and gender:
			userInfo = UserInfo(
				firstname = firstname,
				middlename = middlename,
				lastname = lastname,
				gender = gender,
				user_id = quser.id,
				image = path
			)
			image.save(path)

			db.session.add(userInfo)
			db.session.commit()
		else:
			return "User information fields not complete"

	return redirect(url_for('users.login'))

@users.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email and password:
			user = User.query.filter(User.email == email, User.password == password).first()
			userS = UserSchema(many=False).dump(user)
			role_access = []
			if user:
				session['email'] = user.email
				session['user'] = {'user':userS}
				session['username'] = user.username
				for access in user.role.role_access:
					role_access.append(access.access)
				session['role_access'] = role_access
				return redirect(url_for('users.dashboard'))
			else:
				return "user not found"
		else:
			return "all fields are required"
	elif request.method == 'GET':
		if 'email' in session:
			return redirect(url_for('users.dashboard'))
		return render_template('login.html')
	else:
		return redirect(url_for('/'))

@users.route('/logout')
def logout():
	session.pop('email', None)
	session.pop('user', None)
	session.pop('role_access', None)
	session.pop('username', None)
	return render_template('/login.html')

@users.route('/roles')
def roles():
	return render_template('/roles.html', modules=MODULES)

@users.route('/roles-list') 
def rolesList():
	roles = Role.query.all()
	output = RoleSchema(many=True).dump(roles)
	return jsonify(output)

@users.route('/getroles')
def getroles():
	results = Role.query.all()
	output = RoleSchema(many=True).dump(results)
	return jsonify(output)

@users.route('/add-role', methods=['POST'])
def addRole():
	if request.method == 'POST':
		r = request.form['role']
		access = json.loads(request.form['checkedAccess'])

		print(access)
		
		role = Role(
			role = r
		)

		try:
			db.session.add(role)
			db.session.commit()

			role_id = Role.query.filter(Role.role == r).first().id

			for a in access:
				ra = RoleAccess(
					access = a,
					role_id = role_id
				)
				db.session.add(ra)
			db.session.commit()
		except Exception as e:
			return str(e)
		
		return "success"

	else:
		return "Invalid method"

@users.route('/list')
def users_list():
	if 'users' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	return render_template('/list.html')

@users.route('/adduserinfo')
def addUserInfo():
	if 'users' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	role = Role.query.all()
	output = RoleSchema(many=True).dump(role)
	return render_template('/adduserinfo.html', roles=output)

@users.route('/user-info/<id>')
def userInfo(id):
	if 'users' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	user = User.query.filter(User.id == id).first()
	output = UserSchema(many=False).dump(user)
	return render_template('/comp/user-info.html', user=user)

@users.route('/edit-info/<id>')
def editInfo(id):
	if 'users' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	user = User.query.filter(User.id == id).first()
	output = UserSchema(many=False).dump(user)
	roles = Role.query.all()
	return render_template('/comp/edit-info.html', user=user, roles=roles)

@users.route('/profile')
def profile():
	if 'users' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	return render_template("/profile.html")

@users.route('/show')
def show():
	users = User.query.filter(User.status == True).all()
	output = UserSchema(many=True).dump(users)
	return jsonify(output)

@users.route('/delete', methods=['POST'])
def delete():
	id = request.form['id']
	if id:
		user = User.query.filter(User.id == id).first()
		user.status = False
		db.session.commit()
		return "Delelte successful!"
	else:
		return "Identification needed!"

@users.route('/delete-role', methods=['POST'])
def deleteRole():
	if request.method == 'POST':
		id = request.form['id']
		db.session.query(Role).filter(Role.id == id).delete()
		db.session.query(RoleAccess).filter(RoleAccess.role_id == id).delete()
		db.session.commit()
		return "success"
	else:
		return "failed"

@users.route('/clear-role')
def clearRole():
	db.session.query(Role).delete()
	db.session.query(RoleAccess).delete()
	db.session.commit()
	return "Done"

@users.route('/right-access-control')
def rightAccessControl():
	return render_template('/right-access-control.html')