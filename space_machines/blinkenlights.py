import logging
import time
import Queue
import threading

from neopixel import *

from pystates import StateMachine

class BlinkenLights(StateMachine):

  def colorWipe(self, strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    self.log.debug("numpixels: " + str(strip.numPixels()))
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, color)
      strip.show()
      time.sleep(wait_ms/1000.0)

  def theaterChase(self, strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
      for q in range(3):
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, 0)

  def WAITING(self):
    while True:
      # no state transitions for this class, read keys and send messages
      while True:
        ev = yield
        if ev['event'] == "VALID_KEY":
          self.log.debug('colorWipe started')
          self.colorWipe(self.strip, Color(0, 255, 0))
          self.log.debug('colorWipe stopped')
        else:
          self.colorWipe(self.strip, Color(0, 0, 255), 1)
          self.colorWipe(self.strip, Color(255, 0, 255), 1)

  def setup(self, out_queue, name, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness):
    self.log = logging.getLogger("BlinkenLights")
    self.out_queue = out_queue
    self.name = name
    self.led_count=int(led_count)      # Number of LED pixels.
    self.led_pin = int(led_pin)        # GPIO pin connected to the pixels (must support PWM!).
    self.led_freq_hz = int(led_freq_hz) # LED signal frequency in hertz (usually 800khz)
    self.led_dma = int(led_dma)         # DMA channel to use for generating signal (try 5)
    self.led_brightness = int(led_brightness) # Set to 0 for darkest and 255 for brightest
    self.led_invert = led_invert.lower() in ("yes", "true", "t", "1")  # True to invert the signal (when using NPN transistor level shift)
    # Create NeoPixel object with appropriate configuration.
    self.strip = Adafruit_NeoPixel(self.led_count, self.led_pin, self.led_freq_hz, self.led_dma, self.led_invert, self.led_brightness)
    self.strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255)


  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # Intialize the library (must be called once before other functions).
    self.strip.begin()
    self.log.debug("start called")
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
