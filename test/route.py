from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify

test = Blueprint('test', __name__, static_folder='static', template_folder='templates')

@test.route('/')
def index():
    return render_template('testing.html')