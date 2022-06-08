from multiprocessing.dummy import active_children
import threading
from time import sleep
from siwat_light_control_protocol.siwat_light_control_protocol_multi_serial import siwat_light_control_protocol_multi_serial
from time import perf_counter as ticks
import colorsys
import numpy

class effect:

    active: bool = True

    def __init__(self, frame_time: float, led: siwat_light_control_protocol_multi_serial, brightness: float,
                    r: float, g: float, b: float, **kwargs):
      "Will run at Initialization, do not override"
      self.led = led
      self.num_leds = sum(led.led_map)
      self.frame_time = frame_time
      self.brightness = brightness
      self.initialize(**kwargs)
      self.r = r
      self.g = g
      self.b = b

      self.updater_thread = threading.Thread(target=self.frame_updater)
      self.updater_thread.start()

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

  def draw_frame(self):
    for j in range(0, self.num_leds):
        r, g, b = colorsys.hsv_to_rgb(
            ((-ticks()*10*self.velocity+j*4) % 360)/360, 1, 1)
        self.led.set_led_at(j, r=int(r*self.brightness), g=int(g*self.brightness), b=int(b*self.brightness))
    self.led.show()

class random(effect):
  # Put a new random color on every LEDs
  def initialize(self, **kwargs):
    self.color = [[255,0,0],[255,127,0],[255,255,0],
        [127,255,0],[0,255,0],[0,255,127],
        [0,255,255],[0,127,255],[0,0,255],
        [127,0,255],[255,0,255],[255,0,127]]
    self.array = numpy.random.randint(low=0,high=9,size=self.num_leds)
    self.frame_time = 0.2
    
  def draw_frame(self):
    self.array = numpy.random.randint(low=0,high=9,size=self.num_leds)
    for i in range(0,self.num_leds):
        self.led.set_led_at(i,r=int(self.brightness*self.color[self.array[i]][0]/255.0),g=int(self.brightness*self.color[self.array[i]][1]/255.0),b=int(self.brightness*self.color[self.array[i]][2]/255.0))
    self.led.show()
    

class breathing_random(effect):
  # Slowly fade in and out with random color repeatedly
  def initialize(self, **kwargs):
    self.color = [[255,0,0],[255,127,0],[255,255,0],
        [127,255,0],[0,255,0],[0,255,127],
        [0,255,255],[0,127,255],[0,0,255],
        [127,0,255],[255,0,255],[255,0,127]]
    self.array = numpy.random.randint(low=0,high=9,size=self.num_leds)
    self.init_tick = ticks()
  def draw_frame(self):
    time = ticks()-self.init_tick
    self.array = numpy.random.randint(low=0,high=9,size=self.num_leds)
    val = numpy.sin(time)
    val = numpy.heaviside(val,1)*val
    for i in range(0,self.num_leds):
      self.led.set_led_at(i,r=int(self.brightness*self.color[self.array[i]][0]*val/255.0),g=int(self.brightness*self.color[self.array[i]][1]*val/255.0),b=int(self.brightness*self.color[self.array[i]][2]*val/255.0))
    self.led.show()

class breathing(effect):
      # Slowly fade in and out with current colour
  def initialize(self, **kwargs):
    self.init_tick = ticks()
  def draw_frame(self):
    time = ticks()-self.init_tick
    val = numpy.sin(time)
    val = numpy.heaviside(val,1)*val
    for i in range(0,self.num_leds):
      self.led.set_led_at(i,r=int(self.brightness*self.r*val/255.0),g=int(self.brightness*self.g*val/255.0),b=int(self.brightness*self.b*val/255.0))
    self.led.show()

class police(effect):
  # Strobe Red and Blue
  def initialize(self, **kwargs):
    self.init_tick = ticks()
  def draw_frame(self):
    time = ticks()-self.init_tick
    time *= 1000
    time = time%1000
    if(time<500):
      for i in range(0,self.num_leds):
        self.led.set_led_at(i,r=int(self.brightness*1),g=0,b=0)
    else:
      for i in range(0,self.num_leds):
        self.led.set_led_at(i,r=0,g=0,b=int(self.brightness*1))
    self.led.show()

class starlight(effect):
  #Pop up a random color at random position then fade away
  def initialize(self, **kwargs):
    # TODO Implement This Function
    self.color = [[255,0,0],[255,127,0],[255,255,0],
        [127,255,0],[0,255,0],[0,255,127],
        [0,255,255],[0,127,255],[0,0,255],
        [127,0,255],[255,0,255],[255,0,127]]
    self.array = numpy.random.randint(low=0,high=9,size=self.num_leds)
  def draw_frame(self):
    # TODO Implement This Function
    self.array = numpy.random.randint(low=0,high=9,size=self.num_leds)
    for i in range(0,self.num_leds):
        self.led.set_led_at(i,r=int(self.brightness*self.color[self.array[i]][0]),g=int(self.brightness*self.color[self.array[i]][1]),b=int(self.brightness*self.color[self.array[i]][2]))
    self.led.show()


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
    "name": "BreathingRandom",
    "class": breathing_random
  },
  {
    "name": "Police",
    "class": police
  },
  ]