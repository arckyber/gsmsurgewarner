from flask import Flask, render_template, url_for, Response, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from datetime import datetime, timedelta
import time
from model.models import db, Role

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'll340s0fj340'
app.permanent_session_lifetime = timedelta(minutes=60)


from admin.admin import admin	
app.register_blueprint(admin, url_prefix="/admin")

from transmitter.transmitter import transmitter
app.register_blueprint(transmitter, url_prefix="/transmitter")

from arduino.route import arduino
app.register_blueprint(arduino, url_prefix="/arduino")

from sms.sms import sms
app.register_blueprint(sms, url_prefix="/sms")

from graph.graph import graph
app.register_blueprint(graph, url_prefix="/graph")

from realtime.realtime import realtime
app.register_blueprint(realtime, url_prefix='/realtime')

from users.route import users
app.register_blueprint(users, url_prefix="/users")

from configurations.route import configurations
app.register_blueprint(configurations, url_prefix="/configurations")

from extrasms.route import extrasms
app.register_blueprint(extrasms, url_prefix="/extrasms")

# from admin.model.admin import db as admin_db
# from transmitter.model.transmitter import db as transmitter_db
# from sms.model.sms import db as sms_db
# from users.models.user import db as user_db

# sms_db.init_app(app)
# transmitter_db.init_app(app)
# admin_db.init_app(app)
# user_db.init_app(app)
# with app.app_context():
# 	admin_db.create_all()
# 	transmitter_db.create_all()
# 	sms_db.create_all()
# 	user_db.create_all()

from model.models import db as ModelDb

ModelDb.init_app(app)
with app.app_context():
	ModelDb.create_all()

db = SQLAlchemy(app)

fa = FontAwesome(app)

@app.route('/')
def index():
	return render_template('home/index.html')

@app.route('/dashboard')
def dashboard():
	if 'email' not in session:
		return redirect(url_for('login'))
	return render_template('auth/dashboard.html')

@app.route('/login')
def login():
	if 'email' in session:
		return redirect(url_for('dashboard'))
	return render_template("auth/login.html")

@app.route('/register')
def register():
	return render_template('auth/register.html')

@app.route('/showtime')
def showtime():
	def generate():
		yield datetime.now().strftime("%b. %d, %Y %I:%M:%S %p")
	return Response(generate(), mimetype='text')
	# return generate()

@app.route('/logout')
def logout():
	session.pop('email', None)
	return render_template('auth/login.html')

@app.route('/test')
def test():
	return render_template('home/test.html')

if __name__ == '__main__':
	# with app.app_context():
	# 	db.create_all()
	db.create_all()
	# role = Role(role="Operator")
	# db.session.add(role)
	# db.session.commit()
	app.run(debug=True)