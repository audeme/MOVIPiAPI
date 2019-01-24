#! /usr/bin/env python2

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
# This basic example shows how to use MOVI(tm)'s API to build a basic
# weather station using the web services APIs of ip-api.com and weather.gov
#
# Circuitry:
# Raspberry PI
# MOVI + Raspberry PI adapter
# Connect speaker to MOVI.
# IMPORTANT: Use a power supply that's at least 2A for the Raspberry Pi
#

from movi import MOVI
import urllib2
import json
import sys

############################################
# Setup MOVI
############################################

recognizer = MOVI()
recognizer.init(serialport='/dev/serial0')

recognizer.callSign("Weatherstation")
recognizer.addSentence("What's the temperature ?")        # Sentence #1
recognizer.addSentence("What's the forecast?")        # Sentence #2
recognizer.addSentence("do nothing")                   # Sentence #3
recognizer.train()

# Uncomment and set to a higher value if you have a noisy environment
# recognizer.setThreshhold(5)


try:
    # Automatically detect location based on geoIP
    full_url = "http://ip-api.com/json"
    location = json.loads(urllib2.urlopen(full_url).read().decode())
    city = location["city"].encode()
    latitude = str(location["lat"])
    longitude = str(location["lon"])

    # Get weather information at this location
    full_url = "https://api.weather.gov/points/" + latitude + "," + longitude
    weather = json.loads(urllib2.urlopen(full_url).read().decode())

except:
    sys.exit('Could not access server at ' + full_url)
    recognizer.say("There was a problem. I could not access internet")

recognizer.say("Weather station starting")

############################################
# Main Loop - run over and over
############################################
while True:
    res = recognizer.poll()

    ######### Sentence #1 Detected #############
    if res == 1:
        recognizer.say("Checking")
        try:
            # Get hourly forecast
            full_url = weather["properties"]["forecastHourly"]
            forecast_hourly = json.loads(
                urllib2.urlopen(full_url).read().decode())
            current_temp = forecast_hourly["properties"]["periods"][0]['temperature']

        except:
            sys.exit('Could not access weather server at ' + full_url)
            recognizer.say("There was a problem. I could not access internet")

        response = "the outside temperature in " + \
            city.encode() + " is " + str(current_temp).encode() + " degrees"
        print(response)
        recognizer.say(response)

    ######### Sentence #2 Detected #############
    if res == 2:
        recognizer.say("Checking")
        try:
            # Get detailed forecast
            full_url = weather["properties"]["forecast"]
            forecast = json.loads(urllib2.urlopen(full_url).read().decode())
            current_weather = forecast["properties"]["periods"][0]['detailedForecast']
            # current_weather = forecast["properties"]["periods"][0]['shortForecast']

        except:
            sys.exit('Could not access weather server at ' + full_url)
            recognizer.say("There was a problem. I could not access internet")

        response = str(current_weather).replace(
            " mph.", " miles per hour").encode()
        print(response)
        recognizer.say(response)

    ######### Sentence #3 Detected #############
    if res == 3:
        recognizer.say("nothing done")
