from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, redirect, session
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema
import datetime
from sqlalchemy import desc, asc

map = Blueprint('map', __name__, static_folder='static', template_folder='templates')

@map.route('/index')
@map.route('/')
def index():
	if 'map' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	result = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(result)
	return render_template('index.html', transmitters=output)

@map.route('/query')
def query():
	days_ago = datetime.datetime.now() - datetime.timedelta(hours=12)
	# return str(days_ago)
	# return str(datetime.datetime.now() >= days_ago)
	query = Sms.query.filter(Sms.created_at >= days_ago).order_by(Sms.id.desc())
	messages = query.distinct().order_by(desc(Sms.created_at)).all()
	output = SmsSchema(many=True).dump(messages)
	return jsonify(output)

@map.route('/test')
def test():
	result = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(result)
	return jsonify(output)