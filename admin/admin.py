from flask import Blueprint, render_template, url_for, current_app, request, flash
from model.models import Admin, db

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/', methods=['POST', 'GET'])
@admin.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
	return render_template('admin_dashboard.html')

@admin.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':

		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		password2 = request.form['password2']

		if username and email and password and password2:
			if password == password2:
				pass
			else:
				flash("Password not matched!", "error")
	return render_template('admin_register.html')

@admin.route('/login')
def login():
	return render_template('admin_login.html');

@admin.route('/test')
def test():
	# from admin.model.admin import Admin, db
	a=Admin('Carlo')
	db.session.add(a)
	db.session.commit()

	q=Admin.query.all()

	for qq in q:
		print(qq.name)

	return f"<h1>This is test</h1>"
