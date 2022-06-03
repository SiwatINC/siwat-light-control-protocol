from time import sleep
from siwat_remote_light_control_protocol_client.siwat_remote_light_control_protocol_client import siwat_remote_light_control_protocol_client as srlcp
from secrets import MQTT_SERVER, MQTT_PORT, MQTT_USE_AUTH, MQTT_USERNAME, MQTT_PASSWORD, LIGHT_ADDRESS

led = srlcp(mqtt_server=MQTT_SERVER, mqtt_port=MQTT_PORT, light_address=LIGHT_ADDRESS,
            mqtt_use_auth=MQTT_USE_AUTH, mqtt_username=MQTT_USERNAME, mqtt_password=MQTT_PASSWORD)

led.enter_programming_mode()

def rgb():
    for i in range(led.num_leds):
        if i<20:
            led.set_led_at(i,255,0,0)
        elif i<40:
            led.set_led_at(i,0,255,0)
        else:
            led.set_led_at(i,0,0,255)
    led.show()
def gbr():
    for i in range(led.num_leds):
        if i<20:
            led.set_led_at(i,0,255,0)
        elif i<40:
            led.set_led_at(i,0,0,255)
        else:
            led.set_led_at(i,255,0,0)
    led.show()
def brg():
    for i in range(led.num_leds):
        if i<20:
            led.set_led_at(i,0,0,255)
        elif i<40:
            led.set_led_at(i,255,0,0)
        else:
            led.set_led_at(i,0,255,0)
    led.show()
while True:
    rgb()
    sleep(0.1)
    gbr()
    sleep(0.1)
    brg()
    sleep(0.1)