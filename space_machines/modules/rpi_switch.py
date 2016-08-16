from DerivedBaseClasses.switchBase import *
import sys
if sys.platform=='linux2':
  import RPi.GPIO as GPIO

class RpiGpioSwitch(SwitchBase):

  def WHILE_OFF(self):
    if GPIO.input(self.gpio_pin):
      self.generate_message({"event": self.name + '_TURN_ON'})

  def WHILE_ON(self):
    if not GPIO.input(self.gpio_pin):
      self.generate_message({"event": self.name + '_TURN_OFF'})

  def setup(self, out_queue, name, gpio_pin, on_message, off_message):
    self.logger = logging.getLogger("RpiGpioSwitch")
    self.out_queue = out_queue
    self.name = name
    self.gpio_pin=int(gpio_pin)
    self.on_message = on_message
    self.off_message = off_message
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  def start(self):
    state = GPIO.input(self.gpio_pin)
    if (state == True):
      self.logger.debug("initial state: " + self.on_message)
      self.generate_message({"event": self.on_message})
      super(RpiGpioSwitch, self).start(self.ON)
    else:
      self.logger.debug("initial state: " + self.off_message)
      self.generate_message({"event": self.off_message})
      super(RpiGpioSwitch, self).start(self.OFF)