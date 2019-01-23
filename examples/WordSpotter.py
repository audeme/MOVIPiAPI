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
# Raspberry PI
# MOVI adapter + MOVI
# Connect speaker to MOVI.
# IMPORTANT: Use a power supply that's at least 2A for the Raspberry Pi
#

from movi import MOVI

# Keyword in UPPERCASE
KEYWORD = "computer"

############################################
# Setup MOVI
############################################

recognizer = MOVI()
recognizer.init(serialport='/dev/serial0')

recognizer.addSentence(KEYWORD)

# The training functions are "lazy" and only do something if there are changes.

# Add keyword as sentence 1
recognizer.addSentence(KEYWORD)

# Add the top-50 most frequent English words as 'background model'.
# This way, the keyword is not triggered by other random words.
# See MOVI's user manual for a more detailed explanation on this.
recognizer.addSentence("the be to of and a")
recognizer.addSentence("in that have I it for")
recognizer.addSentence("not on with he as you")
recognizer.addSentence("do at this but his by")
recognizer.addSentence("from they we say her she")
recognizer.addSentence("or an will my one all would")
recognizer.addSentence("there their what so up out")
recognizer.addSentence("if about who get which go me")

recognizer.train()


recognizer.welcomeMessage(False)    # silence MOVI's welcome message
recognizer.responses(False)         # silence MOVI's responses
recognizer.beeps(False)            # silence MOVI's beeps
# Uncomment and set to a higher value if you have a noisy environment
# recognizer.setThreshhold(5)

# The ask method speaks the passed string and then directly listens
# for a response (after beeps, but beeps are turned off).
recognizer.ask("Listening. I react to the word " + KEYWORD)

############################################
# Main Loop - run over and over
############################################
#
# result string is uppercase so convert keyword to uppercase
KEYWORD = KEYWORD.upper()

while True:
    # Get result from MOVI, 0 denotes nothing happened,
    # negative values denote events (see User Manual)
    res = recognizer.poll()

    # The event raw_words let's us get the raw words via getResult()
    if res == RAW_WORDS:
        # if the raw result string contains the (uppercase) keyword
        # string: bingo!
        if (KEYWORD in recognizer.getResult()):
            # say keyword has been spotted and listen again
            recognizer.ask("keyword spotted")
        else:
            # silently listen again
            recognizer.ask()
