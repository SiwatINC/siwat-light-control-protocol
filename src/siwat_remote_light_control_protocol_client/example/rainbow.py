from siwat_remote_light_control_protocol_client.siwat_remote_light_control_protocol_client import siwat_remote_light_control_protocol_client as srlcp
from time import sleep as delay
import signal
import sys
import colorsys
from time import perf_counter as millis
def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
from secrets import MQTT_SERVER, MQTT_PORT, MQTT_USE_AUTH, MQTT_USERNAME, MQTT_PASSWORD, LIGHT_ADDRESS

leds = srlcp(mqtt_server=MQTT_SERVER, mqtt_port=MQTT_PORT, light_address=LIGHT_ADDRESS,
            mqtt_use_auth=MQTT_USE_AUTH, mqtt_username=MQTT_USERNAME, mqtt_password=MQTT_PASSWORD)

leds.enter_programming_mode()

leds.turn_off()
SEGMENT_SIZE = 1
VELOCITY = 10
NUM_LEDS = leds.num_leds
color = []
k = 0
timecounter = 0
while(True):
    for j in range(0,NUM_LEDS):
        r, g, b = colorsys.hsv_to_rgb(((-timecounter*VELOCITY+j*4)%360)/360,1,1)
        leds.set_led_at(j,r=int(r*255),g=int(g*255),b=int(b*255))
    timecounter+=1
    delay(0.1)
    leds.show()
