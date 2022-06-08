import json
from re import S
from time import sleep
import paho.mqtt.client as mqtt
import threading
from siwat_light_control_protocol.input_validation import LEDOutOfBoundError, validate_rgb, index_is_valid, range_is_valid

class siwat_remote_light_control_protocol_client:
    mqttclient: mqtt.Client = mqtt.Client()
    current_color: list = []
    new_color: list
    num_leds: int = None

    def __init__(self, mqtt_server: str, mqtt_port: str, light_address: str, mqtt_use_auth: bool = False, mqtt_username: str = None, mqtt_password: str = None):
        # Setup MQTT
        self.mqttclient = mqtt.Client()
        if mqtt_use_auth:
            self.mqttclient.username_pw_set(
                username=mqtt_username, password=mqtt_password)
        while True:
            if not self.mqttclient.is_connected():
                print("connecting to mqtt. . .")
                self.mqttclient.connect(mqtt_server,
                                        mqtt_port, 60)
                self.mqttclient.loop()
                sleep(5)
                if self.mqttclient.is_connected():
                    print("mqtt connected!")
            else:
                break
        self.light_address = light_address
        self.mqttclient.loop_start()
        self.mqttclient.subscribe(light_address+"/#")
        self.mqttclient.on_message = self.handle_mqtt_messages
        self.send_command("requeststate", "none")
        sleep(1)
        self.turn_off()
        sleep(1)
        if self.num_leds == None:
            raise ConnectionTimeoutException

    def handle_mqtt_messages(self, client, userdata, msg: mqtt.MQTTMessage):
        topic = msg.topic
        payload = msg.payload.decode("UTF-8")
        if topic == self.light_address+"/report/num_leds":
            self.num_leds = int(payload)

    def send_command(self, command: str, data: str):
        self.mqttclient.publish(self.light_address+"/control/"+command, data)

    def enter_programming_mode(self):
        self.send_command("state", "on")
        self.send_command("effect", "Program")
        self.turn_off()

    def turn_off(self):
        self.fill_with_color(0, 0, 0)
        command_array = []
        for i in range(self.num_leds):
            command_array.append([i, self.new_color[i]])
        self.send_command("program", json.dumps(command_array))
        self.current_color = self.new_color.copy()

    def show(self):
        command_array: list = []
        for i in range(self.num_leds):
            if self.current_color[i] != self.new_color[i]:
                self.current_color[i] = self.new_color[i]
                command_array.append([i, self.new_color[i]])
        self.send_command("program", json.dumps(command_array))

    def set_led_at(self, index: int, r: int, g: int, b: int):
        [r,g,b] = validate_rgb(r,g,b)
        if not index_is_valid(index,self.num_leds):
            raise LEDOutOfBoundError
        self.new_color[index] = [r, g, b]

    def fill_with_color(self, r: int, g: int, b: int):
        [r,g,b] = validate_rgb(r,g,b)
        new_color = []
        for i in range(self.num_leds):
            new_color.append([r, g, b])
        self.new_color = new_color

    def fill_segment_with_color(self, segment_start: int, segment_stop: int, r: int, g: int, b: int):
        [r,g,b] = validate_rgb(r,g,b)
        if not range_is_valid(segment_start,segment_stop,self.num_leds):
            return

        for index in range(segment_start, segment_stop+1):
            self.set_led_at(index, r, g, b)


class ConnectionTimeoutException(Exception):
    """The LED server does not response to requests!"""
    pass
