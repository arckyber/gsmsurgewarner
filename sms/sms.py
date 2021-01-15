from flask import Blueprint, render_template, url_for, current_app, request, flash

sms = Blueprint('sms', __name__, static_folder='static', template_folder='templates')

@sms.route('/index')
@sms.route('/')
def index():
	return render_template('sms_index.html')