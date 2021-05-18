import serial, serial.tools.list_ports
from flask import session
import time

class Arduino():
    arduino = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.arduino = self.find_arduino('75735353138351912001')
            time.sleep(3)
            print("device instantiation success")
            print(self.arduino)
            print(self.arduino.port)
        except Exception as e:
            print("device instantiation exception")
            print(str(e))
    
    def find_arduino(self, serial_number):
        for pinfo in serial.tools.list_ports.comports():
            if pinfo.serial_number == serial_number:
                return serial.Serial(pinfo.device)
        raise IOError('Failed to find arduino')

    def read(self):
        try:
            self.arduino.flush()
            time.sleep(1)
            return str(self.arduino.readline(self.arduino.inWaiting()).strip())
            # return self.arduino.read(self.arduino.readline())
        except Exception as e:
            return str(e)

    def write(self, input):
        try:
            self.arduino.flush()
            time.sleep(1)
            self.arduino.write(bytes(input, 'utf-8'))
            print(input+" writen")
            return True
        except Exception as e:
            print(str(e))
            return False

    def port(self):
        if self.arduino:
            return self.arduino.port
        else:
            return None

    def connected(self):
        return self.arduino is not None