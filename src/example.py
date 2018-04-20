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
from hx711   import HX711
from hx711_2 import HX711_2

hx = HX711(dout=5, pd_sck=6)
#hx = HX711(dout=20, pd_sck=21)
#hx = HX711_2(dout_1=5, pd_sck_1=6, dout_2=20, pd_sck_2=21)


def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()


def setup():
    """
    code run once
    """
    # 1 (average) ratio
    # hx.set_offset(8628588.560)
    # hx.set_ratio(1656.565317)

    # TODO 7 ratios for 25, 75, 150, 225, 300, 375, 475 ref. grams
    # hx.set_offset(8628270.340)
    # hx.set_ratios((8670386.533,1684.648), (8752399.907,1655.061), (8876659.720,1655.929), (9001015.187,1656.644), (9125726.580,1658.187), (9249752.487,1657.286), (9415005.647,1656.285))

    # 4 ratios for 25, 100, 175, 250 ref grams
#    hx.set_offset(8628906.780)
#    hx.set_ratios((8671186.060,1691.171), (8794613.307,1657.065), (8918932.973,1657.293), (9043501.513,1658.379))
# Sensor 1
    hx.set_offset(8630374.401)
    hx.set_ratios((8671180.728,1632.253), (8794814.094,1644.397), (8918636.358,1647.211), (9043647.085,1653.091))
# Sensor 2
#    hx.set_offset(8531229.086)
#    hx.set_ratios((8552767.321,861.529), (8620017.884,887.888), (8686818.724,889.084), (8753424.537,888.782))
# Sensors 1 and 2
#    hx.set_offset(18229794.023)
#    hx.set_ratios((18268919.776,1565.030), (18320473.491,906.795), (18375631.173,833.355), (18441637.077,847.372))

    hx.tare()


def loop():
    """
    Use the different read methods (for comparison)
    """

    print 'average         avrg_no_spikes       low-pass filter           avrg of the 3'

    while True:
        try:
            # TODO: Read only once (9, 16, or 25 samples) and calculate the 3 values
            v_1 = hx.read_average(times=16)
            v_2 = hx.read_average_no_spikes(times=16)
            v_3 = hx.read_average_LPF()

            g_1 = hx.to_grams( v_1 )
            g_2 = hx.to_grams( v_2 )
            g_3 = hx.to_grams( v_3 )

            print hx.round_to(g_1, 0.25), ',', hx.round_to(g_1, 0.5), '        ',
            print hx.round_to(g_2, 0.25), ',', hx.round_to(g_2, 0.5), '        ',
            print hx.round_to(g_3, 0.25), ',', hx.round_to(g_3, 0.5), '        ',
            print hx.round_to((g_1 + g_2 + g_3)/3, 0.25), 'g'

#            time.sleep(1)
            hx.reset()

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


def loop_1():
    idx = 0
    samples = [0, 0, 0, 0] # used as circular buffer
    avrg = 0

    print 'Samples               Average of 4 in a circular buffer'

    while True:
        try:
            """
            for i in range(4):
                samples[i] = hx.read_average_LPF() # including running average
                samples[i] = hx.to_grams( samples[i] )
                print hx.round_to(samples[i], 0.25), ',', hx.round_to(samples[i], 0.5)

            print '                             ',
            print hx.round_to((samples[0] + samples[1] + samples[2] + samples[3]) / 4, 0.25), 'g'
            """

            samples[idx] = hx.read_average_LPF() # TODO: Use the other functions as well?
            samples[idx] = hx.to_grams( samples[idx] ) # TODO: avrg before or after the rounding?
            avrg = (samples[0] + samples[1] + samples[2] + samples[3]) / 4
            #avrg = (avrg + samples[idx]) / 2 # Running average

            print hx.round_to(samples[idx], 0.25), ',', hx.round_to(samples[idx], 0.5), '        ',
            print hx.round_to(avrg, 0.25), ',', hx.round_to(avrg, 0.5), 'g'

            idx = (idx + 1) % 4 # modulo counter

            hx.reset()

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

##################################

if __name__ == "__main__":
    setup()
    #loop()
    loop_1()
