#********************************************************************
# This is an example of the use of the Raspberry Pi library for MOVI 
# ----> http://www.audeme.com/MOVI/
# This code is inspired and maintained by Audeme but open to change
# and organic development on GITHUB:
# ----> https://github.com/audeme/MOVIPiAPI
# Written by Bertrand Irissou and Gerald Friedland for Audeme LLC.
# Contact: fractor@audeme.com
# BSD license, all text above must be included in any redistribution.
#********************************************************************

#
# This basic example shows how to use MOVI(tm)'s API to train the call 
# sign "Raspberry" and two sentences. When the sentences are recognized
# they switch on and off an LED on PIN D13. Many boards have a hardwired 
# LED on board already connected to D13.
#
# Circuitry:
# LED is pin D13 and GND
# Works on Raspberry PI
# Connect speaker to MOVI.
# IMPORTANT: Use a power supply that's at least 2A for the Raspberry Pi
# 

# Note: MOVI uses GPIO pins 14 (TXD0) and 15 (RXD0)

import RPi.GPIO as GPIO
import time
from MOVI import *

############################################
### Setup GPIO Pin 13 as Ouput to control LED
############################################
iopin = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(iopin,GPIO.OUT)
GPIO.output(iopin,True)
time.sleep(1)
GPIO.output(iopin,False)
time.sleep(1)

############################################
### Setup MOVI
############################################

recognizer = MOVI()
recognizer.init(serialport='/dev/serial0')

recognizer.callSign("Raspberry")
recognizer.addSentence("Let there be light")        # Sentence #1
recognizer.addSentence("Go dark")                   # Sentence #2
recognizer.train()

# Uncomment and set to a higher value if you have a noisy environment
# recognizer.setThreshhold(5)   

############################################
### Main Loop - run over and over
############################################
while True:
    res = recognizer.poll()

    if res == 1:                    # Sentence #1
        GPIO.output(iopin, True)
        recognizer.say("and there was light!")
    if res == 2:                    # Sentence #2
        GPIO.output(iopin, False)
        recognizer.say("Goodnight")
