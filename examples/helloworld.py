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

from MOVI import *

mymovi = MOVI()
mymovi.init(serialport='/dev/serial0')

print("     API Version: " + str(mymovi.getAPIVersion()))
print("Firmware Version: " + str(mymovi.getFirmwareVersion()))
print("Hardware Version: " + str(mymovi.getHardwareVersion()))

mymovi.addSentence("Hello New World")
mymovi.addSentence("Let there be light")
mymovi.addSentence("Goodnight")
mymovi.callSign("Arduino2")
mymovi.train()
if mymovi.isReady() == True :
    mymovi.say("MOVI is Ready")
else:
    mymovi.say("MOVI not Ready")
while True:
    res = mymovi.poll()
    if res != 0:
        print(mymovi.getResponse())
