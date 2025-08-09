control_servo.py

import time
import serial


def open():
 arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
 time.sleep(2)
 arduino.write(b'open\n')

def close():
 arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
 time.sleep(2)
 arduino.write(b'close\n')