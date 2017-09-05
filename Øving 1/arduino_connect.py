__author__ = 'hakon0601'

''' This file enables your Python code to read from a serial port, which you must insure
 is the SAME serial port that your Arduino writes to.  

 The 'serial' module is part of the 'pyserial' package, which you can install via
 pip:  'pip3 install pyserial'
'''

import serial

# *** For PCs *****

# Connects to the arduino via a COM port (USB).
# Does not work if the serial monitor in arduino is open.
def pc_connect():
    for i in range(100):
        try:
            arduino = serial.Serial('COM' + str(i), 9600, timeout=.1)
            print("Connected to arduino")
            return arduino
        except serial.SerialException:
            pass
    exit("Arduino was not found")

    
