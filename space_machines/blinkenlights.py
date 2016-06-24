import logging
import time
import Queue
import threading
import sys
from Tkinter import *
from pystates import StateMachine
##from neopixel import * #-----I double hashtagged code i disabled relating to this.
import math
import random

 
class QuickChange:
  def __init__(self, handle_pixel):
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

  def int_color(self, color):
    """returns color to a truple of integers"""
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
#----------------------------------------------------------------------------------------------------
  def color_wipe_to_handle_green(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe_to_handle(self.Color(0,255,0))

  def theatre_chase_white(self):
    """Movie theatre light style chaser animation."""
    self.theatre_chase(self.Color(255,255,255))

  def flash_colors_red_black(self):
    """Cycle between two colors"""
    self.flash_colors(self.Color(255,0,0), self.Color(128,0,0))
 
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

  def fade_green_to_red(self):
    """fade from one color to another"""
    self.fade_time = self.stuck_open_timeout
    self.fade(self.Color(0,255,0),self.Color(255,0,0))

  def rainbow(self):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel((i+j) & 255))
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        break
  
  def rainbow_cycle(self):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*5):
      for i in range(self.strip.numPixels()):
        self.strip.setPixelColor(i, self.wheel(((i * 256 / self.strip.numPixels()) + j) & 255))
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        break
  def color_wipe_to_handle(self, color):
    """Wipe color across display a pixel at a time."""
    handle = self.handle_pixel
    pointing = 10
    # turn all green
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      if self.next_func != self.curr_func:
        break
    for i in range(pointing):
      self.strip.setPixelColor(handle - i, self.Color(0,0,0))
      self.strip.setPixelColor(handle + i, self.Color(0,0,0))
      if self.next_func != self.curr_func:
        break
    self.strip.show()
    for i in range(pointing -1, -1, -1):
      self.strip.setPixelColor(handle - i, color)
      self.strip.setPixelColor(handle + i, color)
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        break

  def flash_colors(self, color1, color2):
    """Cycle between two colors"""
    iterations=10
    for j in range(iterations):
      for q in range(2):
        for i in range(0, self.strip.numPixels(), 2):
          self.strip.setPixelColor(i+q, color1)
        for i in range(1, self.strip.numPixels(), 2):
          self.strip.setPixelColor(i+q, 0)
        self.strip.show()
        time.sleep(self.wait_ms/1000.0)
        if self.next_func != self.curr_func:
          break
      if self.next_func != self.curr_func:
        break

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
        break

  def color_wipe(self, color):
    """Wipe color across display a pixel at a time."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        break

  def set_strip_color(self, color):
    """Sets the color of all pixels."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      self.strip.show()
      if self.next_func != self.curr_func:
        break

  def fade(self, color1, color2):
    """fade from one color to another"""
    def interval(index):
      return abs((x[index]-y[index])/tot_frames) or 1
    x = self.int_color(color1)
    y = self.int_color(color2)
    temp = []
    time_0 = time.time()
    self.set_strip_color(self.Color(*x))
    frametime = time.time() - time_0
    tot_frames = float((self.fade_time or 15)/(frametime + self.wait_ms/1000.0))
    i = [interval(0), interval(1), interval(2)]
    #print("x:{0} |y:{1} |frametime:{2} |tot_frames:{3} |i:{4}".format(x,y,frametime,tot_frames,i))
    #print(0,x)
    for t in range(int(tot_frames)):
      for j in range(3):
        if x[j]>y[j]:
          z = x[j] - i[j]
        elif x[j]<y[j]:
          z = x[j] + i[j]
        elif x[j]==y[j]:
          z = x[j]
        if z >255 or z<0:
          temp.append(y[j])
        else:
          temp.append(z)
      x = temp
      temp = []
      self.set_strip_color(self.Color(*[int(round(n)) for n in x]))
      if self.next_func != self.curr_func:
        return
      time.sleep(self.wait_ms/1000.0)#----------why is this necessary?--BK
    self.set_strip_color(color2)
    while True:
      if self.next_func != self.curr_func:
        return
      time.sleep(self.wait_ms/1000.0)


class BlinkenLights(StateMachine):

  def VALID_KEY(self):
    self.state.set("VALID_KEY")
    self.qc.set_next(self.qc.color_wipe_to_handle_green)
    while True:
      ev = yield
      if ev['event'] == "MAIN_DOOR_CLOSED_LOCKED":
        self.transition(self.WAITING)

  def INVALID_KEY(self):
    self.state.set("INVALID_KEY")
    self.qc.set_next(self.qc.flash_colors_red_black)
    while True:
      ev = yield
      if self.duration() > 2:
        self.transition(self.WAITING)
      if ev['event'] == "VALID_KEY":
        self.transition(self.VALID_KEY)

  def WAITING(self):
    self.state.set("WAITING")
    self.qc.set_next(self.qc.rainbow_cycle)
    while True:
      ev = yield
      if ev['event'] == "VALID_KEY":
        self.transition(self.VALID_KEY)
      if ev['event'] == "INVALID_KEY":
        self.transition(self.INVALID_KEY)

  def config_gui(self, root):
    # Set up the GUI part
    frame = LabelFrame(root, text="STATE", padx=5, pady=5)
    frame.pack(fill=X)
    self.state = StringVar()
    self.state.set("[STATE]")
    label = Label(frame, textvariable = self.state)
    label.pack(side=LEFT)
    self.info_frame = frame
    frame2 = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame2.pack(fill=X)
    self.wait_ms = 50
    self.next_func = 1
    self.curr_func = 1
    self.strip = MockStrip(self.led_count, frame2)

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel, stuck_open_timeout):
    self.log = logging.getLogger("BlinkenLights")
    self.out_queue = out_queue
    self.name = name
    # the pixel closest to the handle
    self.handle_pixel = int(handle_pixel)
    self.led_count=int(led_count)      # Number of LED pixels.
    self.led_pin = int(led_pin)        # GPIO pin connected to the pixels (must support PWM!).
    self.led_freq_hz = int(led_freq_hz) # LED signal frequency in hertz (usually 800khz)
    self.led_dma = int(led_dma)         # DMA channel to use for generating signal (try 5)
    self.led_brightness = int(led_brightness) # Set to 0 for darkest and 255 for brightest
    self.led_invert = led_invert.lower() in ("yes", "true", "t", "1")  # True to invert the signal (when using NPN transistor level shift)
    self.stuck_open_timeout = int(stuck_open_timeout)
    # Create NeoPixel object with appropriate configuration.
    ##self.strip = Adafruit_NeoPixel(self.led_count, self.led_pin, self.led_freq_hz, self.led_dma, self.led_invert, self.led_brightness)
    #self.strip = Adafruit_NeoPixel(self.led_count, 18, 800000, 5, False, 255)


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
    super(BlinkenLights, self).start(self.WAITING)


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

  def begin(self):
    pass

  def setPixelColor(self, pixel, color):
    self.pending[pixel]=self.tk_color(color)

  def getPixelColor(self, pixel):
    return self.pending[pixel]

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
  machine.send_message({"event": "VALID_KEY"})

  time.sleep(15)

if __name__=='__main__':
  main()
