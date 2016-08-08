import logging
import time
import Queue
import threading
import sys
from Tkinter import *
from pystates import StateMachine
if sys.platform=='linux2':
  from neopixel import *
import math
import random
from MockStrip import MockStrip







class Layer:
  """Manages a layer of the lights."""
  def __init__(self, None_func, curr_func, opacity, trans_time):
    self.trans_time = float(trans_time)
    self.opacity = opacity
    self.time_0 = None
    self.curr_func = curr_func
    self.set_next(self.curr_func)
    self.None_func = None_func
    self.func_opacities = (1,1)

  def get_data(self, j):
    """Returns the data of the layer at iteration j."""
    if (self.curr_func or self.next_func):
      if self.curr_func == self.next_func:
        _data_out = self.curr_func(j)
      else:
        _data_out = self.mix(self.curr_func(j), self.next_func(j), self.fade_weights(self.trans_time))
        if not self.time_0:
          self.curr_func = self.next_func
      return _data_out

  def fade_weights(self, duration): #! if there are multiple fades active/ this is called when another fade is in progress, it will use its time. self.time_0 conflict
    """Returns a tuple of two multipliers; used to weight color values."""
    if not self.time_0: #if fade not active
      self.time_0 = time.time()
    self.duration = time.time() - self.time_0
    if self.duration >= duration: #if fade complete
      self.time_0 = None
      temp = (0,1)
      self.func_opacities = temp
      return temp
    else:
      temp = (1. - self.duration/duration, self.duration/duration)
      self.func_opacities = temp
      return temp

  def mix(self, data1, data2, multipliers=(.50,.50)):
    """Displays multiple functions at once, weighted with the multipliers (m1, m2).
    If a color value is (0,0,0) it will mix the other color; if it is 'None' it will simply yield the other color.
    Both being 'None' yields 'None'."""
    _data = []
    for i in range(len(data1)): #! if data1 and data2 are not the same length, this could be problematic (they should always be the same though).
      color = []
      if not (data1[i] or data2[i]):
        color = None
      else:
        if not data1[i]: data1[i] = (0,0,0)
        if not data2[i]: data2[i] = (0,0,0)
        for v in range(3):
          color.append(multipliers[0]*data1[i][v] + multipliers[1]*data2[i][v])
          if color[-1] > 255:
            color[-1] = 255
      if color: color = tuple(color)
      _data.append(color)
    return _data

  def set_next(self, next_func):
    """Sets the next function to be displayed."""
    self.next_func = next_func

  def get_next(self):
    """Returns the next function of the layer."""
    return self.next_func

  def set_opacity(self, opacity):
    """Sets the opacity of the layer, where 0 is clear and 1 is opaque."""
    self.opacity = opacity

  def get_opacity(self):
    """Returns the current opacity of the layer."""
    if self.curr_func == self.next_func == self.None_func:
      curr = 0
    elif self.curr_func == self.next_func:
      curr = 1
    elif self.curr_func == self.None_func:
      curr = self.func_opacities[1]
    else:
      curr = self.func_opacities[0]
    return curr*self.opacity

  def clear(self):
    """Resets the layer to the 'None' function. (filled with 'None')"""
    self.next_func = self.None_func










    
 
