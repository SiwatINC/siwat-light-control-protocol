from siwat_remote_light_control_protocol_client import siwat_remote_light_control_protocol_client as srlcp
from time import sleep as delay
import signal
import sys
import numpy
from scipy.ndimage.interpolation import shift
from time import perf_counter as millis
import threading
from secrets import MQTT_SERVER, MQTT_PORT, MQTT_USE_AUTH, MQTT_USERNAME, MQTT_PASSWORD, LIGHT_ADDRESS
def sigint_handler(signal, frame):
    
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

leds = srlcp(mqtt_server=MQTT_SERVER, mqtt_port=MQTT_PORT, light_address=LIGHT_ADDRESS,
            mqtt_use_auth=MQTT_USE_AUTH, mqtt_username=MQTT_USERNAME, mqtt_password=MQTT_PASSWORD)

leds.enter_programming_mode()

NUM_LEDS = leds.num_leds
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




