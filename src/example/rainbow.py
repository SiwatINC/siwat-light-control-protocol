from siwat_light_control_protocol import siwat_light_control_protocol as slcp
from time import sleep as delay
import signal
import sys
import colorsys
from time import perf_counter as millis
def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
led_map = [10]
leds = slcp("COM11",led_map,baudrate=38400,read_serial=False)
leds.turn_off()
SEGMENT_SIZE = 1
VELOCITY = 10
NUM_LEDS = sum(led_map)
color = []
k = 0
timecounter = 0
while(True):
    for j in range(0,NUM_LEDS):
        r, g, b = colorsys.hsv_to_rgb(((-timecounter*VELOCITY+j*4)%360)/360,1,1)
        leds.set_led_at(j,r=int(r*255),g=int(g*255),b=int(b*255))
        print("setting")
    timecounter+=1
    delay(0.1)
    print("showing")
    leds.show()
