import logging
import time
import Queue
import threading

from pystates import StateMachine

class RpiGpioSwitch(StateMachine):

  def ON(self):
    self.logger.debug(self.name + " switch is on ")
    while True:
      ev = yield
      if ev['event'] == self.name + "_TURNED_OFF":
        self.logger.debug("generating message: " + self.off_message)
        self.generate_message({"event": self.off_message})
        self.transition(self.OFF)

  def OFF(self):
    self.logger.debug(self.name + " switch is off")
    while True:
      ev = yield
      if ev['event'] == self.name + "_TURNED_ON":
        self.logger.debug("generating message: " + self.on_message)
        self.generate_message({"event": self.on_message})
        self.transition(self.ON)

  def setup(self, out_queue, name, gpio_pin, on_message, off_message):
    self.logger = logging.getLogger("RpiGpioSwitch")
    self.out_queue = out_queue
    self.name = name
    self.gpio_pin=gpio_pin
    self.on_message = on_message
    self.off_message = off_message

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    #TODO: actually detect the starting state here
    super(RpiGpioSwitch, self).start(self.OFF)


def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  switch_name = "LIGHT"

  switch_1 = RpiGpioSwitch(name=switch_name)
  switch_1.setup(out_queue, name="LIGHT", gpio_pin=24, on_message="DOOR_OPENEND", off_message="DOOR_CLOSED")
  switch_1.start()

  logging.info('turn off the switch')
  switch_1.send_message({"event": switch_name + "_TURNED_OFF"})
  time.sleep(5)

if __name__=='__main__':
  main()
