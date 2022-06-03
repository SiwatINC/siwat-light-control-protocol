from siwat_remote_light_control_protocol_client.siwat_remote_light_control_protocol_client import siwat_remote_light_control_protocol_client as srlcp
from time import sleep as delay
import signal
import sys
import numpy
from time import perf_counter as millis
from secrets import MQTT_SERVER, MQTT_PORT, MQTT_USE_AUTH, MQTT_USERNAME, MQTT_PASSWORD, LIGHT_ADDRESS

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

leds = srlcp(mqtt_server=MQTT_SERVER, mqtt_port=MQTT_PORT, light_address=LIGHT_ADDRESS,
            mqtt_use_auth=MQTT_USE_AUTH, mqtt_username=MQTT_USERNAME, mqtt_password=MQTT_PASSWORD)

leds.enter_programming_mode()

NUM_LEDS = leds.num_leds

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
    delay(0.1)
    