from flask import Blueprint, url_for, render_template

configurations = Blueprint('configurations', __name__, static_folder="static", template_folder="templates")

@configurations.route('/')
def index():
    return render_template('configurations_index.html')

@configurations.route('/trans-tester')
def transTester():
    return render_template('trans-tester.html')