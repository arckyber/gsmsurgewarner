from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, session, redirect
from model.models import db, Sms, SmsSchema, Transmitter
import datetime
from sqlalchemy import desc, asc, func
import random
from config.const import SUCCESS, FAILED, ERROR, ALERT_3_MESSAGE, ALERT_4_MESSAGE, DISTANCE_DEFAULT_UNIT

sms = Blueprint('sms', __name__, static_folder='static', template_folder='templates')

def authenticateUser():
	print("Authenticate.......................")
	if 'user' not in session:
		redirect(url_for('users.login'))

@sms.route('/index')
@sms.route('/')
def index():
	authenticateUser()
	if 'sms' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	return render_template('sms_index.html')

@sms.route('/add', methods=['POST'])
def add():
	transmitter_id = Transmitter.query.first().id
	sms = Sms(
		alert_type = int(4),
		water_distance = float(1.4),
		transmitter_id = 2,
		created_at = datetime.datetime.now(),
		date_sent = datetime.datetime.now(),
		status = True,
		is_opened = False,
	)
	try:
		db.session.add(sms)
		db.session.commit()
		return SUCCESS
	except:
		return ERROR
	return FAILED

@sms.route('/dummy')
def dummy():
	return jsonify([
		{'id': '12', 'name': 'Transmitter 1', 'alert_type': 'orange', 'post_number': 12, 'location': 'Zamora, Talibon, Bohol', 'post_description': 'Under the tulay', 'water_distance': '2m from sensor', 'date_created': 'Jan. 20, 2021'},
		{'id': '12', 'name': 'Transmitter 21', 'alert_type': 'yellow', 'post_number': 2, 'location': 'San Miguel, Bohol', 'post_description': 'Under the hagdan', 'water_distance': '3m from sensor', 'date_created': 'Jan. 19, 2021'},
		{'id': '12', 'name': 'Transmitter 34', 'alert_type': 'normal', 'post_number': 4, 'location': 'Trinidad, Bohol', 'post_description': 'Under the Dahon', 'water_distance': '6m from sensor', 'date_created': 'Jan. 12, 2021'},
		{'id': '12', 'name': 'Transmitter 3', 'alert_type': 'red', 'post_number': 1, 'location': 'Ubay, Bohol', 'post_description': 'Under the tree', 'water_distance': '0.6m from sensor', 'date_created': 'Jan. 9, 2021'},
		{'id': '12', 'name': 'Transmitter 1', 'alert_type': 'yellow', 'post_number': 12, 'location': 'Talibon, Bohol', 'post_description': 'Under the hagdan', 'water_distance': '3.4m from sensor', 'date_created': 'Jan. 2, 2021'},
	])

@sms.route('/show')
def show():
	# query = Sms.query.order_by(desc(Sms.created_at)).all()
	query =  Sms.query.order_by(desc(Sms.date_sent)).all()
	output = SmsSchema(many=True).dump(query)
	return jsonify(output)

@sms.route('/get', methods=['POST'])
def get():
	sms_id = request.form['id']
	sms = Sms.query.filter(Sms.id == sms_id).first()
	output = SmsSchema(many=False).dump(sms)
	return jsonify(output)

@sms.route('/mark_read', methods=['POST'])
def mark_read():
	sms = Sms.query.filter(Sms.id == request.form['id']).first()
	sms.is_opened = True
	db.session.commit()
	return ""

@sms.route('/unread_count', methods=['POST'])
def unread_count():
	count = db.session.query(func.count(Sms.id)).filter(Sms.is_opened == False).scalar()
	return str(count)

@sms.route('/unread', methods=['POST'])
def unread():
	sms = Sms.query.filter(Sms.is_opened == False).order_by(desc(Sms.created_at)).limit(3)
	output = SmsSchema(many=True).dump(sms)
	return jsonify(output)

@sms.route('/clear')
def clear():
	db.session.query(Sms).delete()
	db.session.commit()
	return "Deleted"

@sms.route('/delete/<id>')
def delete(id):
	Sms.query.filter(Sms.id == id).delete()
	db.session.commit()
	return "Deleted"