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
  def __init__(self, handle_pixel=20):
    self.set_next(self.color_wipe_blue)
    self.curr_func = self.color_wipe_blue
    self.wait_ms = 50
    self.handle_pixel = handle_pixel

  def main(self):
    while True:
      self.next_func()
      self.curr_func = self.next_func

  def set_next(self, next_func):
    self.next_func = next_func
    #print(next_func)

  def set_strip(self, strip):
    self.strip = strip

  def ColorRGB(self, color):
    """returns color as a truple of integers (R,G,B)."""
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
      return self.Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return self.Color(255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return self.Color(0, pos * 3, 255 - pos * 3)

  def fade_to_color(self, color24, rate=(5,5,5), fade_time=None):
    color = self.ColorRGB(color24)
    _strip_data = {}
    if fade_time: rate = (.1,.1,.1)
    while True:
      time_0= time.time()
      for i in range(self.strip.numPixels()):

        newcolor = []
        if i not in _strip_data:
          _strip_data[i] = (self.strip.getPixelColorRGB(i).r,self.strip.getPixelColorRGB(i).g,self.strip.getPixelColorRGB(i).b)
        curr_color = _strip_data[i]
        for j in range(3):
          tempcolor = None
          if curr_color[j] == color[j]:
            tempcolor = color[j]
          elif curr_color[j] < color[j]:
            if curr_color[j] + rate[j] > color[j]:
              tempcolor = color[j]
            else:
              tempcolor = curr_color[j] + rate[j]
          else:
            if curr_color[j] - rate[j] < color[j]:
              tempcolor = color[j]
            else:
              tempcolor = curr_color[j] - rate[j]
          newcolor.append(tempcolor)
        self.strip.setPixelColor(i, self.Color(*[int(round(n)) for n in newcolor]))
        _strip_data[i] = newcolor
      self.strip.show()
      if fade_time:
        frame_time = time.time() - time_0
        tot_frames = float((fade_time)/(frame_time + self.wait_ms/1000.0))
        rate = (255/tot_frames,255/tot_frames,255/tot_frames)
      if self.next_func != self.curr_func:
        return
      time.sleep(self.wait_ms/1000.0)

#----------------------------------------------------------------------------------------------------
  def fade_green_to_red(self):
    self.fade_to_color(self.Color(255,0,0),fade_time=self.stuck_open_timeout)

  def color_wipe_to_handle_green(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe_to_handle(self.Color(0,255,0))

  def theatre_chase_white(self):
    """Movie theatre light style chaser animation."""
    self.theatre_chase(self.Color(255,255,255))

  def flash_colors_blue_red(self):
    """Cycle between two colors"""
    self.flash_colors(self.Color(0,0,255), self.Color(255,0,0))

  def flash_colors_red_black(self):
    """Cycle between two colors"""
    self.flash_colors(self.Color(255,0,0), self.Color(96,0,0))
 
  def color_wipe_red(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe(self.Color(255, 0, 0))

  def color_wipe_green(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe(self.Color(0, 255, 0))

  def color_wipe_blue(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe(self.Color(0, 0, 255))

  def set_color_green(self):
    """Sets the color of all pixels."""
    self.set_strip_color(self.Color(0,255,0))

  def rainbow(self):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel((i+j) & 255))
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        return
  
  def rainbow_cycle(self):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*5):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel(((i * 256 / self.strip.numPixels()) + j) & 255))
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        return

  def color_wipe_to_handle(self, color):
    """Wipe color across display a pixel at a time."""
    handle = self.handle_pixel
    pointing = 10
    # turn all green
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      if self.next_func != self.curr_func:
        self.rainbow_cycle()
        return
    for i in range(pointing):
      self.strip.setPixelColor(handle - i, self.Color(0,0,0))
      self.strip.setPixelColor(handle + i, self.Color(0,0,0))
      self.strip.show()
      if self.next_func != self.curr_func:
        self.rainbow_cycle()
        return
    
    for i in range(pointing -1, -1, -1):
      self.strip.setPixelColor(handle - i, color)
      self.strip.setPixelColor(handle + i, color)
      self.strip.show()
      if self.next_func != self.curr_func:
        self.rainbow_cycle()
        return
      time.sleep(self.wait_ms/1000.0)

  def flash_colors(self, color1, color2):
    """Cycle between two colors"""
    iterations=10
    for j in range(iterations):
      for q in range(2):
        for i in range(0, self.strip.numPixels(), 2):
          if q:
            self.strip.setPixelColor(i, color1)
          else:
            self.strip.setPixelColor(i, color2)
        for i in range(1, self.strip.numPixels(), 2):
          if q:
            self.strip.setPixelColor(i, color2)
          else:
            self.strip.setPixelColor(i, color1)
        self.strip.show()
        time.sleep(self.wait_ms/1000.0)
        if self.next_func != self.curr_func:
          break
      if self.next_func != self.curr_func:
        return

  def theatre_chase(self, color):
    """Movie theatre light style chaser animation."""
    iterations=10
    for j in range(iterations):
      for q in range(3):
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, color)
        self.strip.show()
        time.sleep(self.wait_ms/1000.0)
        if self.next_func != self.curr_func:
          break
        for i in range(0, self.strip.numPixels(), 3):
          self.strip.setPixelColor(i+q, 0)
      if self.next_func != self.curr_func:
        return

  def color_wipe(self, color):
    """Wipe color across display a pixel at a time."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        return

  def set_strip_color(self, color):
    """Sets the color of all pixels."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      self.strip.show()
      if self.next_func != self.curr_func:
        return

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
    self.qc.set_next(self.qc.fade_green_to_red)

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
      self.do_state()

  def set_gui_state(self, state):
    if self.gui:
      self.gui_state.set(state)

  def do_state(self):
    if self.curr_state != self.state:
      self.prev_state = self.state
      self.state = self.curr_state
      self.curr_state()

  def get_state(self):
    return self.state

  def set_state(self, state):
    self.curr_state = state

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel, stuck_open_timeout):
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
    label = Label(frame, textvariable = self.gui_state)
    label.pack(side=LEFT)
    self.info_frame = frame
    frame2 = LabelFrame(root, text=self.name, padx=5, pady=5, bg='black')
    frame2.pack(fill=X)
    self.wait_ms = 50
    self.next_func = 1
    self.curr_func = 1
    self.strip = MockStrip(self.led_count, frame2)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # Intialize the library (must be called once before other functions).
    self.strip.begin()
    self.log.debug("start called")
    self.qc = QuickChange(self.handle_pixel)
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
