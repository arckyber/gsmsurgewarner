from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, session, redirect
from model.models import User, db, Role, RoleSchema

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/', methods=['POST', 'GET'])
@admin.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
	return render_template('admin_dashboard.html')

@admin.route('/register', methods=['POST'])
def register():
	name = request.form['name']
	email = request.form['email']
	password1 = request.form['password1']
	password2 = request.form['password2']
	role = request.form['role']

	if name and email and password1 and password2 and role:
		if password2 == password1:
			role_id = Role.query.filter(Role.role == role).first().id
			if role_id:
				user = User(
					name = name,
					email = email,
					password = password1,
					role_id = role_id
				)
				db.session.add(user)
				db.session.commit()
			else:
				return "role not found"
		else:
			return "password not matched"
	else:
		return "fields not complete"

	return render_template('admin_register.html')

@admin.route('/login', methods=['POST'])
def login():
	if 'email' in session:
		return redirect(url_for('transmitter.index'))
	email = request.form['email']
	password = request.form['password']
	if email and password:
		user = User.query.filter(User.email == email, User.password == password).first()
		if user:
			session['email'] = user.email
			return redirect(url_for('dashboard'))
		else:
			return "user not found"
	else:
		return "all fields are required"
	return render_template('admin_login.html')

@admin.route('/test')
def test():
	# from admin.model.admin import Admin, db
	a=User('Carlo')
	db.session.add(a)
	db.session.commit()

	q=User.query.all()

	for qq in q:
		print(qq.name)

	return f"<h1>This is test</h1>"

@admin.route('/roles')
def roles():
	results = Role.query.all()
	output = RoleSchema(many=True).dump(results)
	return jsonify(output)
