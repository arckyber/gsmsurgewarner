from flask import Blueprint, render_template, url_for, current_app, request, flash

realtime = Blueprint('realtime', __name__, static_folder='static', template_folder='templates')

@realtime.route('/index')
@realtime.route('/')
def index():
	legend = "Water Distance"
	water_distance = [
		3.3,
		1.2,
		4.4,
		2.2,
		4.5,
		2.3,
	]
	times = [
		'12:00pm',
		'1:00pm',
		'2:00pm',
		'2:30pm',
		'2:50pm',
		'3:30pm',
	]
	return render_template('realtime_index.html', legend=legend, water_distance=water_distance, times=times)