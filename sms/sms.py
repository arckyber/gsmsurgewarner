from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify
from model.models import db, Sms, SmsSchema, Transmitter
import datetime
from sqlalchemy import desc, asc
import random
from config.const import SUCCESS, FAILED, ERROR
from model.alert import get_alert_level

sms = Blueprint('sms', __name__, static_folder='static', template_folder='templates')

@sms.route('/index')
@sms.route('/')
def index():
	return render_template('sms_index.html')

@sms.route('/add', methods=['POST'])
def add():
	transmitter_id = Transmitter.query.first().id
	sms = Sms(
		alert_level = int(3),
		water_distance = float(2),
		transmitter_id = 1,
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
		{'id': '12', 'name': 'Transmitter 1', 'alert_level': 'orange', 'post_number': 12, 'location': 'Zamora, Talibon, Bohol', 'post_description': 'Under the tulay', 'water_distance': '2m from sensor', 'date_created': 'Jan. 20, 2021'},
		{'id': '12', 'name': 'Transmitter 21', 'alert_level': 'yellow', 'post_number': 2, 'location': 'San Miguel, Bohol', 'post_description': 'Under the hagdan', 'water_distance': '3m from sensor', 'date_created': 'Jan. 19, 2021'},
		{'id': '12', 'name': 'Transmitter 34', 'alert_level': 'normal', 'post_number': 4, 'location': 'Trinidad, Bohol', 'post_description': 'Under the Dahon', 'water_distance': '6m from sensor', 'date_created': 'Jan. 12, 2021'},
		{'id': '12', 'name': 'Transmitter 3', 'alert_level': 'red', 'post_number': 1, 'location': 'Ubay, Bohol', 'post_description': 'Under the tree', 'water_distance': '0.6m from sensor', 'date_created': 'Jan. 9, 2021'},
		{'id': '12', 'name': 'Transmitter 1', 'alert_level': 'yellow', 'post_number': 12, 'location': 'Talibon, Bohol', 'post_description': 'Under the hagdan', 'water_distance': '3.4m from sensor', 'date_created': 'Jan. 2, 2021'},
	])

@sms.route('/show')
def show():
	# query = Sms.query.order_by(desc(Sms.created_at)).all()
	query =  Sms.query.all()
	output = SmsSchema(many=True).dump(query)
	return jsonify(output)