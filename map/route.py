from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema
import datetime

map = Blueprint('map', __name__, static_folder='static', template_folder='templates')

@map.route('/index')
@map.route('/')
def index():
	result = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(result)
	return render_template('save.html', transmitters=output)

@map.route('/query')
def query():
	days_ago = datetime.datetime.now() - datetime.timedelta(hours=12)
	# return str(days_ago)
	# return str(datetime.datetime.now() >= days_ago)
	messages = Sms.query.distinct(Sms.transmitter_id).filter(Sms.date_sent >= days_ago).order_by(Sms.id.desc()).first()
	output = SmsSchema(many=False).dump(messages)
	return jsonify(output)