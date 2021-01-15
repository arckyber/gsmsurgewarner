from flask import Blueprint, render_template, jsonify

import serial, serial.tools.list_ports

arduino = Blueprint("arduino", __name__, static_folder="static", template_folder="templates")

@arduino.route('/render', methods=['POST', 'GET'])
def render():
	try:
		device = find_arduino('75735353138351912001')
		if device.port:
			return jsonify({'connected':True})
		else: 
			return jsonify({'connected':False})
	except:
		return jsonify({'connected':False})

def find_arduino(serial_number):
	for pinfo in serial.tools.list_ports.comports():
		if pinfo.serial_number == serial_number:
			return serial.Serial(pinfo.device)
	raise IOError('Failed to find arduino')

# ser = serial.Serial(str(device.port), baudrate=19200, timeout=1)
# val = ser.readline().decode('utf-8')