from flask import Blueprint, render_template, jsonify, request
from arduino.device import Arduino as Ard
import time

print("diri ni sa arduino nga blueprint..............")
ard = Ard()

arduino = Blueprint("arduino", __name__, static_folder="static", template_folder="templates")

@arduino.route('/read', methods=['POST'])
def read():
	data = ard.read()
	return jsonify({'data':str(data)})

@arduino.route('/light')
def light():
	return render_template('light.html')

@arduino.route('/write', methods=['POST'])
def write():
	message = request.form['message']
	ard.write(message)
	return message

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
				'connected':True,
			})

if __name__ == '__main__':
	while True:
		print('in main........')
		time.sleep(1)