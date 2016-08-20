import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

from DerivedBaseClasses.door_lockBase import *

class door_lockStateMachine(door_lockBase):
  __metaclass__ = ABCMeta
  """description of class"""
  
  

    
  def setup(self, out_queue, name, unlock_timeout=5):
    self.log = logging.getLogger("door_lock")
    self.out_queue = out_queue
    self.name = name
    self.unlock_timeout = int(unlock_timeout)#not currently being used by base

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    # assume a the starting state assigned by MyStateMachines.com
    super(door_lockStateMachine, self).start(self.UNLOCKED)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)


  def ON_ENTER_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED_ENTER"})
    self.generate_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})

  def ON_ENTER_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED_ENTER"})
    self.generate_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_EXTEND"})

  def ON_ENTER_TEMP_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED_ENTER"})
    self.generate_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})

  def WHILE_UNLOCKED(self, ev):
    """  """
    if ev['event'] == "VALID_KEY":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_TEMP_UNLOCK"})
    if ev['event'] == "LOCK_MODE_SWITCH_LOCKED_MODE_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LOCK"})

  def WHILE_LOCKED(self, ev):
    """  """
    if ev['event'] == "LOCK_MODE_SWITCH_UNLOCKED_MODE_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    if ev['event'] == "VALID_KEY":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_TEMP_UNLOCK"})


  def WHILE_TEMP_UNLOCKED(self, ev):
    """  """
    if ev['event'] == "LOCK_MODE_SWITCH_UNLOCKED_MODE_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    if ev['event'] == "LOCK_MODE_SWITCH_LOCKED_MODE_ENTER":
      self.generate_message({"event": "REQUEST_MAIN_DOOR_LOCK"})

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "TEST_door_lock"

  door_lockTestMachine = door_lockStateMachine(name=name)
  door_lockTestMachine.setup(out_queue, name=name)
  door_lockTestMachine.start()

  # Send some test messages
  
  # Start Testing sample state machine by sending some random messages
  # Current State: UNLOCKED
  # Next State: LOCKED
  # Send Message 10 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_SOLENOID_RETRACT"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 9 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 8 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 7 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 6 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 5 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 4 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 3 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  # Current State: TEMP_UNLOCKED
  # Next State: LOCKED
  # Send Message 2 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
    
  # Current State: LOCKED
  # Next State: TEMP_UNLOCKED
  # Send Message 1 after 2 seconds.
  time.sleep(2)
  door_lockTestMachine.send_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
    
  

if __name__=='__main__':
  main()

