import logging
import time
import Queue
import threading

from neopixel import *

from pystates import StateMachine

import threading
import sys
import time
 
class QuickChange:
  def __init__(self, handle_pixel):
    self.set_next(self.theatre_chase_white)
    self.curr_func = self.theatre_chase_white
    self.wait_ms = 50
    self.handle_pixel = handle_pixel
 
  def main(self):
    while True:
      self.next_func()
      self.curr_func = self.next_func
 
  def color_wipe_to_handle_green(self):
    self.color_wipe_to_handle(Color(0,255,0))

  def color_wipe_to_handle(self, color):
    """Wipe color across display a pixel at a time."""
    handle = self.handle_pixel
    pointing = 10
    # turn all green
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
    for i in range(pointing):
      self.strip.setPixelColor(handle - i, Color(0,0,0))
      self.strip.setPixelColor(handle + i, Color(0,0,0))
    self.strip.show()
    for i in range(pointing -1, -1, -1):
      self.strip.setPixelColor(handle - i, color)
      self.strip.setPixelColor(handle + i, color)
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        break

  def theatre_chase_white(self):
    self.theatre_chase(Color(255,255,255))

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

 
  def color_wipe_red(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe(Color(255, 0, 0))

  def color_wipe_green(self):
    """Wipe color across display a pixel at a time."""
    self.color_wipe(Color(0, 255, 0))

  def color_wipe(self, color):
    """Wipe color across display a pixel at a time."""
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, color)
      self.strip.show()
      time.sleep(self.wait_ms/1000.0)
      if self.next_func != self.curr_func:
        break

  def wheel(self, pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
      return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return Color(255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return Color(0, pos * 3, 255 - pos * 3)
  
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


  def set_next(self, next_func):
    self.next_func = next_func

  def set_strip(self, strip):
    self.strip = strip

class BlinkenLights(StateMachine):

  def VALID_KEY(self):
    self.qc.set_next(self.qc.color_wipe_to_handle_green)
    while True:
      ev = yield
      if ev['event'] == "MAIN_DOOR_CLOSED_LOCKED":
        self.transition(self.WAITING)

  def INVALID_KEY(self):
    self.qc.set_next(self.qc.color_wipe_red)
    while True:
      ev = yield
      if self.duration() > 2:
        self.transition(self.WAITING)
      if ev['event'] == "VALID_KEY":
        self.transition(self.VALID_KEY)

  def WAITING(self):
    self.qc.set_next(self.qc.rainbow_cycle)
    while True:
      ev = yield
      if ev['event'] == "VALID_KEY":
        self.transition(self.VALID_KEY)
      if ev['event'] == "INVALID_KEY":
        self.transition(self.INVALID_KEY)

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, handle_pixel):
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
    # Create NeoPixel object with appropriate configuration.
    self.strip = Adafruit_NeoPixel(self.led_count, self.led_pin, self.led_freq_hz, self.led_dma, self.led_invert, self.led_brightness)
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
    self.thread = threading.Thread(target=self.qc.main)
    self.thread.setDaemon(True)
    self.thread.start()
    self.log.debug("thread started")
    for i in range(self.strip.numPixels()):
      self.strip.setPixelColor(i, Color(0,255,0))
      self.strip.show()
      time.sleep(50/1000.0)
    super(BlinkenLights, self).start(self.WAITING)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "BLINKENLIGHTS"
  machine = BlinkenLights(name=name)
  machine.setup(out_queue, name=name, led_count=16, led_pin=18, led_freq_hz=800000, led_dma=5, led_invert="False", led_brightness=255)
  machine.start()
  machine.send_message({"event": "VALID_KEY"})

  time.sleep(15)

if __name__=='__main__':
  main()
