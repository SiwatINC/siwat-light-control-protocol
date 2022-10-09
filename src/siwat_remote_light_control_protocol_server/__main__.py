import sys
import os
from time import sleep
from siwat_light_control_protocol.input_validation import validate_rgb
from siwat_light_control_protocol.siwat_light_control_protocol_multi_serial import siwat_light_control_protocol_multi_serial as slcp
import siwat_light_control_protocol.led_effects as led_effects
import threading
import json
import paho.mqtt.client as mqtt
from serial.serialutil import SerialException

# Load Configuration
config = json.load(open("config.json"))
MQTT_SERVER: str = config['MQTT_SERVER']
MQTT_USE_AUTH: bool = config['MQTT_USE_AUTH']
MQTT_USERNAME: str = config['MQTT_USERNAME']
MQTT_PASSWORD: str = config['MQTT_PASSWORD']
MQTT_BASE_TOPIC: str = config['MQTT_BASE_TOPIC']
SERIAL_PORTS_MAP: list = config['SERIAL_PORTS_MAP']
LED_MAP: list = config['LED_MAP']
FRAME_TIME: float = config['FRAME_TIME']

global state, r, g, b, brightness, effect, effector, led, effects_list

# Setup LED Object
led = slcp(SERIAL_PORTS_MAP, LED_MAP)

# Variables Declaration
state = False
r = 255
g = 255
b = 255
brightness = 255
effect = 0
effector: led_effects.effect = None

# Consatant Declaration and Calculation
num_leds = sum(led.led_map)
effects_list = []
for eff in led_effects.effects:
    effects_list.append(eff['name'])

# Setup MQTT
mqttclient = mqtt.Client()
if MQTT_USE_AUTH:
    mqttclient.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)


def keep_alive():
    while True:
        if not mqttclient.is_connected():
            print("connecting to mqtt. . .")
            mqttclient.connect(MQTT_SERVER,
                               1883, 60)
            sleep(3)
            if(mqttclient.is_connected()):
                print("mqtt reconnected!")
                print("resubscribing to topics")
                mqttclient.subscribe(MQTT_BASE_TOPIC+"/control/#")
        if not led.is_connected():
            sys.exit(16)
        sleep(15)

for i in range(5):
    if mqttclient.is_connected():
        break
    print("connecting to mqtt. . .")
    mqttclient.connect(MQTT_SERVER,1883, 60)
    mqttclient.loop()
    sleep(5)
if not mqttclient.is_connected():
    print("Could not connect tro MQTT server!, Exiting . . .")
    sys.exit(23)
print("mqtt connected!")

print("subscribing to topics")
mqttclient.subscribe(MQTT_BASE_TOPIC+"/control/#")

print("keeping connection alive!")

threading.Thread(target=keep_alive).start()

def report_state():
    global state, r, g, b, brightness, effect, effector, led, effects_list
    mqttclient.publish(MQTT_BASE_TOPIC+"/report/state",
                       "on" if state else "off")
    mqttclient.publish(MQTT_BASE_TOPIC+"/report/color", str(int(r))+","+str(int(g))+","+str(int(b)))
    mqttclient.publish(MQTT_BASE_TOPIC+"/report/effect",
                       led_effects.effects[effect]['name'])
    mqttclient.publish(MQTT_BASE_TOPIC+"/report/effectlist", json.dumps(effects_list))
    mqttclient.publish(MQTT_BASE_TOPIC+"/report/brightness", int(brightness))
    mqttclient.publish(MQTT_BASE_TOPIC+"/report/num_leds", num_leds)


def handle_mqtt_messages(client, userdata, msg: mqtt.MQTTMessage):
    try:
        global state, r, g, b, brightness, effect, effector, led, effects_list
        topic = msg.topic
        payload = msg.payload.decode("UTF-8")
        if topic == MQTT_BASE_TOPIC+"/control/state":
            if payload == "off":
                if effector != None:
                    effector.stop_effect()
                    effect = 0
                    effector = None
                    mqttclient.publish(MQTT_BASE_TOPIC+"/report/effect",
                    led_effects.effects[effect]['name'])
                led.turn_off()
                state = 0
            elif payload == "on" and effect != 1:
                if state != 1:
                    state = 1
                    if effect == 0:
                        led.fill_led_with_color(
                            r*brightness/255.0, g*brightness/255.0, b*brightness/255.0)
                    elif effect >= 2:
                        effector = led_effects.effects[effect]['class'](
                            frame_time=FRAME_TIME, led=led, brightness=brightness, r=r, g=g, b=b)
            mqttclient.publish(MQTT_BASE_TOPIC+"/report/state",
                        "on" if state else "off")
        elif topic == MQTT_BASE_TOPIC+"/control/brightness":
            if effect != 1:
                try:
                    brightness = float(payload)
                    if brightness > 255 or brightness<0: 
                        return
                    if effect == 0:
                        led.fill_led_with_color(
                            r*brightness/255.0, g*brightness/255.0, b*brightness/255.0)
                    elif effect != 1 and effector != None:
                        effector.brightness = brightness
                except ValueError:
                    return
            mqttclient.publish(MQTT_BASE_TOPIC+"/report/brightness", int(brightness))
        elif topic == MQTT_BASE_TOPIC+"/control/color":
            if effect != 1:
                try:
                    [rtmp,gtmp,btmp] = payload.split(',')
                    [r,g,b] = validate_rgb(int(float(rtmp)),int(float(gtmp)),int(float(btmp)))
                    if effect >= 2:
                        effector.r = r
                        effector.g = g
                        effector.b = b
                    if r<0 or r>255 or g<0 or g>255 or b<0 or b>255:
                        return
                    if effect == 0:
                        led.fill_led_with_color(
                            r*brightness/255.0, g*brightness/255.0, b*brightness/255.0)
                except ValueError:
                    print("Invalid Payload")
                    return
            mqttclient.publish(MQTT_BASE_TOPIC+"/report/color", str(int(r))+","+str(int(g))+","+str(int(b)))
        elif topic == MQTT_BASE_TOPIC+"/control/effect":
            if effector != None:
                effector.stop_effect()
                effector = None
            for i in range(len(led_effects.effects)):
                if led_effects.effects[i]['name'] == payload:
                    effect = i
                    if effect == 0:
                        led.fill_led_with_color(
                            r*brightness/255.0, g*brightness/255.0, b*brightness/255.0)
                    elif effect == 1:
                        led.turn_off()
                    elif effect >= 2 and state:
                        effector = led_effects.effects[i]['class'](
                            frame_time=FRAME_TIME, led=led, brightness=brightness, r=r, g=g, b=b)
            mqttclient.publish(MQTT_BASE_TOPIC+"/report/effect",
                        led_effects.effects[effect]['name'])
        elif topic == MQTT_BASE_TOPIC+"/control/exit":
            sys.exit(0)
        elif topic == MQTT_BASE_TOPIC+"/control/program":
            if effect == 1:
                datas = json.loads(payload)
                for data in datas:
                    led.set_led_at(data[0],data[1][0],data[1][1],data[1][2])
                led.show()
        elif topic == MQTT_BASE_TOPIC+"/control/requeststate":
            report_state()
    except SerialException:
        print("Serial Disconnected, Exiting. . .")
        mqttclient.disconnect()
        if os.name == 'posix':
            os.kill(os.getpid(), signal.SIGINT)
        else:
            os._exit()
mqttclient.on_message = handle_mqtt_messages

report_state()

print("Initialization Completed!")

mqttclient.loop_forever()
