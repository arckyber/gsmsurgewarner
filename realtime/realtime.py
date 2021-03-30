from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema
import datetime

realtime = Blueprint('realtime', __name__, static_folder='static', template_folder='templates')

@realtime.route('/index')
@realtime.route('/')
def index():
	result = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(result)
	return render_template('realtime_index.html', transmitters=output)

@realtime.route('/query')
def query():
	days_ago = datetime.datetime.now() - datetime.timedelta(days=3)
	# return str(days_ago)
	# return str(datetime.datetime.now() >= days_ago)
	messages = Sms.query.distinct(Sms.transmitter_id).filter(Sms.date_sent >= days_ago).order_by(Sms.id.desc()).first()
	output = SmsSchema(many=False).dump(messages)
	return jsonify(output)