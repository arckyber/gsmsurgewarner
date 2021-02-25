from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, redirect
from model.models import db, Sms, SmsSchema, Transmitter, TransmitterSchema
from datetime import datetime
from sqlalchemy import desc, asc, and_, func
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
	transmitters = Transmitter.query.all()
	return render_template('graph.html', legend=t_name, water_distance=water_distance, times=times, transmitters=transmitters)

@graph.route('/process', methods=['POST'])
def process():
	transmitter = request.form['transmitter']
	if (transmitter == 'All'):
		return redirect('/graph')
	date_begin = request.form['date_begin']
	date_end = request.form['date_end']
	sms = db.session.query(Sms).join(Transmitter).filter(Sms.created_at.between(date_begin, date_end)).filter(Transmitter.name == transmitter).order_by(desc(Sms.created_at)).all()
	# sms = db.session.query(Sms).join(Transmitter).filter(and_(func.date(Sms.created_at >= date_begin), func.date(Sms.created_at <= date_end))).filter(Transmitter.name == transmitter).order_by(desc(Sms.created_at)).all()
	output = SmsSchema(many=True).dump(sms)
	water_distance = []
	times = []
	for o in output:
		water_distance.append(o.get('water_distance'))
		times.append(parser.parse(o.get('created_at')).strftime("%b. %d, %Y %I:%M:%S %p"))
	transmitters = Transmitter.query.all()
	return render_template('graph.html', legend=transmitter, water_distance=water_distance, times=times, transmitters=transmitters)
