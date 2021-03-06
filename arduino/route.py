from flask import Blueprint, render_template, jsonify, request
from arduino.arduino import Arduino as Ard
import time
from config.const import SUCCESS, FAILED, ERROR, MISSING_DATA, SIMNUMBER_INDEX, SOURCE_INDEX, CMD_INDEX, MSG_INDEX, DATETIME_INDEX, DISTANCE_INDEX, ALERT_TYPE_INDEX
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema, db, Extra, ExtraSchema
import datetime
import dateparser
from sqlalchemy import asc, desc

print("diri ni sa arduino nga blueprint..............")
ard = Ard()

SEND = "SEND"
SAVE = "SAVE"

# Syntax for sending, saving message

# CMD:SIM_NUMBER:MESSAGE:DATE
# Example:
# =>  
# =>  


arduino = Blueprint("arduino", __name__, static_folder="static", template_folder="templates")

@arduino.route('/write-message')
def write_message():
	return render_template('write-message.html')

@arduino.route('/smslist')
def smslist():
	return render_template('smslist.html')

@arduino.route('/smsdum', methods=['POST', 'GET'])
def smsdum():
	smsdum = Extra.query.filter(Extra.status == True).order_by(desc(Extra.date_sent)).all()
	schema = ExtraSchema(many=True)
	output = schema.dump(smsdum)
	# print("printing smsdumoutput........................")
	return jsonify(output)

@arduino.route('/send', methods=['POST'])
def send():
	number = request.form['number']
	msg = request.form['message']
	data = "RECEIVER&SEND&"+msg+"&"+number+"&"+str(datetime.datetime.now())
	# print('Printing message to be send....................')
	# print(data)
	if ard.write(data):
		return SUCCESS
	else:
		return FAILED

@arduino.route('/test-trans')
def testTrans():
	try:
		data = ard.read()
		# strd = str(data)[]
		return str(data)
	except Exception as e:
		return str(e)

@arduino.route('/receivedum', methods=['POST'])
def receivedum():
	try:
		data = ard.read()
		if data:
			data = data.replace('b\'', '')
			data = data.replace('b\"', '')
			data = data[:-1]
			print('receive dum..............')
			print(data)

			# if simcard module is not initialized properly
			if "error" in data:
				return ERROR

			if "TRANSMITTER" in data:
				dataArr = data.split('&')
				transmitter = Transmitter.query.filter(Transmitter.sim_number == dataArr[SIMNUMBER_INDEX]).first()
				if transmitter:
					sms = Sms(
						alert_type = dataArr[ALERT_TYPE_INDEX],
						water_distance = dataArr[DISTANCE_INDEX],
						transmitter_id = transmitter.id,
						created_at = datetime.datetime.now(),
						date_sent = dateparser.parse(dataArr[DATETIME_INDEX][:-3]),
						status = True,
						is_opened = False,
					)
					db.session.add(sms)
					db.session.commit()
					return SUCCESS
			else:
				dataArr = data.split('&')
				extra_obj = Extra(
					number = dataArr[SIMNUMBER_INDEX],
					message = dataArr[MSG_INDEX],
					date_sent = datetime.datetime.now(),
					created_at = datetime.datetime.now(),
					is_opened = False,
					status = True
				)
				db.session.add(extra_obj)
				db.session.commit()
				return SUCCESS
		return FAILED
	except Exception as e:
		print(str(e))
		return str(e)

@arduino.route('/delete-all-sms', methods=['POST'])
def delete_all_sms():
	try:
		db.session.query(Extra).delete()
		db.session.commit()
	except Exception as e:
		print(str(e))
	return jsonify({
		'success':True
	})

@arduino.route('/light')
def light():
	return render_template('light.html')

@arduino.route('/render', methods=['POST', 'GET'])
def render():
	if ard.port():
		return jsonify({
			'connected':True,
		})
	else:
		ard.connect()
		if ard.port():
			return jsonify({
				'connected':True,
			})
		else:
			return jsonify({
				'connected':False,
			})

if __name__ == '__main__':
	while True:
		# print('in main........')
		time.sleep(1)