from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, session, redirect
from model.models import User, db, Role, RoleSchema
from users import dashboard_data as dd

users = Blueprint("users", __name__, static_folder="static", template_folder="templates")

@users.route('/dashboard')
def dashboard():
	data = {
		"transmitter_count": dd.transmitters_count(),
		"message_count": dd.sms_count(),
		"users_count": dd.users_count(),
		"alerts_count": dd.alert_count(),
		"detection_history": dd.detection_history(),
		"users": dd.users(),
	}
	if 'email' not in session:
		return redirect(url_for('users.login'))
	return render_template('dashboard.html', data=data)

@users.route('/register')
def register():
	return render_template('register.html')

@users.route('/store', methods=['POST'])
def store():
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

	return redirect(url_for('users.login'))

@users.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            user = User.query.filter(User.email == email, User.password == password).first()
            if user:
                session['email'] = user.email
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
	return render_template('/login.html')

@users.route('/roles')
def roles():
	return render_template('/roles.html')

@users.route('/getroles')
def getroles():
	results = Role.query.all()
	output = RoleSchema(many=True).dump(results)
	return jsonify(output)

@users.route('/addrole', methods=['POST'])
def addrole():
	role = request.form['role']
	try:
		role = Role(role=role)
		db.session.add(role)
		db.session.commit()
	except Exception as e:
		return str(e)
	return "Done"

@users.route('/test')
def test():
	return dd.detection_history()
 