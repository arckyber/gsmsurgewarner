from flask import Blueprint, render_template, url_for, current_app, request, flash

realtime = Blueprint('realtime', __name__, static_folder='static', template_folder='templates')

@realtime.route('/index')
@realtime.route('/')
def index():
	return render_template('realtime_index.html')