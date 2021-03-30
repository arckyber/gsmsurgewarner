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

@transmitter.route('/store', methods=['POST'])
def add():
	# return request.form['name']	
	transmitter = Transmitter(
		name = request.form['name'],
		sim_number = request.form['sim_number'],
		post_number = request.form['post_number'],
		post_description = request.form['post_description'],
		location = request.form['location'],
		longitude = request.form['longitude'],
		latitude = request.form['latitude'],
	)
	if transmitter.longitude and transmitter.latitude and transmitter.name and transmitter.sim_number and transmitter.post_number and transmitter.post_description and transmitter.location:
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

@transmitter.route('/add')
def addtest():
	return render_template('add.html')

@transmitter.route('/edit/<id>')
def edit(id):
	transmitter = Transmitter.query.filter(Transmitter.id==id).first()
	res = Transmitter.query.filter(Transmitter.id==id).first()
	output = TransmitterSchema(many=False).dump(res)
	# return jsonify(output)
	return render_template('edit.html', transmitter=output)

@transmitter.route('/update', methods=['POST'])
def update():
		# return request.form['name']	
	transmitter = Transmitter(
		name = request.form['name'],
		sim_number = request.form['sim_number'],
		post_number = request.form['post_number'],
		post_description = request.form['post_description'],
		location = request.form['location'],
		longitude = request.form['longitude'],
		latitude = request.form['latitude'],
	)
			
	desequivalert = Desequivalert(
		_normal = request.form['_normal'],
		_yellow = request.form['_yellow'],
		_orange = request.form['_orange'],
		_red = request.form['_red'],
		transmitter_id = request.form['id']
	)
	if transmitter.longitude and transmitter.latitude and  transmitter.name and transmitter.sim_number and transmitter.post_number and transmitter.post_description and transmitter.location and desequivalert._normal and desequivalert._yellow and desequivalert._orange and desequivalert._red:
		try:
			trans = Transmitter.query.filter(Transmitter.id == request.form['id']).first()

			trans.name = transmitter.name
			trans.sim_number = transmitter.sim_number
			trans.post_number = transmitter.post_number
			trans.post_description = transmitter.post_description
			trans.location = transmitter.location

			time.sleep(.5)			
			db.session.commit()

			desequiv = Desequivalert.query.filter(Desequivalert.transmitter_id==request.form['id']).first()
			
			desequiv._normal = desequivalert._normal
			desequiv._yellow = desequivalert._yellow
			desequiv._orange = desequivalert._orange
			desequiv._red = desequivalert._red

			db.session.commit()

			return SUCCESS
		except Exception as e:
			print(str(e))
			return ERROR
	else:
		return MISSING_DATA

@transmitter.route('/delete', methods=['POST'])
def delete():
	id = request.form['id']
	try:
		Transmitter.query.filter(Transmitter.id==id).delete()
		db.session.commit()
	except Exception as e:
		print(str(e))
		return ERROR
	return SUCCESS

@transmitter.route('/map')
def map():
	result = Transmitter.query.all()
	output = TransmitterSchema(many=True).dump(result)
	return render_template('map.html', transmitters=output)


@transmitter.route('/hoy')
def hoy():
	res = Transmitter.query.first()
	out = TransmitterSchema(many=False).dump(res)
	return str(out['desequivealert'][0]['_red'])