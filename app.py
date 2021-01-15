from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome

# from admin.model.admin import Admin

db = None
fa = None

def init_app():
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.secret_key = 'll340s0fj340'

	from admin.admin import admin	
	app.register_blueprint(admin, url_prefix="/admin")

	from arduino.arduino import arduino
	app.register_blueprint(arduino, url_prefix="/arduino")

	from sms.sms import sms
	app.register_blueprint(sms, url_prefix="/sms")

	from graph.graph import graph
	app.register_blueprint(graph, url_prefix="/graph")

	from realtime.realtime import realtime
	app.register_blueprint(realtime, url_prefix='/realtime')

	global db
	db = SQLAlchemy(app)

	global fa
	fa = FontAwesome(app)
	
	return app

app = init_app()

@app.route('/')
@app.route('/login')
def index():
	return render_template("login.html")

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)