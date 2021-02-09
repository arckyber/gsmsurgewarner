from flask import Blueprint, render_template, jsonify, request

extrasms = Blueprint('extrasms', __name__, static_folder="static", template_folder="templates")

@extrasms.route('/')
def index():
    return render_template('extrasms-index.html')