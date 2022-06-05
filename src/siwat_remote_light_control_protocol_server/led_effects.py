from multiprocessing.dummy import active_children
import threading
from time import sleep
from siwat_light_control_protocol.siwat_light_control_protocol_multi_serial import siwat_light_control_protocol_multi_serial
import colorsys


class effect:

    active: bool = True

    def __init__(self, frame_time: float, led: siwat_light_control_protocol_multi_serial, brightness: float, **kwargs):
      "Will run at Initialization, do not override"
      self.led = led
      self.num_leds = sum(led.led_map)
      self.frame_time = frame_time
      self.brightness = brightness
      self.updater_thread = threading.Thread(target=self.frame_updater)
      self.updater_thread.start()
      self.initialize(**kwargs)

    def initialize(self, **kwargs):
      "Initialize Function, override if neccessary"
      pass

    def frame_updater(self):
      while True:
          if not self.active:
              break
          self.draw_frame()
          sleep(self.frame_time)

    def draw_frame(self):
      "This function update the led"
      "Will be called every frame_time"
      pass

    def stop_effect(self):
      "Stop the Effect"
      self.active = False
      while(self.updater_thread.is_alive()):
        sleep(0.1)


class rainbow(effect):

  def initialize(self, **kwargs):
    if 'velocity' in kwargs:
      self.velocity: float = kwargs['velocity']
    else:
      self.velocity = 10
    if 'segment_size' in kwargs:
      self.segment_size: int = kwargs['segment_size']
    else:
      self.segment_size = 1
    self.timecounter = 0
    
  def draw_frame(self):
    print(self.timecounter)
    for j in range(0, self.num_leds):
        r, g, b = colorsys.hsv_to_rgb(
            ((-self.timecounter*self.velocity+j*4) % 360)/360, 1, 1)
        self.led.set_led_at(j, r=int(r*self.brightness), g=int(g*self.brightness), b=int(b*self.brightness))
    self.timecounter += 1
    self.led.show()

class random(effect):
  # Put a new random color on every LEDs
  def initialize(self, **kwargs):
    # TODO Implement This Function
    pass
  def draw_frame(self):
    # TODO Implement This Function
    pass

class breathing(effect):
  # Slowly fade in and out with random color repeatedly
  def initialize(self, **kwargs):
    # TODO Implement This Function
    pass
  def draw_frame(self):
    # TODO Implement This Function
    pass

class police(effect):
  # Strobe Red and Blue
  def initialize(self, **kwargs):
    # TODO Implement This Function
    pass
  def draw_frame(self):
    # TODO Implement This Function
    pass

class starlight(effect):
  #Pop up a random color at random position then fade away
  def initialize(self, **kwargs):
    # TODO Implement This Function
    pass
  def draw_frame(self):
    # TODO Implement This Function
    pass


effects = [
  {
    "name": "None",
    "class": None
  },
  {
    "name": "Program",
    "class": None
  },
  {
    "name": "Rainbow",
    "class": rainbow
  },
  {
    "name": "Random",
    "class": random
  },
  {
    "name": "Breathing",
    "class": breathing
  },
  {
    "name": "Police",
    "class": police
  },
  {
    "name": "Starlight",
    "class": starlight
  }]