# MOVIPiAPI

This is the official repository of the Raspberry Pi API for MOVI. For
more information check out http://www.audeme.com/MOVI

## Getting MOVI to work on a Raspberry PI 3 or Pi ZeroW
1. Connect MOVI onto Raspberry Pi using adapter the Adapter sold by
Audeme or the wiring scheme in this
[Instructable](https://www.instructables.com/id/Untethered-Speech-Dialog-Using-MOVI-With-the-Rasbe/).
_Beware that some steps have changed._ This README presents an update.
Connect the Raspberry PI to a power supply with at least 2 Amperes. If
the power supply has not enough power, the Raspberry PI will complain
`Undervoltage detected` and show a ⚡️ in the upper right corner of the
screen.
1. Download latest
[Raspbian](https://www.raspberrypi.org/downloads/raspbian/). Install
on SDCard, start Raspberry PI, follow steps including updating
process.
1. Start a terminal and edit `/boot/config.txt` using your favorite editor like `sudo nano /boot/config.txt`. 
   Add the following lines to the end of the file:
   ``` 
   dtoverlay=pi3-disable-bt 
   core_freq=250
   enable_uart=1
   ```
1. Now edit `/boot/cmdline.txt`: ``` sudo nano /boot/cmdline.txt ```
   remove the word phrase `console=serial0,115200` or
   `console=ttyAMA0,115200`.
1. Reboot the Raspberry PI.
1. Find out which devices files exist now. This seems to be dynamic.
For me: `/dev/serial0` is the one that MOVI responds to. `/dev/ttyS0`
or `/dev/serial1` give an input/output error. The easiest way to find
out is to do an: ``` stty -a -F <devicefile> ``` where devicefile is
one of `/dev/ttyAMA0`, `/dev/serial0`, `/dev/ttyS0`, or
`/dev/serial1`. The one with the lowest number that doesn't return an
error should be used. For example if `/dev/ttyAMA0` and `/dev/serial1`
both work, try using `/dev/ttyAMA0` first.
1. You'll need setuptools for the installation.
   ```
   sudo apt-get install python3-setuptools
   ```
   or for python2
   ```
   sudo apt-get install python-setuptools
   ```
1. From this directory call `python3 setup.py install` or better yet
   install it into your `venv`.
1. Browse through the examples directory and play around with them.
All examples assume `/dev/serial0`. You may have to modify them if
that's not your device file.

## Version History
 * 0.1 initial version.
 * 0.2 various fixes.
 * 0.3 more fixes
 * 0.4 more fixes and a couple Python examples derived from Arduino examples
 * 0.5 python3, flake8, and `setup.py` added.
