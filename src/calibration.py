"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711


hx = HX711(dout=5, pd_sck=6)


def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()


def loop():
    idx = 0
    samples = [0, 0, 0, 0]
    avrg = 0

    print 'Samples                                          Average'
    
    try:
        hx.reset()
        
        for i in range(4):
            samples[i] = hx.read_average_LPF() # including running average
#            samples[i] = hx.read_average_no_spikes(times=9) # Try as well?
            print samples[i], ','

        avrg = (samples[0] + samples[1] + samples[2] + samples[3]) / 4
        print '        ', avrg
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


##################################

if __name__ == "__main__":
    print "Press Enter when ready, 'q' for quit"
    while True:
        q = raw_input()
        if q == 'q':
            cleanAndExit()
        loop()
