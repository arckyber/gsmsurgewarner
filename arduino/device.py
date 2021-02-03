import serial, serial.tools.list_ports
import time

class Arduino():
    arduino = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.arduino = serial.Serial('COM6', 9600)
            time.sleep(3)
            print("device instantiation success")
            print(self.arduino)
        except Exception as e:
            print("device instantiation exception")
            print(str(e))

    def read(self):
        try:
            self.arduino.flush()
            time.sleep(1)
            return self.arduino.read(self.arduino.inWaiting())
        except Exception as e:
            return str(e)

    def write(self, input):
        try:
            self.arduino.flush()
            time.sleep(1)
            self.arduino.write(bytes(input, 'utf-8'))
            print(input+" writen")
            return input
        except Exception as e:
            return str(e)

    def port(self):
        if self.arduino:
            return self.port
        else:
            return None