# ********************************************************************
# This is an example of the use of the Raspberry Pi library for MOVI
# ----> http://www.audeme.com/MOVI/
# This code is inspired and maintained by Audeme but open to change
# and organic development on GITHUB:
# ----> https://github.com/audeme/MOVIPiAPI
# Written by Bertrand Irissou and Gerald Friedland for Audeme LLC.
# Contact: fractor@audeme.com
# BSD license, all text above must be included in any redistribution.
# ********************************************************************

#
# This basic example shows how to use MOVI(tm)'s API to build a voice 
# controlled clock / timer.  
#
# Circuitry:
#   Raspberry PI
#   MOVI + Raspberry PI adapter
#   Connect speaker to MOVI.
# IMPORTANT: Use a power supply that's at least 2A for the Raspberry Pi
#

from movi import MOVI
from time import sleep
import datetime as _datetime
import sys


############################################
# Setup MOVI
############################################

recognizer = MOVI()
recognizer.init(serialport="/dev/serial0")

recognizer.callSign("Raspberry"); # Train callsign (may take 20 seconds)

recognizer.addSentence("What time is it ?")        # Add sentence 1
recognizer.addSentence("What is the time ?")       # Add sentence 2
recognizer.addSentence("What is the date ?")       # Add sentence 3
recognizer.addSentence("What is today ?")          # Add sentence 4
recognizer.addSentence("Cancel timer")             # Add sentence 5
recognizer.addSentence("Is timer set ?")           # Add sentence 6
recognizer.addSentence("How much time remaining ?")# Add sentence 7
recognizer.addSentence("Set Timer for 1 minute")   # Add sentence 8
recognizer.addSentence("Set Timer for 2 minutes")  # Add sentence 9
recognizer.addSentence("Set Timer for 3 minutes")  # Add sentence 10
recognizer.addSentence("Set Timer for 4 minutes")  # Add sentence 11
recognizer.addSentence("Set Timer for 5 minutes")  # Add sentence 12
recognizer.addSentence("Countdown")                # Add sentence 13

recognizer.train()

# Uncomment and set to a higher value if you have a noisy environment
# recognizer.setThreshhold(5)

elapsed   = 0
TimerOn   = 0
Countdown = -1


recognizer.say("Real Time Clock Starting")

############################################
# Main Loop - Runs forever
############################################
while True:

    now = _datetime.datetime.now()      # now is current time
    minute = now.minute
    hour   = now.hour
    day    = now.day
    month  = now.month
    monthname  = now.strftime("%B")
    year   = now.year

    res = recognizer.poll()             # check MOVI for new sentence.      

    ######### Sentence #1 or #2 Detected
    ######### Tell current time
    if res == 1 or res == 2:
        if minute < 10:
            ostr = "O"
        else:
            ostr = ""
        if hour > 12 :
            saystr = "It's %d %s %d PM" % (hour-12, ostr, minute)
        else:
            saystr = "It's %d %s %d AM" % (hour, ostr, minute)
        recognizer.say(saystr)

    ######### Sentence #3 or #4 Detected
    ######### Tell current date
    if res == 3 or res == 4:
        saystr = "Today is %s %d %d" % (monthname, day, year)
        recognizer.say(saystr)
        
    ######### Sentence #5 Detected
    ######### Cancel Time
    if res == 5:
        TimerOn = 0
        recognizer.say("Timer was cancelled")

    ######### Sentence #6 or #7 Detected
    ######### Check Timer Status
    if res == 6 or res == 7:
        if TimerOn:
            if res == 6:
                recognizer.say("Yes")
            TimeLeft = int((TimerEndTime-now).total_seconds())
            minleft = int (TimeLeft / 60)
            secleft = int (TimeLeft % 60)
            if minleft:
                saystr = "%d minutes and %d seconds left on timer" % ( minleft, secleft)
            else:
                saystr = "%d seconds left on timer" % secleft
        else:
            saystr = "Timer is not set"
        recognizer.say(saystr)

    ######### Sentence #8 through #12 Detected
    ######### Check Timer Status
    if res >= 8 and res <= 12:
        if TimerOn:
            saystr = "Timer is already set. Say Cancel timer to stop it"
        else:
            TimerOn = 1
            duration = (res-7) # Timer duration in minutes
            TimerEndTime = now + _datetime.timedelta(0, duration * 60)
            saystr = "Timer set for %d minutes" % duration
        recognizer.say(saystr)

            
    ######### Sentence #13 Detected
    ######### 10 second countdown
    if res == 13:
        Countdown = 11
        CountdownEndTime = now + _datetime.timedelta(0, 11)

    if Countdown >= 0 and ((CountdownEndTime-now).total_seconds()) != Countdown:
        Countdown -= 1 
        recognizer.say("%d" % Countdown)

    if TimerOn and TimerEndTime <= now:
        TimerOn = 0
        recognizer.say("Time is up!")

    res = 0
