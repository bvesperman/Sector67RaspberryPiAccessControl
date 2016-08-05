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

 
class QuickChange:
  def __init__(self, handle_pixel=20, trans_time=1.5):
    self.time_0 = None
    self.wait_ms = 50
    self.sur_func = None
    self.curr_func = self.color_wipe_blue
    self.set_next(self.color_wipe_blue)
    self.handle_pixel = handle_pixel
    self.trans_time = float(trans_time)

  def update_strip(self, data):
    """Updates the strip then shows the new strip."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, self.Color(*[int(round(n)) for n in data[i]]))
    self.strip.show()

  def main(self):
    j = 0 #iterator for all functions run by main
    while True:
      if self.curr_func == self.next_func:
        _data_out = self.curr_func(j)
      else:
        _data_out = self.mix(j, self.curr_func(j), self.next_func(j), self.fade_multipliers(self.trans_time))
        if not self.time_0:
          self.curr_func = self.next_func
      if self.sur_func:
        _data_out = self.mix(j, _data_out, self.sur_func.func(j), (1,self.sur_func.get_multiplier()))
        print(_data_out)
        if self.sur_func.is_finished():
          self.sur_func = None
      self.update_strip(_data_out)
      time.sleep(self.wait_ms/1000.0)
      j += 1
      if j >= self.strip.numPixels()*18000:
        j=0

  def fade_multipliers(self, duration): #! if there are multiple fades active/ this is called when another fade is in progress, it will use its time. self.time_0  and self.fade_running conflict
    """Returns a tuple of two multipliers; used to weight color values."""
    if not self.time_0: #if fade not active
      self.time_0 = time.time()
    self.duration = time.time() - self.time_0
    if self.duration >= duration: #if fade complete
      self.time_0 = None
      return (0,1)
    else:
      return (1. - self.duration/duration, self.duration/duration)

  def mix(self, j, data1, data2, multipliers=(1,.5)):
    """Displays multiple functions at once, weighted with the multipliers."""
    _data = []
    for i in range(self.strip.numPixels()):
      color = []
      for v in range(3):
        color.append(multipliers[0]*data1[i][v] + multipliers[1]*data2[i][v])
        if color[-1] > 255:
          color[-1] = 255
      _data.append(color)
    return _data

  def set_overlay(self,func):
    self.sur_func = func

  def get_overlay(self): #!WIP/unfinished
    return self.sur_func

  def clear_overlay(self): #WIP/unfinished
    self.sur_func = None

  def set_next(self, next_func):
    """Sets the next function to be displayed."""
    self.next_func = next_func
    #print(next_func)

  def set_strip(self, strip):
    """Sets the LED strip instance."""
    self.strip = strip

  def ColorRGB(self, color):
    """Returns color as a truple of integers (R,G,B)."""
    return (int(bin(color)[2:].zfill(24)[:-16],2), int(bin(color)[2:].zfill(24)[-16:-8],2), int(bin(color)[2:].zfill(24)[-8:],2))

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
    """Wipe color across display a pixel at a time."""
    return self.color_wipe(j, (255, 0, 0))

  def color_wipe_green(self, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe(j, (0, 255, 0))

  def color_wipe_blue(self, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe(j, (0, 0, 255))

  def set_color_red(self, j):
    return self.set_color(j, (255, 0, 0))

  def set_color_green(self, j):
    """Sets the color of all pixels."""
    return self.set_color(j, (0,255,0))

  def rainbow(self, j):
    """Draw rainbow that fades across all pixels at once."""
    _data = []
    for i in range(self.strip.numPixels()): #initialize pixel data
      _data.append(self.wheel((i+j) & 255))

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
      _data.append((0,0,0))
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

  def theatre_chase(self, j, color1, color2=(0,0,0)):
    """Movie theatre light style chaser animation."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append((0,0,0))
    for i in range(self.strip.numPixels()):
      if i%3==0:
        _data[i+j%3] = color1
        _data[i+(j - 1)%3] = color2
    return _data

  def color_wipe(self, j, color):
    """Wipe color across display a pixel at a time."""
    _data = []
    for i in range(self.strip.numPixels()):
      _data.append((0,0,0))
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
    self.qc.set_next(self.qc.color_wipe_to_handle_green)

  def INVALID_KEY(self):
    self.set_gui_state("INVALID_KEY")
    self.qc.set_next(self.qc.flash_colors_red_black)
    time.sleep(2)
    self.set_state(self.prev_state)

  def MAIN_DOOR_FORCED_OPEN(self):
    self.set_gui_state("MAIN_DOOR_FORCED_OPEN")
    self.qc.set_next(self.qc.flash_colors_blue_red)

  def MAIN_DOOR_OPENED(self):
    self.set_gui_state("DOOR_OPENED")
    self.qc.set_next(self.qc.color_wipe_blue)

  def MAIN_DOOR_STUCK_OPEN(self):
    self.set_gui_state("MAIN_DOOR_STUCK_OPEN")
    self.qc.set_next(self.qc.flash_colors_red_black)

  def MAIN_DOOR_CLOSED(self):
    self.set_gui_state("MAIN_DOOR_CLOSED")
    self.qc.set_next(self.qc.rainbow_cycle)

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


class MockStrip:
  def __init__(self, led_count, frame):
    self.led_count = led_count
    self.rand = random.Random()
    self.pending = []
    self.labels = []

    for i in range(led_count):
      self.pending.append("#000000")

    for i in range(led_count):
      lbl = Label(frame, text=str(i), width = 2)
      self.labels.append(lbl)
      lbl.pack(side=LEFT, expand = True, fill = X)
      lbl.configure(bg="#000000")

    self.show() 

  def show(self):
    i=0
    for label in self.labels:
      #print "i is " + str(i)
      #print "color is " + self.pending[i]
      label.configure(bg=self.pending[i])
      i=i+1

  def begin(self):# mimicing neopixel;
    pass

  def setPixelColor(self, pixel, color):
    self.pending[pixel]=self.tk_color(color)

  def getPixelColor(self, pixel):
    return self.pending[pixel]

  def getPixelColorRGB(self, pixel):
    n = self.pending[pixel][1:]
    n = int(n, base=16)
    c = lambda: None
    setattr(c, 'r', n >> 16 & 0xff)
    setattr(c, 'g', n >> 8  & 0xff) 
    setattr(c, 'b', n & 0xff)
    return c

  def tk_color(self,color):
    red=(color & 0xff0000) >> 16
    green=(color & 0x00ff00) >> 8
    blue=(color & 0x0000ff)
    newcolor='#%02X%02X%02X' % (red,green,blue)
    return newcolor

  def numPixels(self):
    return self.led_count

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
