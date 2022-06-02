from siwat_light_control_protocol import siwat_light_control_protocol as slcp
from time import sleep as delay
import signal
import sys
import numpy
from time import perf_counter as millis
def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

led_map = [60,20]
leds = slcp("COM6",led_map,baudrate=115200)

NUM_LEDS = sum(led_map)

leds.turn_off()

color = [[255,0,0],[255,127,0],[255,255,0],
        [127,255,0],[0,255,0],[0,255,127],
        [0,255,255],[0,127,255],[0,0,255],
        [127,0,255],[255,0,255],[255,0,127]]
array = numpy.random.randint(low=0,high=9,size=NUM_LEDS)

def update_led():
    for i in range(0,NUM_LEDS):
        leds.set_led_at(i,r=color[array[i]][0],g=color[array[i]][1],b=color[array[i]][2])
    leds.show()

while True:
    array = numpy.random.randint(low=0,high=9,size=NUM_LEDS)
    update_led()
    #delay(0.1)
    