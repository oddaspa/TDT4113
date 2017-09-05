'''This file provides a few of the 'tricky' elements of the Morse Code project: those
involving setting up and reading from the serial port.  

IMPORTANT!! If you are a MAC user, you will need to modify the actual device code for 
your serial port in arduino_connect.py '''

import arduino_connect  # This is the key import so that you can access the serial port.


# Codes for the 5 signals sent to this level from the Arduino

_dot = 1
_dash = 2
_symbol_pause = 3
_word_pause = 4
_reset = 5


# Morse Code Class
class mocoder():

# Note: the codes for dot and dash coming to Python via the serial port are 1 and 2, respectively, since those were most
# convenient at the Arduino level. However, I've switched to 0 and 1 in this dictionary, since it is a lot easier to
# read.  So O = dot, 1 = dash in the _morse_codes dictionary below.  You will need to remember that when looking
# up letters and digits in this dictionary.

    _morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
               '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
               '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
               '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}

	# This is where you set up the connection to the serial port.
    def __init__(self,sport=True):
        if sport:
            self.serial_port = arduino_connect.pc_connect()
        self.reset()

    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''

    # This should receive an integer in range 1-4 from the Arduino via a serial port
    def read_one_signal(self,port=None):
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data
                
    # The signal returned by the serial port is one (sometimes 2) bytes, that represent characters of a string.  So,
    # a 2 looks like this: b'2', which is one byte whose integer value is the ascii code 50 (ord('2') = 50).  The use
    # of function 'int' on the string converts it automatically.   But, due to latencies, the signal sometimes
    # consists of 2 ascii codes, hence the little for loop to cycle through each byte of the signal.

    def decoding_loop(self):
        while True:
            s = self.read_one_signal(self.serial_port)
            print(s)
            for byte in s:
                self.process_signal(int(chr(byte)))


    # Read the next signal from the serial port and return it.
    def read_one_signal(self, port=None):
        connection = port if port else self.serial_port
        while True:
        # Read the data from arduino_connect.py
            data = connection.readline()
            if data:
                return data

    # Examine the recently-read signal and call one of several methods, depending
    # upon the signal type. If it is a dot or dash, then call update current symbol; if it is a pause, then call
    # handle symbol end or handle word end depending upon the type of pause
    def process_signal(self, signal):
        # if we get a dot or dash append it to our current word.
        if (signal == 1 or signal == 2):
            self.update_current_symbol(signal)
        # if we get a letter pause signal we append the ascii letter to our word and add a space.
        elif signal == 3:
            self.handle_symbol_end()
            self.current_message += (" ")
        # if we get a word pause signal we print the word.
        elif signal == 4:
            self.handle_word_end()

    # Append the current dot or dash onto the end of current_symbol.
    def update_current_symbol(self, signal):
        if signal == 2:
            self.current_symbol += '1'
        if signal == 1:
            self.current_symbol += '0'


    # When the code for a symbol ends, use that code as a key into morse codes
    # to find the appropriate symbol, which is then used as the argument in a call to update current word.
    # Finally, reset current symbol to the empty string.
    def handle_symbol_end(self):
        value = self._morse_codes.get(self.current_symbol, '')
        self.update_current_word(value)
        self.current_symbol=""
    # Add the most recently completed symbol onto current word.
    def update_current_word(self, symbol):
        self.current_word += (symbol)
    # This should begin by calling handle symbol end; it should then print current
    # word to the screen and, finally, reset current word to the empty string.
    def handle_word_end(self):
        self.handle_symbol_end()
        print(self.current_word)
        self.reset()





''' To test if this is working, do the following in a Python command window:

> from morse_skeleton import *
> m = mocoder()
> m.decoding_loop()

If your Arduino is currently running and hooked up to the serial port, then this
simple decoding loop will print the raw signals that the Arduino sends to
the serial port.  Each time you press (or release) your morse-code device, a signal should
appear in your Python window. In Python, these signals typically look like this:
 b'5' or b'1' or b'3', etc.
'''
m = mocoder()
m.decoding_loop()