import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

class DoorState(StateMachine):
  def CLOSED_LOCKED(self):
    self.v.set("CLOSED_LOCKED")
    self.log.debug("turn off solenoid")
    while True:
      ev = yield
      if ev['event'] == "VALID_KEY":
        self.transition(self.CLOSED_UNLOCKING)
      if ev['event'] == "DOOR_OPENED":
        self.transition(self.FORCED_OPEN)

  def CLOSED_UNLOCKING(self):
    self.v.set("CLOSED_UNLOCKING")
    self.log.debug("turn on solenoid")
    self.log.debug("waiting up to " + str(self.unlock_timeout) + " seconds")
    while True:
      ev = yield
      if ev['event'] == "DOOR_OPENED":
        self.log.debug('Unlocked and opened')
        self.transition(self.OPEN_UNLOCKING)
      if self.duration() > self.unlock_timeout:
        self.log.debug('Unlocked but not opened')
        self.transition(self.CLOSED_LOCKED)

  def OPEN_UNLOCKING(self):
    self.v.set("OPEN_UNLOCKING")
    self.log.debug("waiting up to " + str(self.open_unlock_timeout) + " seconds")
    while True:
      ev = yield
      if ev['event'] == "DOOR_CLOSED":
        self.log.debug('Door closed')
        self.transition(self.CLOSED_LOCKED)
      if self.duration() > self.open_unlock_timeout:
        self.transition(self.OPEN_LOCKED)

  def OPEN_LOCKED(self):
    self.v.set("OPEN_LOCKED")
    self.log.debug("turn off solenoid")
    self.log.debug("waiting up to " + str(self.stuck_open_timeout) + "seconds")
    while True:
      ev = yield
      if ev['event'] == "DOOR_CLOSED":
        self.log.debug('Door closed')
        self.transition(self.CLOSED_LOCKED)
      if self.duration() > self.stuck_open_timeout:
        self.log.debug("timeout!")
        self.transition(self.STUCK_OPEN)

  def STUCK_OPEN(self):
    self.v.set("STUCK_OPEN")
    self.log.debug("door stuck open")
    while True:
      ev = yield
      if ev['event'] == "DOOR_CLOSED":
        self.log.debug('Door finally closed')
        self.transition(self.CLOSED_LOCKED)

  def FORCED_OPEN(self):
    self.v.set("FORCED_OPEN")
    self.log.debug("door forced open")
    while True:
      ev = yield
      if ev['event'] == "DOOR_CLOSED":
        self.log.debug('Door closed')
        self.transition(self.CLOSED_LOCKED)
      if self.duration() > self.stuck_open_timeout:
        self.log.debug("timeout!")
        self.transition(self.STUCK_OPEN)

  def setup(self, out_queue, name, solenoid_pin, unlock_timeout, open_unlock_timeout, stuck_open_timeout):
    self.log = logging.getLogger("DoorState")
    self.out_queue = out_queue
    self.name = name
    self.solenoid_pin=int(solenoid_pin)
    self.unlock_timeout = int(unlock_timeout)
    self.open_unlock_timeout = int(open_unlock_timeout)
    self.stuck_open_timeout = int(stuck_open_timeout)

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # assume a starting state of CLOSED_LOCKED and appropriate messages will send it to the correct state
    super(DoorState, self).start(self.CLOSED_LOCKED)

  def config_gui(self, root):
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)


def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_DOOR"

  doorstate = DoorState(name=name)
  doorstate.setup(out_queue, name=name, solenoid_pin=24)
  doorstate.start()

  doorstate.send_message({"event": "VALID_KEY"})

  logging.info('unlock the door, open then close it')
  doorstate.send_message({"event":"VALID_KEY"})
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_OPENED"})
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

  logging.info('current state:' + doorstate.current_state())
  logging.info('unlock the door but do not open it')
  time.sleep(2)
  doorstate.send_message({"event":"VALID_KEY"})
  time.sleep(10)


  logging.info('open the door and close it quickly')
  time.sleep(0.1)
  doorstate.send_message({"event":"VALID_KEY"})
  doorstate.send_message({"event":"DOOR_OPENED"})
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

  logging.info('open the door and leave it open for 30 seconds')
  time.sleep(2)
  doorstate.send_message({"event":"VALID_KEY"})
  doorstate.send_message({"event":"DOOR_OPENED"})
  time.sleep(30)

  time.sleep(2)
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

  logging.info('force the door open')
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_OPENED"})
  time.sleep(2)
  doorstate.send_message({"event":"DOOR_CLOSED"})
  time.sleep(2)

if __name__=='__main__':
  main()

