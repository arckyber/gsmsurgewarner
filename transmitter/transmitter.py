import json, traceback
from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, Response
from model.models import db, TransmitterSchema, Transmitter
from util.query_serializer import serialize

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
def test():
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
			return "Add successful!"
		except:
			return "Add failure!"
	else:
		return "All fields are required"
	# t1 = Transmitter('Transmitter 1', '09097454445', 2, 'Near the gate', 'Tagum Sur, Trinidad, Bohol')
	# t2 = Transmitter('Transmitter 2', '09097454465', 2, 'Below Bridge', 'San Jose, Talibon, Bohol')
	# t3 = Transmitter('Transmitter 2', '09097454465', 2, 'Near the Nara tree', 'Ubay, Bohol')