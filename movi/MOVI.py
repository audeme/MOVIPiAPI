#********************************************************************
# This is a library for the Audeme MOVI Voice Control Shield
# ----> http://www.audeme.com/MOVI/
# This code is inspired and maintained by Audeme but open to change
# and organic development on GITHUB:
# ----> https://github.com/audeme/MOVIPiAPI
# Written by Bertrand Irissou and Gerald Friedland for Audeme LLC.
# Contact: fractor@audeme.com
# BSD license, all text above must be included in any redistribution.
#********************************************************************

import serial
import sys
import time

# 07/27/18 - v0.1 Initial version
# 07/29/18 - v0.2 fixed various bugs, added password functionality, added controlled sendcommand functionality and uses it during initialization and training
# 10/20/18 - v0.3 fixed more bugs
# 11/20/18 - v0.4 more fixes

# Equivalent of #define in C++
API_VERSION = 1.20
ARDUINO_BAUDRATE = 9600
SHIELD_IDLE = 0
BEGIN_LISTEN = -140
END_LISTEN = -141
BEGIN_SAY = -150
END_SAY = -151
CALLSIGN_DETECTED = -200
RAW_WORDS = -201
PASSWORD_ACCEPT = -204
PASSWORD_REJECT = -404
NOISE_ALARM = -530
SILENCE = -501
UNKNOWN_SENTENCE = -502

MALE_VOICE = False
FEMALE_VOICE = True

SYNTH_ESPEAK = 0
SYNTH_PICO = 1


