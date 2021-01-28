from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify
from model.models import db, Sms, SmsSchema, Transmitter, TransmitterSchema
from datetime import datetime
from sqlalchemy import desc, asc
import random
from dateutil import parser

graph = Blueprint('graph', __name__, static_folder='static', template_folder='templates')

@graph.route('/index')
@graph.route('/')
def index():
	# t_name = request.form['transmitter_name']
	t_name = "Transmitter Jagna"
	sms = db.session.query(Sms).join(Transmitter).filter(Transmitter.name == t_name).order_by(desc(Sms.created_at)).all()
	output = SmsSchema(many=True).dump(sms)
	water_distance = []
	times = []
	for o in output:
		water_distance.append(o.get('water_distance'))
		times.append(parser.parse(o.get('created_at')).strftime("%b. %d, %Y %I:%M:%S %p"))
	# return jsonify(output)
	return render_template('graph_index.html', legend=t_name, water_distance=water_distance, times=times)