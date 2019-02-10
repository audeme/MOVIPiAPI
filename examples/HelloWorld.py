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

from movi import MOVI

mymovi = MOVI()
mymovi.init(serialport='/dev/serial0')

print("Found MOVI board:")
print("     API Version: " + str(mymovi.getAPIVersion()))
print("Firmware Version: " + str(mymovi.getFirmwareVersion()))
print("Hardware Version: " + str(mymovi.getHardwareVersion()))

print("Training callsign")
mymovi.callSign("Raspberry")

print("Training sentences:")
mymovi.addSentence("Hello")
print("1) Hello")
mymovi.addSentence("Good night")
print("2) Good night")
mymovi.train()
mymovi.say("Call me with Raspberry and wait for beep. Then speak sentence.") 
while True:
    res = mymovi.poll()
    if res!=0:
        print(mymovi.getResponse())
    if res==1:
	mymovi.say("World!")
    if res==2:
	mymovi.say("Bye Bye")
	