class QuickChange:
  def __init__(self, handle_pixel=20, trans_time=1.5):
    self.time_0 = None
    self.wait_ms = 50
    self.handle_pixel = handle_pixel
    self.trans_time = float(trans_time)

  def main(self):
    self.Layer_0 = Layer(self.set_color_None, self.rainbow_cycle, 1, self.trans_time)
    self.Layer_1 = Layer(self.set_color_None, self.set_color_None, .5, self.trans_time)
    j = 0 #iterator for all functions run by main
    while True:
      _data_out = self.stack_layers(j, self.Layer_0, self.Layer_1)
      self.update_strip(_data_out)
      time.sleep(self.wait_ms/1000.0)
      j += 1
      if j >= self.strip.numPixels()*18000:
        j=0

  def update_strip(self, data):
    """Updates the strip then shows the new strip."""
    for i in range(self.strip.numPixels()):
      if not (data or data[i]):
        self.strip.setPixelColor(i, self.Color(0,0,0))
      else:
        self.strip.setPixelColor(i, self.Color(*[int(round(n)) for n in data[i]]))
    self.strip.show()

  def stack_layers(self, j, *layers):
    """Displays multiple functions at once, weighted with the multipliers."""
    _data = self.mix(self.set_color_None(j), layers[0].get_data(j), (1 - layers[0].get_opacity(), layers[0].get_opacity()))
    for i in range(1, len(layers)):
      _data = self.mix(_data, layers[i].get_data(j), (1 - layers[i].get_opacity(), layers[i].get_opacity()))
      #print(1 - layers[i].get_opacity(), layers[i].get_opacity())
    return _data

  def mix(self, data1, data2, multipliers):
    """Displays multiple functions at once, weighted with the multipliers (m1, m2).
    If a color value is (0,0,0) it will mix the other color; if it is 'None' it will simply yield the other color.
    Both being 'None' yields 'None'."""
    _data = []
    for i in range(self.strip.numPixels()):
      color = []
      if not data1[i]:
        color = data2[i]
      elif not data2[i]:
        color = data1[i]
      else:
        for v in range(3):
          color.append(multipliers[0]*data1[i][v] + multipliers[1]*data2[i][v])
          if color[-1] > 255:
            color[-1] = 255
      if color: color = tuple(color)
      _data.append(color)
    return _data

  def set_strip(self, strip):
    """Sets the LED strip instance."""
    self.strip = strip

  def Color(self,red, green, blue):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (red << 16) | (green << 8) | blue

  def wheel(self, pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
      return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return (255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return (0, pos * 3, 255 - pos * 3)

#----------------------------------------------------------------------------------------------------
  def fade_to_green(self, j):
    """Fades to green."""
    return self.fade_to_color(j, (0,255,0))

  def fade_to_red(self, j):
    """Fades to red."""
    return self.fade_to_color(j, (255,0,0),fade_time=self.stuck_open_timeout)

  def color_wipe_to_handle_green(self, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe_to_handle(j, (0,255,0))

  def color_wipe_to_handle_white(self, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe_to_handle(j, (255,255,255))

  def theatre_chase_white(self, j):
    """Movie theatre light style chaser animation."""
    return self.theatre_chase(j, (255,255,255))

  def flash_colors_blue_red(self, j):
    """Cycle between two colors"""
    return self.flash_colors(j, (0,0,255), (255,0,0))

  def flash_colors_red_black(self, j):
    """Cycle between two colors"""
    return self.flash_colors(j, (255,0,0), (96,0,0))
 
  def color_wipe_red(self, j):
    """Wipe red across display a pixel at a time."""
    return self.color_wipe(j, (255, 0, 0))

  def color_wipe_green(self, j):
    """Wipe green across display a pixel at a time."""
    return self.color_wipe(j, (0, 255, 0))

  def color_wipe_blue(self, j):
    """Wipe blue across display a pixel at a time."""
    return self.color_wipe(j, (0, 0, 255))

  def set_color_red(self, j):
    """Sets the color of all pixels to red."""
    return self.set_color(j, (255, 0, 0))

  def set_color_green(self, j):
    """Sets the color of all pixels to green."""
    return self.set_color(j, (0,255,0))

  def set_color_black(self, j):
    """Sets the color of all pixels to black."""
    return self.set_color(j, (0,0,0))

  def set_color_None(self, j):
    """Sets the color of all pixels to 'None'."""
    return self.set_color(j, None)
#----------------------------------------------------------------------------------------------------
  def rainbow(self, j):
    """Draw rainbow that fades across all pixels at once."""
    _data = []
    for i in range(self.strip.numPixels()): #initialize pixel data
      _data.append(self.wheel((i+j) & 255))
    return _data

  def rainbow_cycle(self, j):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    _data = []
    for i in range(self.strip.numPixels()): #initialize pixel data
      _data.append(self.wheel((i * 256 / self.strip.numPixels()) + j & 255))
    return _data

  def color_wipe_to_handle(self, j, color, pointing=10): #Yet to be worked on. Completed simpler functions first.
    """Wipe color across display a pixel at a time."""
    handle = self.handle_pixel
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(None)
    _data[handle - (-j)%pointing] = color
    _data[handle + (-j)%pointing] = color
    return _data

  def flash_colors(self, j, color1, color2):
    """Cycle between two colors"""
    _data = []
    for i in range(self.strip.numPixels()):
      if i%2==0:
        if j%2==0:
          _data.append(color1)
        else:
          _data.append(color2)
      else:
        if j%2==0:
          _data.append(color2)
        else:
          _data.append(color1)
    return _data

  def theatre_chase(self, j, color1, color2=None):
    """Movie theatre light style chaser animation."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(color2)
    for i in range(self.strip.numPixels()-1):
      if i%3==0:
        _data[i+j%3] = color1
    return _data

  def color_wipe(self, j, color):
    """Wipe color across display a pixel at a time."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(None)
    _data[j%self.strip.numPixels()] = color
    return _data

  '''def fade_to_color(self, j, color, rate=(5,5,5), fade_time=None):
    """Fades to color."""
    _data = []
    #print("--------------------------------------------------")
    if fade_time:
      tot_frames = float((fade_time)/(self.wait_ms/1000.0)) #float((fade_time)/(frame_time + self.wait_ms/1000.0))
      rate = (255/tot_frames,255/tot_frames,255/tot_frames)
    for i in range(self.strip.numPixels()):
      newcolor = []
      curr_color = data[i]
      print("{i}: {cc}".format(i=i, cc=curr_color))
      for c in range(3):
        tempcolor = None
        if curr_color[c] < color[c] and curr_color[c] + rate[c] > color[c]:
          #print("cc < c && cc + r > c")
          pass
        elif curr_color[c] > color[c] and curr_color[c] - rate[c] < color[c]:
          #print("cc > c && cc - r < c")
          pass
        if curr_color[c] == color[c] \
        or (curr_color[c] < color[c] and curr_color[c] + rate[c] > color[c]) \
        or (curr_color[c] > color[c] and curr_color[c] - rate[c] < color[c]): # Is this actually more helpful than if statements in if statements?
          tempcolor = color[c]
        elif curr_color[c] < color[c]:
          tempcolor = curr_color[c] + rate[c]
        else:
          tempcolor = curr_color[c] - rate[c]
        newcolor.append(tempcolor)
      _data[i] = newcolor
      print("{i}: {nc}".format(i=i, nc=(newcolor)))
    return _data'''.format(i=1,cc=1,nc=1)

  def set_color(self, j, color):
    """Sets the color of all pixels."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append(color)
    return _data

class BlinkenLights(StateMachine):

  def MAIN_DOOR_UNLOCKING(self):
    self.set_gui_state("MAIN_DOOR_UNLOCKING")
    self.qc.Layer_1.set_next(self.qc.color_wipe_to_handle_white)

  def INVALID_KEY(self):
    self.set_gui_state("INVALID_KEY")
    #self.qc.Layer_1.set_next(self.qc.flash_colors_red_black)
    time.sleep(1.5)
    self.set_state(self.prev_state)

  def MAIN_DOOR_FORCED_OPEN(self):
    self.set_gui_state("MAIN_DOOR_FORCED_OPEN")
    self.qc.Layer_0.set_next(self.qc.flash_colors_blue_red)

  def MAIN_DOOR_OPENED(self):
    self.set_gui_state("DOOR_OPENED")
    self.qc.Layer_0.set_next(self.qc.rainbow)
    self.qc.Layer_1.clear()

  def MAIN_DOOR_STUCK_OPEN(self):
    self.set_gui_state("MAIN_DOOR_STUCK_OPEN")
    self.qc.Layer_0.set_next(self.qc.flash_colors_red_black)

  def MAIN_DOOR_CLOSED(self):
    self.set_gui_state("MAIN_DOOR_CLOSED")
    self.qc.Layer_0.set_next(self.qc.rainbow_cycle)
    self.qc.Layer_1.clear()

  def IDLE(self):
    self.set_gui_state("IDLE")
    while True:
      ev = yield
      if ev['event'] ==    "MAIN_DOOR_CLOSED":
        self.set_state(self.MAIN_DOOR_CLOSED)
      if ev['event'] ==    "MAIN_DOOR_UNLOCKING":
        self.set_state(self.MAIN_DOOR_UNLOCKING)
      if ev['event'] ==    "MAIN_DOOR_OPENED":
        self.set_state(self.MAIN_DOOR_OPENED)
      if ev['event'] ==    "MAIN_DOOR_FORCED_OPEN":
        self.set_state(self.MAIN_DOOR_FORCED_OPEN)
      if ev['event'] ==    "INVALID_KEY":
        self.set_state(self.INVALID_KEY)
      if ev['event'] ==    "MAIN_DOOR_STUCK_OPEN":
        self.set_state(self.MAIN_DOOR_STUCK_OPEN)
      self.do_func()

  def set_gui_state(self, state):
    if self.gui:
      self.gui_state.set(state)

  def do_func(self):
    if self.curr_state != self.state:
      self.prev_state = self.state
      self.state = self.curr_state
      self.curr_state()

  def get_state(self):
    return self.state

  def set_state(self, state):
    self.curr_state = state

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel, stuck_open_timeout, trans_time):
    self.log = logging.getLogger("BlinkenLights")
    self.out_queue = out_queue
    self.name = name
    # the pixel closest to the handle
    self.handle_pixel = int(handle_pixel)
    self.led_count=int(led_count)       # Number of LED pixels.
    self.led_pin = int(led_pin)         # GPIO pin connected to the pixels (must support PWM!).
    self.led_freq_hz = int(led_freq_hz) # LED signal frequency in hertz (usually 800khz)
    self.led_dma = int(led_dma)         # DMA channel to use for generating signal (try 5)
    self.led_brightness = int(led_brightness) # Set to 0 for darkest and 255 for brightest
    self.led_invert = led_invert.lower() in ("yes", "true", "t", "1")  # True to invert the signal (when using NPN transistor level shift)
    self.stuck_open_timeout = int(stuck_open_timeout)
    self.trans_time = float(trans_time)
    self.gui = False
    self.state = None
    self.prev_state = None
    self.curr_state = None
    # Create NeoPixel object with appropriate configuration.
    if sys.platform=='linux2':
      self.strip = Adafruit_NeoPixel(self.led_count, self.led_pin, self.led_freq_hz, self.led_dma, self.led_invert, self.led_brightness)
    #self.strip = Adafruit_NeoPixel(self.led_count, 18, 800000, 5, False, 255)

  def config_gui(self, root):
    # Set up the GUI part
    self.gui = True
    frame = LabelFrame(root, text="STATE", padx=5, pady=5)
    frame.pack(fill=X)
    self.gui_state = StringVar()
    self.gui_state.set("[STATE]")
    label = Label(frame, textvariable = self.gui_state, justify=LEFT)
    label.pack(side=LEFT)
    self.info_frame = frame
    frame2 = LabelFrame(root, text=self.name, padx=5, pady=5, bg='black')
    frame2.pack(fill=X)
    self.wait_ms = 50
    self.strip = MockStrip(self.led_count, frame2)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # Intialize the library (must be called once before other functions).
    self.strip.begin()
    self.log.debug("start called")
    self.qc = QuickChange(self.handle_pixel, self.trans_time)
    self.qc.set_strip(self.strip)
    self.qc.stuck_open_timeout = self.stuck_open_timeout
    self.thread = threading.Thread(target=self.qc.main)
    self.thread.setDaemon(True)
    self.thread.start()
    self.log.debug("thread started")
    super(BlinkenLights, self).start(self.IDLE)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "BLINKENLIGHTS"
  machine = BlinkenLights(name=name)
  machine.setup(out_queue, name=name, led_count=16, led_pin=18, led_freq_hz=800000, led_dma=5, led_invert="False", led_brightness=255, handle_pixel = 8, stuck_open_timeout = 15)
  machine.start()
  machine.send_message({"event": "MAIN_DOOR_UNLOCKING"})

  time.sleep(15)

if __name__=='__main__':
  main()
