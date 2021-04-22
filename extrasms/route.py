from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from sqlalchemy import desc, func, asc

from model.models import Extra, ExtraSchema, ExtraSms, ExtraSmsSchema, db

extrasms = Blueprint('extrasms', __name__, static_folder="static", template_folder="templates")

@extrasms.route('/')
def index():
	if 'extrasms' not in session['role_access']:
		return redirect(url_for('users.rightAccessControl'))
	return render_template('/extrasms-index.html')

@extrasms.route('/unread_count', methods=['POST'])
def unread_count():
	count = db.session.query(func.count(Extra.id)).filter(Extra.is_opened == False, Extra.status == True).scalar()
	return str(count)

@extrasms.route('/unread', methods=['POST'])
def unread():
	sms = Extra.query.filter(Extra.is_opened == False, Extra.status == True).order_by(desc(Extra.created_at)).limit(3)
	output = ExtraSchema(many=True).dump(sms)
	return jsonify(output)

@extrasms.route('/unreads')
def unreads():
	sms = Extra.query.filter(Extra.status == True, Extra.is_opened == False).order_by(desc(Extra.created_at)).limit(3)
	output = ExtraSchema(many=True).dump(sms)
	return jsonify(output)

@extrasms.route('/clear')
def clear():
	db.session.query(Extra).delete()
	db.session.commit()
	return "Deleted"

@extrasms.route('/show', methods=['POST', 'GET'])
def show():
	smsdum = Extra.query.filter(Extra.status == True).order_by(desc(Extra.date_sent)).all()
	ouput = ExtraSchema(many=True).dump(smsdum)
	return jsonify(output)

@extrasms.route('/delete', methods=['POST'])
def delete():
	try:
		id = request.form['id']
		extra = Extra.query.filter(Extra.id == id).first()
		print(extra)
		extra.status = False
		db.session.commit()
		return "success"
	except Exception as e:
		return str(e)

@extrasms.route('/view', methods=['POST'])
def view():
	if request.method == 'POST':
		id = request.form['id']

		# mark as read
		e = Extra.query.filter(Extra.status == True, Extra.id == id).first()
		e.is_opened = True
		db.session.commit()

		extra = Extra.query.filter(Extra.status == True, Extra.id == id).first()
		output = ExtraSchema(many=False).dump(extra)
		return jsonify(output)
	else:
		return "Invalid method"
