import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine
class DoorState(StateMachine):

  def setInfoText(self,text):
    if self.show_gui:
      self.v.set(text)
      self.infoText = self.v

  def track(self,ev):
    '''Tracks the state of the door, and updates the vars and display.
    '''
    if ev['event'] == 'MAIN_DOOR_MODE_UNLOCKED':
      self.IN_LOCK_MODE = False
      self.log.debug('Door left lockmode')

    if ev['event'] == 'MAIN_DOOR_MODE_LOCKED':
      self.IN_LOCK_MODE = True
      self.log.debug('Door entered lockmode')

    if ev['event'] == 'MAIN_DOOR_SENSOR_CLOSED':
      self.IS_OPEN = False
      self.log.debug('Door closed')

    if ev['event'] == 'MAIN_DOOR_SENSOR_OPENED':
      self.IS_OPEN = True
      self.log.debug('Door opened')
    self.currentInfo ='STUCK: {} | IN_LOCK_MODE: {} | IS_OPEN: {}'.format(self.STUCK, self.IN_LOCK_MODE, self.IS_OPEN)
    if self.infoText != self.currentInfo:
      self.setInfoText(self.currentInfo)

  def FORCED(self):
    self.generate_message({"event": self.name + "_FORCED_OPEN"})
    while True:
      ev = yield
      self.track(ev)
      if ev['event'] == "VALID_KEY":
        if self.CLOSED_LOCKED:
          self.transition(self.UNLOCKING)
        else:
          self.transition(self.IS_OPEN)

  def CLOSED_LOCKED(self):
    self.generate_message({"event": self.name + "_CLOSED_LOCKED"})
    self.log.debug("turn off solenoid")

    while True:
      ev = yield
      self.track(ev)
      if ev['event'] == "VALID_KEY":
        self.transition(self.UNLOCKING)
      if self.IS_OPEN:
        if self.IN_LOCK_MODE:
          self.transition(self.FORCED)
        else:
          self.transition(self.OPEN)

  def UNLOCKING(self):
    self.generate_message({"event": self.name + "_UNLOCKING", "timeout": self.unlock_timeout})
    self.log.debug("turn on solenoid")
    self.log.debug("waiting up to " + str(self.unlock_timeout) + " seconds")

    while True:
      ev = yield
      self.track(ev)
      if self.IS_OPEN:
        self.log.debug('Unlocked and opened')
        time.sleep(self.open_unlock_timeout) #open unlocking replacement (?)
        self.transition(self.OPEN)
      if self.duration() > self.unlock_timeout:
        self.log.debug('Unlocked but was not opened')
        self.transition(self.CLOSED_LOCKED)

  def OPEN(self):
    self.generate_message({"event": self.name + "_OPENED"})
    self.log.debug("turn off solenoid")
    self.log.debug("waiting up to " + str(self.stuck_open_timeout) + "seconds")

    while True:
      ev = yield
      self.track(ev)
      if not self.IS_OPEN:
        self.STUCK = False
        self.transition(self.CLOSED_LOCKED)
      if not self.STUCK and self.duration() > self.stuck_open_timeout:
        self.log.debug("timeout!")
        self.generate_message({"event": self.name + "_STUCK_OPEN"})
        self.STUCK = True

  def setup(self, out_queue, name, unlock_timeout=5, open_unlock_timeout=1, stuck_open_timeout=15):
    self.log = logging.getLogger("DoorState")
    self.out_queue = out_queue
    self.name = name
    self.unlock_timeout = int(unlock_timeout)
    self.open_unlock_timeout = int(open_unlock_timeout)
    self.stuck_open_timeout = int(stuck_open_timeout)
    self.infoText = ''
    self.STUCK = False
    self.IS_OPEN = False
    self.IN_LOCK_MODE = True

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # assume a starting state of CLOSED_LOCKED and appropriate messages will send it to the correct state
    super(DoorState, self).start(self.CLOSED_LOCKED)

  def config_gui(self, root):
    self.show_gui = True
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
  doorstate.setup(out_queue, name=name)
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

