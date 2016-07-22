import sys
if sys.platform=='linux2':

  import logging
  import time
  import Queue
  import threading
  
  import RPi.GPIO as GPIO

  from pystates import StateMachine

  class RpiGpioOutput(StateMachine):

    def ON(self):
      self.logger.info(self.name + " output turned on ")
      GPIO.output(self.gpio_pin, 1)
      while True:
        ev = yield
        if ev['event'] == self.off_message:
          self.transition(self.OFF)

    def OFF(self):
      self.logger.info(self.name + " output turned off")
      GPIO.output(self.gpio_pin, 0)
      while True:
        ev = yield
        if ev['event'] == self.on_message:
          self.transition(self.ON)

    def setup(self, out_queue, name, gpio_pin, on_message, off_message, initial_state):
      self.logger = logging.getLogger("RpiGpioOutput")
      self.out_queue = out_queue
      self.name = name
      self.gpio_pin=int(gpio_pin)
      self.on_message = on_message
      self.off_message = off_message
      self.initial_state = initial_state

    """ Perform initialization here
    """
    def start(self):
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(self.gpio_pin, GPIO.OUT)
      if (self.initial_state == "ON"):
        self.logger.debug("initial state: " + self.on_message)
        super(RpiGpioOutput, self).start(self.ON)
      else:
        self.logger.debug("initial state: " + self.off_message)
        super(RpiGpioOutput, self).start(self.OFF)
else:
  from guiswitch import *
  RpiGpioSwitch = GuiSwitch
