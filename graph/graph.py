from flask import Blueprint, render_template, url_for, current_app, request, flash

graph = Blueprint('graph', __name__, static_folder='static', template_folder='templates')

@graph.route('/index')
@graph.route('/')
def index():
	return render_template('graph_index.html')