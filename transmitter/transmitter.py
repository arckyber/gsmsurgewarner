import json, traceback
from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, Response
from model.models import db, TransmitterSchema, Transmitter, Desequivalert, DesequivalertSchema
from util.query_serializer import serialize
from config.const import SUCCESS, FAILED, ERROR, MISSING_DATA
import datetime, time

transmitter = Blueprint('transmitter', __name__, static_folder='static', template_folder='templates')

@transmitter.route('/index')
@transmitter.route('/')
def index():
	return render_template('transmitter_index.html')

@transmitter.route('/show')
def show():
	results = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(results)
	return jsonify(output)

@transmitter.route('/add', methods=['POST'])
def add():
	# return request.form['name']	
	transmitter = Transmitter(
		name = request.form['name'],
		sim_number = request.form['sim_number'],
		post_number = request.form['post_number'],
		post_description = request.form['post_description'],
		location = request.form['location']
	)
	if transmitter.name and transmitter.sim_number and transmitter.post_number and transmitter.post_description and transmitter.location:
		try:
			db.session.add(transmitter)
			db.session.commit()

			time.sleep(1)

			trans_id = Transmitter.query.filter(Transmitter.sim_number == request.form['sim_number']).first().id

			# trans_id = db.session.query(Transmitter).filter(Transmitter.sim_number == request.form['sim_number'])

			print("printing trans id_____________________________________________")
			print(trans_id)
			
			desequivalert = Desequivalert(
				_normal = request.form['_normal'],
				_yellow = request.form['_yellow'],
				_orange = request.form['_orange'],
				_red = request.form['_red'],
				transmitter_id = trans_id
			)

			if desequivalert._normal and desequivalert._yellow and desequivalert._orange and desequivalert._red:
				db.session.add(desequivalert)
				db.session.commit()

				return SUCCESS
			else:
				return ERROR
		except Exception as e:
			print(str(e))
			return ERROR
	else:
		return MISSING_DATA

@transmitter.route('/des')
def des():
	results = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(results)
	# return jsonify(output)
	for o in output:
		print(o['desequivealert'][0]['_red'])
	return jsonify(output)

	# t1 = Transmitter('Transmitter 1', '09097454445', 2, 'Near the gate', 'Tagum Sur, Trinidad, Bohol')
	# t2 = Transmitter('Transmitter 2', '09097454465', 2, 'Below Bridge', 'San Jose, Talibon, Bohol')
	# t3 = Transmitter('Transmitter 2', '09097454465', 2, 'Near the Nara tree', 'Ubay, Bohol')