from siwat_light_control_protocol import siwat_light_control_protocol as slcp
from time import sleep as delay
import signal
import sys
import colorsys
import numpy
from time import perf_counter as millis
def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
led_map = [60]
leds = slcp("COM9",led_map=led_map)

NUM_LEDS = sum(led_map)-1

leds.turn_off()
color = [[255,0,0],[255,127,0],[255,255,0],
        [127,255,0],[0,255,0],[0,255,127],
        [0,255,255],[0,127,255],[0,0,255],
        [127,0,255],[255,0,255],[255,0,127]]
timecounter = 0
array = numpy.random.randint(low=0,high=9,size=60)

def update_led():
    for i in range(0,NUM_LEDS):
        leds.set_led_at(i,r=color[array[i]][0],g=color[array[i]][1],b=color[array[i]][2])
    leds.show()

while True:
    array = numpy.random.randint(low=0,high=9,size=60)
    isSorted = False
    for i in range(len(array)):

        # loop to compare array elements
        for j in range(0, len(array) - i - 1):

        # compare two adjacent elements
        # change > to < to sort in descending order
            if array[j] > array[j + 1]:

                # swapping elements if elements
                # are not in the intended order
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
                update_led()
                delay(0.1)
    