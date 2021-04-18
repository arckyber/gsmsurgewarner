from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import desc, func, asc

from model.models import Extra, ExtraSchema, ExtraSms, ExtraSmsSchema, db

extrasms = Blueprint('extrasms', __name__, static_folder="static", template_folder="templates")

@extrasms.route('/')
def index():
    return render_template('extrasms-index.html')

@extrasms.route('/unread_count', methods=['POST'])
def unread_count():
	count = db.session.query(func.count(Extra.id)).filter(Extra.is_opened == False).scalar()
	return str(count)

@extrasms.route('/unread', methods=['POST'])
def unread():
	sms = Extra.query.filter(Extra.is_opened == False).order_by(desc(Extra.created_at)).limit(3)
	output = ExtraSchema(many=True).dump(sms)
	return jsonify(output)

@extrasms.route('/unreads')
def unreads():
	sms = Extra.query.filter(Extra.is_opened == False).order_by(desc(Extra.created_at)).limit(3)
	output = ExtraSchema(many=True).dump(sms)
	return jsonify(output)

@extrasms.route('/clear')
def clear():
	db.session.query(Extra).delete()
	db.session.commit()
	return "Delted"

@extrasms.route('/show')
def show():
	query = Extra.query.all()
	output = ExtraSchema(many=True).dump(query)
	return jsonify(output)