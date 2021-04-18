from flask import Flask, render_template, url_for, Response, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from datetime import datetime, timedelta
import time, bisect
from model.models import db, Role

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'll340s0fj340'
# app.permanent_session_lifetime = timedelta(minutes=60)

# init celery
# flask_app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(flask_app)


from transmitter.transmitter import transmitter
app.register_blueprint(transmitter, url_prefix="/transmitter")

from arduino.route import arduino
app.register_blueprint(arduino, url_prefix="/arduino")

from sms.sms import sms
app.register_blueprint(sms, url_prefix="/sms")

from graph.graph import graph
app.register_blueprint(graph, url_prefix="/graph")

from map.route import map
app.register_blueprint(map, url_prefix='/map')

from users.route import users
app.register_blueprint(users, url_prefix="/users")

from configurations.route import configurations
app.register_blueprint(configurations, url_prefix="/configurations")

from extrasms.route import extrasms
app.register_blueprint(extrasms, url_prefix="/extrasms")

from test.route import test
app.register_blueprint(test, url_prefix="/test")

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


# Celery processes
# @celery.task()
# end celery processes

@app.route('/')
def index():
	return render_template('home/index.html')

# @app.route('/showtime')
# def showtime():
# 	def generate():
# 		yield datetime.now().strftime("%b. %d, %Y %I:%M:%S %p")
# 	return Response(generate(), mimetype='text')

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)