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
  def __init__(self, handle_pixel=20, trans_time=1):
    self._data_master = {}
    self._data_secondary = {} #currently unused.
    self.curr_func = self.color_wipe_blue
    self.set_next(self.color_wipe_blue)
    self.wait_ms = 50
    self.handle_pixel = handle_pixel
    self.trans_time = float(trans_time)

  def update_strip(self, data):
    """Updates the strip then shows the new strip."""
    for i in data:
      self.strip.setPixelColor(i, self.Color(*[int(round(n)) for n in data[i]]))
    self.strip.show()

  def main(self):
    for i in range(self.strip.numPixels()):
      self._data_master[i] = (0,0,0)
    _data_out = self._data_master
    j = 0
    self.start_trans = None
    while True:
      print(j)
      if self.curr_func == self.next_func:
        _data_out = self.curr_func(self._data_master, j)

      else:
        if not isinstance(self.start_trans, float):
          self.start_trans = time.time()
        self.duration = self.start_trans - time.time()
        self._data_curr_func = self.curr_func(self._data_master, j)
        self._data_next_func = self.next_func(self._data_master, j)
        if self.duration >= self.trans_time:
          self.curr_func = self.next_func
          _data_out = self._data_next_func
          self.start_trans = None
        else:
          for k in self._data_master:
            for v in self._data_master[k]:
              print(k,v)
              print(self._data_master[k])
              print(self._data_curr_func[k])
              _data_out[k][v] = (1 - self.duration/self.trans_time)*self._data_curr_func[k][v] + (self.duration/self.trans_time)*self._data_next_func[k][v]
      self._data_master = _data_out
      self.update_strip(self._data_master)
      time.sleep(self.wait_ms/1000.0)
      j += 1

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
  def fade_to_green(self, data, j):
    return self.fade_to_color(data, j, (0,255,0))
  def fade_to_red(self, data, j):
    return self.fade_to_color(data, j, (255,0,0),fade_time=self.stuck_open_timeout)

  def color_wipe_to_handle_green(self, data, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe_to_handle(data, j, (0,255,0))

  def theatre_chase_white(self, data, j):
    """Movie theatre light style chaser animation."""
    return self.theatre_chase(data, j, (255,255,255))

  def flash_colors_blue_red(self, data, j):
    """Cycle between two colors"""
    return self.flash_colors(data, j, (0,0,255), (255,0,0))

  def flash_colors_red_black(self, data, j):
    """Cycle between two colors"""
    return self.flash_colors(data, j, (255,0,0), (96,0,0))
 
  def color_wipe_red(self, data, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe(data, j, (255, 0, 0))

  def color_wipe_green(self, data, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe(data, j, (0, 255, 0))

  def color_wipe_blue(self, data, j):
    """Wipe color across display a pixel at a time."""
    return self.color_wipe(data, j, (0, 0, 255))

  def set_color_green(self, data, j):
    """Sets the color of all pixels."""
    return self.set_strip_color(data, j, (0,255,0))

  def rainbow(self, data, j):
    """Draw rainbow that fades across all pixels at once."""
    _data_out = data
    for i in data:
      _data_out[i] = self.wheel((i+j) & 255)
    return _data_out
  
  def rainbow_cycle(self, data, j):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    _data_out = data
    for i in data:
      _data_out[i] = self.wheel((i * 256 / len(data)) + j & 255)
    return _data_out

  def color_wipe_to_handle(self, data, j, color, pointing=10):
    """Wipe color across display a pixel at a time."""
    handle = self.handle_pixel
    # turn all green
    for i in data:
      data[i] = color
    for i in range(pointing):
      data[handle - i] = (0,0,0)
      data[handle + i] = (0,0,0)
      self.strip.show()
    
    for i in range(pointing -1, -1, -1):
      data[handle - i] = color
      data[handle + i] = color
      self.strip.show()

  def flash_colors(self, data, j, color1, color2):
    """Cycle between two colors"""
    _data_out = data
    for i in data:
      if i%2==0:
        if j%2==0:
          _data_out[i] = color1
        else:
          _data_out[i] = color2
      else:
        if j%2==0:
          _data_out[i] = color2
        else:
          _data_out[i] = color1
    return _data_out

  def theatre_chase(self, data, j, color1, color2=(0,0,0)):
    """Movie theatre light style chaser animation."""
    _data_out = data
    for i in data:
      if i%3==0:
        _data_out[i+j%3] = color1
        _data_out[i+(j - 1)%3] = color2
    return _data_out

  def color_wipe(self, data, j, color):
    """Wipe color across display a pixel at a time."""
    _data_out = data
    _data_out[j%self.strip.numPixels()] = color
    return _data_out

  def fade_to_color(self, data, j, color, rate=(5,5,5), fade_time=None):
    _data_out = data
    if fade_time:
      tot_frames = float((fade_time)/(self.wait_ms/1000.0)) #float((fade_time)/(frame_time + self.wait_ms/1000.0))
      rate = (255/tot_frames,255/tot_frames,255/tot_frames)
    for i in data:
      newcolor = []
      curr_color = data[i]
      for c in range(3):
        tempcolor = None
        if curr_color[c] == color[c]:
          tempcolor = color[c]
        elif curr_color[c] < color[c]:
          if curr_color[c] + rate[c] > color[c]:
            tempcolor = color[c]
          else:
            tempcolor = curr_color[c] + rate[c]
        else:
          if curr_color[c] - rate[c] < color[c]:
            tempcolor = color[c]
          else:
            tempcolor = curr_color[c] - rate[c]
        newcolor.append(tempcolor)
      _data_out[i] = newcolor
    return _data_out

  def set_strip_color(self, data, j, color):
    """Sets the color of all pixels."""
    _data_out
    for i in data:
      _data_out[i] = color
    return _data_out

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
    self.qc.set_next(self.qc.fade_to_red)

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
    label = Label(frame, textvariable = self.gui_state, justify=LEFT)
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
