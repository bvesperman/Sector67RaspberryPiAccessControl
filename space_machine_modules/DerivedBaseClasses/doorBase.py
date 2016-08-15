import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class doorBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("doorState")
    self.out_queue = out_queue
    self.name = name
  def DOOR_CLOSED_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_CLOSED_LOCKED"})
    if self.show_gui: self.v.set("DOOR_CLOSED_LOCKED")
    self.log.debug("NEW STATE: DOOR_CLOSED_LOCKED - ")
    self.ON_DOOR_CLOSED_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "INVALID_KEY":
        self.ON_DOOR_CLOSED_LOCKED_INVALID_KEY()
        self.transition(self.INVALID_KEY)
      
      if ev['event'] == "MAIN_DOOR_UNLOCK":
        self.ON_DOOR_CLOSED_LOCKED_MAIN_DOOR_UNLOCK()
        self.transition(self.DOOR_CLOSED_UNLOCKED)
      
      if ev['event'] == "VALID_KEY":
        self.ON_DOOR_CLOSED_LOCKED_VALID_KEY()
        self.transition(self.DOOR_CLOSED_GRANTING_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_OPENED":
        self.ON_DOOR_CLOSED_LOCKED_MAIN_DOOR_OPENED()
        self.transition(self.DOOR_OPEN_LOCKED)
      
  def DOOR_CLOSED_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_CLOSED_UNLOCKED"})
    if self.show_gui: self.v.set("DOOR_CLOSED_UNLOCKED")
    self.log.debug("NEW STATE: DOOR_CLOSED_UNLOCKED - ")
    self.ON_DOOR_CLOSED_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "INVALID_KEY":
        self.ON_DOOR_CLOSED_UNLOCKED_INVALID_KEY()
        self.transition(self.DOOR_CLOSED_GRANTING_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_OPENED":
        self.ON_DOOR_CLOSED_UNLOCKED_MAIN_DOOR_OPENED()
        self.transition(self.DOOR_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCK":
        self.ON_DOOR_CLOSED_UNLOCKED_MAIN_DOOR_LOCK()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
      if ev['event'] == "VALID_KEY":
        self.ON_DOOR_CLOSED_UNLOCKED_VALID_KEY()
        self.transition(self.DOOR_CLOSED_GRANTING_UNLOCKED)
      
  def DOOR_CLOSED_GRANTING_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_CLOSED_GRANTING_LOCKED", "timeout": 5000})
    if self.show_gui: self.v.set("DOOR_CLOSED_GRANTING_LOCKED")
    self.log.debug("NEW STATE: DOOR_CLOSED_GRANTING_LOCKED - ")
    self.ON_DOOR_CLOSED_GRANTING_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 5000:
        self.ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED_GRANTING_TIMEOUT":
        self.ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_OPENED":
        self.ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_OPENED()
        self.transition(self.DOOR_OPEN_GRANTING_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_UNLOCK":
        self.ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_UNLOCK()
        self.transition(self.DOOR_CLOSED_GRANTING_UNLOCKED)
      
  def DOOR_OPEN_GRANTING_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_OPEN_GRANTING_LOCKED", "timeout": 1000})
    if self.show_gui: self.v.set("DOOR_OPEN_GRANTING_LOCKED")
    self.log.debug("NEW STATE: DOOR_OPEN_GRANTING_LOCKED - ")
    self.ON_DOOR_OPEN_GRANTING_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 1000:
        self.ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT()
        self.transition(self.DOOR_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_UNLOCK":
        self.ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_UNLOCK()
        self.transition(self.DOOR_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_OPEN_GRANTING_TIMEOUT":
        self.ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT()
        self.transition(self.DOOR_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_CLOSED()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
  def DOOR_OPEN_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_OPEN_LOCKED", "timeout": 15000})
    if self.show_gui: self.v.set("DOOR_OPEN_LOCKED")
    self.log.debug("NEW STATE: DOOR_OPEN_LOCKED - ")
    self.ON_DOOR_OPEN_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 15000:
        self.ON_DOOR_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.DOOR_STUCK_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_STUCK_TIMEOUT":
        self.ON_DOOR_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.DOOR_STUCK_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_UNLOCK":
        self.ON_DOOR_OPEN_LOCKED_MAIN_DOOR_UNLOCK()
        self.transition(self.DOOR_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_DOOR_OPEN_LOCKED_MAIN_DOOR_CLOSED()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
  def DOOR_OPEN_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_OPEN_UNLOCKED", "timeout": 15000})
    if self.show_gui: self.v.set("DOOR_OPEN_UNLOCKED")
    self.log.debug("NEW STATE: DOOR_OPEN_UNLOCKED - ")
    self.ON_DOOR_OPEN_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 15000:
        self.ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.DOOR_STUCK_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCK":
        self.ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_LOCK()
        self.transition(self.DOOR_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_STUCK_TIMEOUT":
        self.ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.DOOR_STUCK_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_CLOSED()
        self.transition(self.DOOR_CLOSED_UNLOCKED)
      
  def DOOR_CLOSED_GRANTING_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_CLOSED_GRANTING_UNLOCKED", "timeout": 5000})
    if self.show_gui: self.v.set("DOOR_CLOSED_GRANTING_UNLOCKED")
    self.log.debug("NEW STATE: DOOR_CLOSED_GRANTING_UNLOCKED - ")
    self.ON_DOOR_CLOSED_GRANTING_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "MAIN_DOOR_CLOSED_GRANTING_TIMEOUT":
        self.ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.DOOR_CLOSED_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCK":
        self.ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_LOCK()
        self.transition(self.DOOR_CLOSED_GRANTING_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_OPENED":
        self.ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_OPENED()
        self.transition(self.DOOR_OPEN_UNLOCKED)
      
  def DOOR_STUCK_OPEN_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_STUCK_OPEN_LOCKED"})
    if self.show_gui: self.v.set("DOOR_STUCK_OPEN_LOCKED")
    self.log.debug("NEW STATE: DOOR_STUCK_OPEN_LOCKED - ")
    self.ON_DOOR_STUCK_OPEN_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "MAIN_DOOR_UNLOCK":
        self.ON_DOOR_STUCK_OPEN_LOCKED_MAIN_DOOR_UNLOCK()
        self.transition(self.DOOR_STUCK_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_DOOR_STUCK_OPEN_LOCKED_MAIN_DOOR_CLOSED()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
  def DOOR_STUCK_OPEN_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_DOOR_STUCK_OPEN_UNLOCKED"})
    if self.show_gui: self.v.set("DOOR_STUCK_OPEN_UNLOCKED")
    self.log.debug("NEW STATE: DOOR_STUCK_OPEN_UNLOCKED - ")
    self.ON_DOOR_STUCK_OPEN_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "MAIN_DOOR_CLOSED":
        self.ON_DOOR_STUCK_OPEN_UNLOCKED_MAIN_DOOR_CLOSED()
        self.transition(self.DOOR_CLOSED_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCK":
        self.ON_DOOR_STUCK_OPEN_UNLOCKED_MAIN_DOOR_LOCK()
        self.transition(self.DOOR_STUCK_OPEN_LOCKED)
      
  def INVALID_KEY(self):
    """  """
    self.generate_message({"event": self.name + "_INVALID_KEY", "timeout": 2000})
    if self.show_gui: self.v.set("INVALID_KEY")
    self.log.debug("NEW STATE: INVALID_KEY - ")
    self.ON_INVALID_KEY();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 2000:
        self.ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_INVALID_TIMEOUT":
        self.ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT()
        self.transition(self.DOOR_CLOSED_LOCKED)
      
  
  # By Default - do nothing ON_DOOR_CLOSED_LOCKED
  def ON_DOOR_CLOSED_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_INVALID_KEY(self):
    """ While in DOOR_CLOSED_LOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_CLOSED_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_VALID_KEY(self):
    """ While in DOOR_CLOSED_LOCKED, a VALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_LOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_LOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_CLOSED_UNLOCKED
  def ON_DOOR_CLOSED_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_INVALID_KEY(self):
    """ While in DOOR_CLOSED_UNLOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_UNLOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_CLOSED_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_UNLOCKED_VALID_KEY(self):
    """ While in DOOR_CLOSED_UNLOCKED, a VALID_KEY message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_CLOSED_GRANTING_LOCKED
  def ON_DOOR_CLOSED_GRANTING_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in DOOR_CLOSED_GRANTING_LOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_GRANTING_LOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_CLOSED_GRANTING_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_OPEN_GRANTING_LOCKED
  def ON_DOOR_OPEN_GRANTING_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_OPEN_GRANTING_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT(self):
    """ While in DOOR_OPEN_GRANTING_LOCKED, a MAIN_DOOR_OPEN_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_GRANTING_LOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_OPEN_GRANTING_LOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_OPEN_LOCKED
  def ON_DOOR_OPEN_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in DOOR_OPEN_LOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_OPEN_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_LOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_OPEN_LOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_OPEN_UNLOCKED
  def ON_DOOR_OPEN_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_OPEN_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in DOOR_OPEN_UNLOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_OPEN_UNLOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_OPEN_UNLOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_CLOSED_GRANTING_UNLOCKED
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in DOOR_CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_OPENED(self):
    """ While in DOOR_CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_STUCK_OPEN_LOCKED
  def ON_DOOR_STUCK_OPEN_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_LOCKED_MAIN_DOOR_UNLOCK(self):
    """ While in DOOR_STUCK_OPEN_LOCKED, a MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_LOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_STUCK_OPEN_LOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_DOOR_STUCK_OPEN_UNLOCKED
  def ON_DOOR_STUCK_OPEN_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_UNLOCKED_MAIN_DOOR_CLOSED(self):
    """ While in DOOR_STUCK_OPEN_UNLOCKED, a MAIN_DOOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_DOOR_STUCK_OPEN_UNLOCKED_MAIN_DOOR_LOCK(self):
    """ While in DOOR_STUCK_OPEN_UNLOCKED, a MAIN_DOOR_LOCK message is recieved. """
    pass
      
  
  # By Default - do nothing ON_INVALID_KEY
  def ON_INVALID_KEY(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT(self):
    """ While in INVALID_KEY, a MAIN_DOOR_INVALID_TIMEOUT message is recieved. """
    pass