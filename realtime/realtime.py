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
	messages = Sms.query.filter(Sms.date_sent == datetime.datetime.now(), Sms.date_sent >= days_ago).all()
	return jsonify(messages)