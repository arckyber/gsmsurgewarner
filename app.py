from flask import Flask, render_template, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from datetime import datetime
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'll340s0fj340'


from admin.admin import admin	
app.register_blueprint(admin, url_prefix="/admin")

from transmitter.transmitter import transmitter
app.register_blueprint(transmitter, url_prefix="/transmitter")

from arduino.arduino import arduino
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
@app.route('/login')
def index():
	return render_template("login.html")

@app.route('/showtime')
def showtime():
	def generate():
		yield datetime.now().strftime("%b. %d, %Y %I:%M:%S %p")
	return Response(generate(), mimetype='text')
	# return generate()

if __name__ == '__main__':
	# with app.app_context():
	# 	db.create_all()
	db.create_all()
	app.run(debug=True)