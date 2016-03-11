import logging
import time
import Queue
import threading

import RPi.GPIO as GPIO

from pystates import StateMachine

class RpiGpioRelay(StateMachine):

  def ON(self):
    self.logger.debug(self.name + " relay turned on ")
    GPIO.output(self.gpio_pin, True)
    while True:
      ev = yield
      if ev['event'] == self.off_message:
        self.transition(self.OFF)

  def OFF(self):
    self.logger.debug(self.name + " relay turned off")
    GPIO.output(self.gpio_pin, False)
    while True:
      ev = yield
      if ev['event'] == self.on_message:
        self.transition(self.ON)

  def setup(self, out_queue, name, gpio_pin, on_message, off_message):
    self.logger = logging.getLogger("RpiGpioRelay")
    self.out_queue = out_queue
    self.name = name
    self.gpio_pin=int(gpio_pin)
    self.on_message = on_message
    self.off_message = off_message

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.OUT)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    #TODO: start in the off state
    self.logger.debug("initial state: " + self.off_message)
    super(RpiGpioRelay, self).start(self.OFF)