class MOVI():

    def __init__(self):
        self.__passstring = ""    # stores password challenge
        self.__hardwareversion = 0     # stores hardware version
        self.__firmwareversion = 0     # stores firmware version
        self.__shieldinit = 0     # stores the init state of the MOVI object
        self.__callsigntrainok = True  # makes sure callsign is only called once
        self.__debug = 0     # debug allows serial monitor interfacing
        self.__intraining = False  # determines if training is ok
        self.__firstsentence = True  # determines if addSentence() has been called
        self.__response = ""    # stores the stream of the last serial com result
        self.__result = ""    # stores the last result of getResult()

    def init(self, waitformovi=1, serialport='/dev/serial0'):
        self.__response = ""
        self.__result = ""
        self.__ser = serial.Serial(port=serialport,
                                   parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   bytesize=serial.EIGHTBITS,
                                   baudrate=9600,
                                   timeout=0.1)
        self.__pyv = sys.version_info.major
        if self.__ser.isOpen() == False:
            try:
                self.__ser.open()
            except:
                print ("Error communicating with serial port")
                exit()

        self.__shieldinit = 1
        while waitformovi and (self.isReady() == False):
            # This is a longer sleep than Arduino but the CPU is faster too.
            time.sleep(0.1)

        while True:
            self.__ser.write(self.__makeCommand("INIT"))
            time.sleep(0.1)
            response = self.getShieldResponse()
            if response.find('@') > -1:
                break
        self.__firmwareversion = float(
            response[response.find(' ') + 1:response.find('@')])
        self.__hardwareversion = float(response[response.find('@') + 1:])

    def poll(self):
        self.__firstsentence = False  # Assume loop() and we can't train in loop
        self.__intraining = False
        self.getShieldResponse()
        if "MOVIEvent[" in self.__response:
            start = self.__response.find('[')
            stop = self.__response.find(']')
            # eventno = int(self.__response[start+1:stop])
            eventno = int(self.__response[self.__response.find('[') + 1:
                                          self.__response.find(']')])
            self.__result = self.__response[self.__response.find(' ') + 1:]

            if (eventno < 100):  # user read-only event
                #self.__response = ""
                return(SHIELD_IDLE)
            if (eventno == 202):  # sentence recognized
                self.__result = self.__response[self.__response.find('#') + 1:]
                #self.__response = ""
                return(int(self.__result) + 1)
            if (eventno == 203):  # password event
                self.__response = ""
                self.__result = self.__result.strip()
                if (self.__passstring.equals(self.__result)):
                    return PASSWORD_ACCEPT
                else:
                    return PASSWORD_REJECT

            #self.__response = ""
            return(-eventno)
        else:
            return (SHIELD_IDLE)

    def getResult(self):
        return(self.__result)

    def getResponse(self):
        return(self.__response)

    def getShieldResponse(self):
        # Simplified version
        if (self.__shieldinit == 0):
            self.init()
        else:
            self.__response = self.__ser.readline()
        if self.__pyv == 3:
            self.__response = self.__response.decode()
        return(self.__response)

    def sendCommand(self, command, okresponse=None):
        if (okresponse == None):
            return(self.__sendCommand(command))
        else:
            return(self.__sendctrldCommand(command, okresponse))

    def __sendCommand(self, command):
        if (self.__firstsentence or self.__intraining):
            # Use controlled sendCommand
            return(self.__sendctrldCommand(command, "]"))
        # TODO - Implement firstsentence OR intraining cases
        self.__ser.write(self.__makeCommand(command))
        return(self.getShieldResponse())

    def __sendctrldCommand(self, command, okresponse):
        if (self.isReady()):
            self.__ser.write(self.__makeCommand(command))
            if (okresponse == ""):
                return True
            if (self.getShieldResponse().find(okresponse) >= 0):
                return True
            else:
                return False
        else:
            return False

    def __makeCommand(self, command):
        c = command + '\n'
        if self.__pyv == 3:
            c = str.encode(c)
        return c

    def isReady(self):
        if self.__shieldinit == 100:
            return(True)
        if self.__shieldinit == 0:
            self.init()
        self.__ser.write(self.__makeCommand("PING"))
        if "PONG" in self.getShieldResponse():
            self.__shieldinit = 100
            return(True)
        self.__shieldinit = 1
        return(False)

    def factoryDefault(self):
        self.sendCommand("FACTORY")

    def stopDialog(self):
        self.sendCommand("STOP")

    def restartDialog(self):
        self.sendCommand("RESTART")

    def say(self, sentence):
        self.sendCommand("SAY " + sentence)

    def pause(self):
        self.sendCommand("PAUSE")

    def unpause(self):
        self.sendCommand("UNPAUSE")

    def finish(self):
        self.sendCommand("FINISH")

    def play(self, filename):
        self.sendCommand("PLAY " + filename)

    def abort(self):
        self.sendCommand("ABORT")

    def setSynthesizer(self, synth, commandline=""):
        if (synth == SYNTH_PICO):
            self.sendCommand("SETSYNTH PICO " + commandline)
        else:
            self.sendCommand("SETSYNTH ESPEAK " + commandline)

    def ask(self, question=""):
        if question != "":
            self.say(question)
        self.sendCommand("ASK")

    def password(self, question, passkey):
        self.__passstring = passkey.strip().upper()
        self.say(question)
        self.sendCommand("PASSWORD")

    def callSign(self, callsign):
        if (self.__callsigntrainok):
            self.sendCommand("CALLSIGN " + callsign, "callsign")
            self.__callsigntrainok = False

    def responses(self, on):
        if (on == True):
            self.sendCommand("RESPONSES ON")
        else:
            self.sendCommand("RESPONSES OFF")

    def welcomeMessage(self, on):
        if (on == True):
            self.sendCommand("WELCOMEMESSAGE ON")
        else:
            self.sendCommand("WELCOMEMESSAGE OFF")

    def beeps(self, on):
        if (on == True):
            self.sendCommand("BEEPS ON")
        else:
            self.sendCommand("BEEPS OFF")

    def setVoiceGender(self, female):
        if (female == True):
            self.sendCommand("FEMALE")
        else:
            self.sendCommand("MALE")

    def setVolume(self, volume):
        self.sendCommand("VOLUME " + str(volume))

    def setThreshold(self, threshold):
        self.sendCommand("THRESHOLD " + str(threshold))

    def getFirmwareVersion(self):
        return(self.__firmwareversion)

    def getAPIVersion(self):
        return(API_VERSION)

    def getHardwareVersion(self):
        return(self.__hardwareversion)

    def addSentence(self, sentence):
        if (self.__firstsentence == True):
            self.__intraining = self.sendCommand("NEWSENTENCES ", "210")
            self.__firstsentence = False
        if (self.__intraining == False):
            return(False)
        self.__intraining = self.sendCommand("ADDSENTENCE " + sentence, "211")
        return (self.__intraining)

    def train(self):
        if (self.__intraining == False):
            return(False)
        self.sendCommand("TRAINSENTENCES", "trained")
        self.__intraining = False
        return (True)
