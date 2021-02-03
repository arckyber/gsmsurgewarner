from flask import Blueprint, render_template, jsonify
import serial, serial.tools.list_ports
import time
time.sleep(3)

arduinosdfsdf = Blueprint("arduinosdfsdf", __name__, static_folder="static", template_folder="templates")
# device = None
@arduino.route('/render', methods=['POST', 'GET'])
def render():
	try:
		device = find_arduino('75735353138351912001')
		time.sleep(2)
		if device.port:
			print(device)
			return jsonify({
				'connected':True,
				'baudrate':device.baudrate,
				'port':device.port,
				# 'device':device,
			})
		else:
			print("no port")
			return jsonify({'connected':False})
	except:
		print("exception occured")
		return jsonify({'connected':False})

def find_arduino(serial_number):
	for pinfo in serial.tools.list_ports.comports():
		if pinfo.serial_number == serial_number:
			return serial.Serial(pinfo.device)
	raise IOError('Failed to find arduino')

@arduino.route('/send')
def send():
	device = None
	try:
		device = find_arduino('75735353138351912001')
		time.sleep(2)
		if device:
			device.flushInput()
			device.flushOutput()
			device.write(bytes('3', 'utf-8'))
			return str(device)
		else:
			print("Cannot find device")
	except Exception as e:
		return f"<h1>Error!</h1>" + str(e)
	finally:
		if device:
			device.close()
	return f"<h1>arduino->send()</h1>"

@arduino.route('/receive')
def receive():
	device = None
	try:
		# device = find_arduino('75735353138351912001')
		device = serial.Serial('COM6', 9600)
		time.sleep(2)
		device.flush()
		if device:
			time.sleep(.50)
			data = device.read(device.inWaiting())
			return str(data)
		else:
			return "No device found"
	except Exception as e:
		return "Exception: " + str(e)
	finally:
		if device:
			device.close()
	return f"<h1>arduino->receive()</h1>"

@arduino.route('/light')
def light():
	return render_template('light.html')

@arduino.route('/light/on')
def light_on():
	try:
		device = find_arduino('75735353138351912001')
		# device = serial.Serial('COM6', 9600)
		time.sleep(2)
		device.write(bytes('H', 'utf-8'))
	except Exception as e:
		return str(e)
	return "On"

@arduino.route('/light/off')
def light_off():
	try:
		device = find_arduino('75735353138351912001')
		time.sleep(2)
		device.write(bytes('L', 'utf-8'))
	except Exception as e:
		return str(e)
	return "Off"

# ser = serial.Serial(str(device.port), baudrate=19200, timeout=1)
# val = ser.readline().decode('utf-8')