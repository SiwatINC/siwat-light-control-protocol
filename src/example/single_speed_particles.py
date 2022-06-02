from siwat_light_control_protocol import siwat_light_control_protocol as slcp
from time import sleep as delay
import signal
import sys
import colorsys
import numpy
from scipy.ndimage.interpolation import shift
from time import perf_counter as millis
import threading
def sigint_handler(signal, frame):
    
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

led_map = [30]
leds = slcp("COM9",led_map,baudrate=115200)

NUM_LEDS = sum(led_map)
TIME_UNIT = 0.1

global spaces
spaces = numpy.zeros(NUM_LEDS)

leds.turn_off()

def update_led():
    for i in range(0,NUM_LEDS):
        leds.set_led_at(i,r=int(spaces[i]*255),g=int(spaces[i]*255),b=int(spaces[i]*255))
        
    leds.show()
def advance_time_unit():
    global spaces
    while True:
        spaces = shift(spaces,1,cval=0)
        update_led()
        delay(TIME_UNIT)
atu = threading.Thread(target=advance_time_unit)
atu.start()

while True:
    input("Press Enter to Particle")
    spaces[0] = 1




