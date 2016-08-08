import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class blinkenlightsBase(StateMachine):
  """description of class"""
  __metaclass__ = ABCMeta
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("blinkenlightsState")
    self.out_queue = out_queue
    self.name = name
    self.gui = False
  
def set_gui_state(self, state):
    if self.gui:
      self.gui_state.set(state)

  def MAIN_DOOR_CLOSED(self):
    """  """
    self.generate_message({"event": self.name + "_MAIN_DOOR_CLOSED"})
    self.set_gui_state("MAIN_DOOR_CLOSED")
    self.log.debug("NEW STATE: MAIN_DOOR_CLOSED - ")
    self.ON_MAIN_DOOR_CLOSED();

    # Wait for events
    while True:
      ev = yield
      
      if ev['event'] == "MAIN_DOOR_UNLOCKING":
        self.ON_MAIN_DOOR_CLOSED_MAIN_DOOR_UNLOCKING()
        self.transition(self.MAIN_DOOR_UNLOCKING)
        
      if ev['event'] == "MAIN_DOOR_OPENED":
        self.ON_MAIN_DOOR_CLOSED_MAIN_DOOR_OPENED()
        self.transition(self.MAIN_DOOR_OPENED)
        
      if ev['event'] == "INVALID_KEY":
        self.ON_MAIN_DOOR_CLOSED_INVALID_KEY()
        self.transition(self.INVALID_KEY)
        
  def MAIN_DOOR_UNLOCKING(self):
    """  """
    self.generate_message({"event": self.name + "_MAIN_DOOR_UNLOCKING", "timeout": 5000})
    self.set_gui_state("MAIN_DOOR_UNLOCKING")
    self.log.debug("NEW STATE: MAIN_DOOR_UNLOCKING - ")
    self.ON_MAIN_DOOR_UNLOCKING();

    # Wait for events
    while True:
      ev = yield
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_MAIN_DOOR_UNLOCKING_MAIN_DOOR_CLOSED()
        self.transition(self.MAIN_DOOR_CLOSED)
        
      if ev['event'] == "MAIN_DOOR_OPENED":
        self.ON_MAIN_DOOR_UNLOCKING_MAIN_DOOR_OPENED()
        self.transition(self.MAIN_DOOR_OPENED)
        
  def INVALID_KEY(self):
    """  """
    self.generate_message({"event": self.name + "_INVALID_KEY", "timeout": 1500})
    self.set_gui_state("INVALID_KEY")
    self.log.debug("NEW STATE: INVALID_KEY - ")
    self.ON_INVALID_KEY();

    # Wait for events
    while True:
      ev = yield
      
      if ev['event'] == "MAIN_DOOR_INVALID_TIMEOUT":
        self.ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT()
        self.transition(self.MAIN_DOOR_CLOSED)
        
  def MAIN_DOOR_STUCK_OPEN(self):
    """  """
    self.generate_message({"event": self.name + "_MAIN_DOOR_STUCK_OPEN"})
    self.set_gui_state("MAIN_DOOR_STUCK_OPEN")
    self.log.debug("NEW STATE: MAIN_DOOR_STUCK_OPEN - ")
    self.ON_MAIN_DOOR_STUCK_OPEN();

    # Wait for events
    while True:
      ev = yield
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_MAIN_DOOR_STUCK_OPEN_MAIN_DOOR_CLOSED()
        self.transition(self.MAIN_DOOR_CLOSED)
        
  def MAIN_DOOR_OPENED(self):
    """  """
    self.generate_message({"event": self.name + "_MAIN_DOOR_OPENED", "timeout": 15000})
    self.set_gui_state("MAIN_DOOR_OPENED")
    self.log.debug("NEW STATE: MAIN_DOOR_OPENED - ")
    self.ON_MAIN_DOOR_OPENED();

    # Wait for events
    while True:
      ev = yield
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_MAIN_DOOR_OPENED_MAIN_DOOR_CLOSED()
        self.transition(self.MAIN_DOOR_CLOSED)
        
      if ev['event'] == "MAIN_DOOR_STUCK_TIMEOUT":
        self.ON_MAIN_DOOR_OPENED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.MAIN_DOOR_STUCK_OPEN)
        
  def MAIN_DOOR_FORCED_OPEN(self):
    """  """
    self.generate_message({"event": self.name + "_MAIN_DOOR_FORCED_OPEN"})
    self.set_gui_state("MAIN_DOOR_FORCED_OPEN")
    self.log.debug("NEW STATE: MAIN_DOOR_FORCED_OPEN - ")
    self.ON_MAIN_DOOR_FORCED_OPEN();

    # Wait for events
    while True:
      ev = yield
      
      if ev['event'] == "MAIN_DOOR_UNLOCKING":
        self.ON_MAIN_DOOR_FORCED_OPEN_MAIN_DOOR_UNLOCKING()
        self.transition(self.MAIN_DOOR_OPENED)
        
  
  # By Default - do nothing ON_MAIN_DOOR_CLOSED
  def ON_MAIN_DOOR_CLOSED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_CLOSED_MAIN_DOOR_UNLOCKING(self):
    """ While in MAIN_DOOR_CLOSED, a MAIN_DOOR_UNLOCKING message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_CLOSED_MAIN_DOOR_OPENED(self):
    """ While in MAIN_DOOR_CLOSED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_CLOSED_INVALID_KEY(self):
    """ While in MAIN_DOOR_CLOSED, a INVALID_KEY message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_UNLOCKING
  def ON_MAIN_DOOR_UNLOCKING(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_UNLOCKING_MAIN_DOOR_CLOSED(self):
    """ While in MAIN_DOOR_UNLOCKING, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_UNLOCKING_MAIN_DOOR_OPENED(self):
    """ While in MAIN_DOOR_UNLOCKING, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_INVALID_KEY
  def ON_INVALID_KEY(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT(self):
    """ While in INVALID_KEY, a MAIN_DOOR_INVALID_TIMEOUT message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_STUCK_OPEN
  def ON_MAIN_DOOR_STUCK_OPEN(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_STUCK_OPEN_MAIN_DOOR_CLOSED(self):
    """ While in MAIN_DOOR_STUCK_OPEN, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_OPENED
  def ON_MAIN_DOOR_OPENED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_OPENED_MAIN_DOOR_CLOSED(self):
    """ While in MAIN_DOOR_OPENED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_OPENED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in MAIN_DOOR_OPENED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  
  # By Default - do nothing ON_MAIN_DOOR_FORCED_OPEN
  def ON_MAIN_DOOR_FORCED_OPEN(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_MAIN_DOOR_FORCED_OPEN_MAIN_DOOR_UNLOCKING(self):
    """ While in MAIN_DOOR_FORCED_OPEN, a MAIN_DOOR_UNLOCKING message is recieved. """
    pass