import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class DoorBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("doorState")
    self.out_queue = out_queue
    self.name = name

  def CLOSED_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_LOCKED"})
    if self.show_gui: self.v.set("CLOSED_LOCKED")
    self.log.debug("NEW STATE: CLOSED_LOCKED - ")
    self.ON_CLOSED_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "INVALID_KEY":
        self.ON_CLOSED_LOCKED_INVALID_KEY()
        self.transition(self.INVALID_KEY)
      
      if ev['event'] == "MAIN_DOOR_UNLOCKED":
        self.ON_CLOSED_LOCKED_MAIN_DOOR_UNLOCKED()
        self.transition(self.CLOSED_UNLOCKED)
      
      if ev['event'] == "VALID_KEY":
        self.ON_CLOSED_LOCKED_VALID_KEY()
        self.transition(self.CLOSED_GRANTING_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_OPENED":
        self.ON_CLOSED_LOCKED_MAIN_DOOR_SENSOR_OPENED()
        self.transition(self.OPEN_LOCKED)
      
  def CLOSED_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_UNLOCKED"})
    if self.show_gui: self.v.set("CLOSED_UNLOCKED")
    self.log.debug("NEW STATE: CLOSED_UNLOCKED - ")
    self.ON_CLOSED_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "INVALID_KEY":
        self.ON_CLOSED_UNLOCKED_INVALID_KEY()
        self.transition(self.CLOSED_GRANTING_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_OPENED":
        self.ON_CLOSED_UNLOCKED_MAIN_DOOR_SENSOR_OPENED()
        self.transition(self.OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCKED":
        self.ON_CLOSED_UNLOCKED_MAIN_DOOR_LOCKED()
        self.transition(self.CLOSED_LOCKED)
      
      if ev['event'] == "VALID_KEY":
        self.ON_CLOSED_UNLOCKED_VALID_KEY()
        self.transition(self.CLOSED_GRANTING_UNLOCKED)
      
  def CLOSED_GRANTING_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_GRANTING_LOCKED", "timeout": 5000})
    if self.show_gui: self.v.set("CLOSED_GRANTING_LOCKED")
    self.log.debug("NEW STATE: CLOSED_GRANTING_LOCKED - ")
    self.ON_CLOSED_GRANTING_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 1./1000 * 5000:
        self.ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.CLOSED_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED_GRANTING_TIMEOUT":
        self.ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.CLOSED_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_OPENED":
        self.ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_SENSOR_OPENED()
        self.transition(self.OPEN_GRANTING_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_UNLOCKED":
        self.ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_UNLOCKED()
        self.transition(self.CLOSED_GRANTING_UNLOCKED)
      
  def OPEN_GRANTING_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_OPEN_GRANTING_LOCKED", "timeout": 1000})
    if self.show_gui: self.v.set("OPEN_GRANTING_LOCKED")
    self.log.debug("NEW STATE: OPEN_GRANTING_LOCKED - ")
    self.ON_OPEN_GRANTING_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 1./1000 * 1000:
        self.ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT()
        self.transition(self.OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_UNLOCKED":
        self.ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_UNLOCKED()
        self.transition(self.OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_OPEN_GRANTING_TIMEOUT":
        self.ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT()
        self.transition(self.OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_CLOSED":
        self.ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_SENSOR_CLOSED()
        self.transition(self.CLOSED_LOCKED)
      
  def OPEN_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_OPEN_LOCKED", "timeout": 15000})
    if self.show_gui: self.v.set("OPEN_LOCKED")
    self.log.debug("NEW STATE: OPEN_LOCKED - ")
    self.ON_OPEN_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 1./1000 * 15000:
        self.ON_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.STUCK_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_STUCK_TIMEOUT":
        self.ON_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.STUCK_OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_UNLOCKED":
        self.ON_OPEN_LOCKED_MAIN_DOOR_UNLOCKED()
        self.transition(self.OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_CLOSED":
        self.ON_OPEN_LOCKED_MAIN_DOOR_SENSOR_CLOSED()
        self.transition(self.CLOSED_LOCKED)
      
  def OPEN_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_OPEN_UNLOCKED", "timeout": 15000})
    if self.show_gui: self.v.set("OPEN_UNLOCKED")
    self.log.debug("NEW STATE: OPEN_UNLOCKED - ")
    self.ON_OPEN_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 1./1000 * 15000:
        self.ON_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.STUCK_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCKED":
        self.ON_OPEN_UNLOCKED_MAIN_DOOR_LOCKED()
        self.transition(self.OPEN_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_STUCK_TIMEOUT":
        self.ON_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT()
        self.transition(self.STUCK_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_CLOSED":
        self.ON_OPEN_UNLOCKED_MAIN_DOOR_SENSOR_CLOSED()
        self.transition(self.CLOSED_UNLOCKED)
      
  def CLOSED_GRANTING_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_GRANTING_UNLOCKED", "timeout": 5000})
    if self.show_gui: self.v.set("CLOSED_GRANTING_UNLOCKED")
    self.log.debug("NEW STATE: CLOSED_GRANTING_UNLOCKED - ")
    self.ON_CLOSED_GRANTING_UNLOCKED();

    # Wait for events
    while True:
      ev = yield

      if self.duration() > 1./1000 * 5000:
        self.ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.CLOSED_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_CLOSED_GRANTING_TIMEOUT":
        self.ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT()
        self.transition(self.CLOSED_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCKED":
        self.ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_LOCKED()
        self.transition(self.CLOSED_GRANTING_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_OPENED":
        self.ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_SENSOR_OPENED()
        self.transition(self.OPEN_UNLOCKED)
      
  def STUCK_OPEN_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_STUCK_OPEN_LOCKED"})
    if self.show_gui: self.v.set("STUCK_OPEN_LOCKED")
    self.log.debug("NEW STATE: STUCK_OPEN_LOCKED - ")
    self.ON_STUCK_OPEN_LOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "MAIN_DOOR_UNLOCKED":
        self.ON_STUCK_OPEN_LOCKED_MAIN_DOOR_UNLOCKED()
        self.transition(self.STUCK_OPEN_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_SENSOR_CLOSED":
        self.ON_STUCK_OPEN_LOCKED_MAIN_DOOR_SENSOR_CLOSED()
        self.transition(self.CLOSED_LOCKED)
      
  def STUCK_OPEN_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_STUCK_OPEN_UNLOCKED"})
    if self.show_gui: self.v.set("STUCK_OPEN_UNLOCKED")
    self.log.debug("NEW STATE: STUCK_OPEN_UNLOCKED - ")
    self.ON_STUCK_OPEN_UNLOCKED();

    # Wait for events
    while True:
      ev = yield
    
      if ev['event'] == "MAIN_DOOR_SENSOR_CLOSED":
        self.ON_STUCK_OPEN_UNLOCKED_MAIN_DOOR_SENSOR_CLOSED()
        self.transition(self.CLOSED_UNLOCKED)
      
      if ev['event'] == "MAIN_DOOR_LOCKED":
        self.ON_STUCK_OPEN_UNLOCKED_MAIN_DOOR_LOCKED()
        self.transition(self.STUCK_OPEN_LOCKED)
      
  def INVALID_KEY(self):
    """  """
    self.generate_message({"event": self.name + "_INVALID_KEY", "timeout": 2000})
    if self.show_gui: self.v.set("INVALID_KEY")
    self.log.debug("NEW STATE: INVALID_KEY - ")
    self.ON_INVALID_KEY();

    # Wait for events
    while True:
      ev = yield
    
      if self.duration() > 1./1000 * 2000:
        self.ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT()
        self.transition(self.CLOSED_LOCKED)
      
      if ev['event'] == "MAIN_DOOR_INVALID_TIMEOUT":
        self.ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT()
        self.transition(self.CLOSED_LOCKED)
      
  
  # By Default - do nothing ON_CLOSED_LOCKED
  def ON_CLOSED_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_INVALID_KEY(self):
    """ While in CLOSED_LOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_MAIN_DOOR_UNLOCKED(self):
    """ While in CLOSED_LOCKED, a MAIN_DOOR_UNLOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_VALID_KEY(self):
    """ While in CLOSED_LOCKED, a VALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_LOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_LOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_CLOSED_UNLOCKED
  def ON_CLOSED_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_INVALID_KEY(self):
    """ While in CLOSED_UNLOCKED, a INVALID_KEY message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_UNLOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_MAIN_DOOR_LOCKED(self):
    """ While in CLOSED_UNLOCKED, a MAIN_DOOR_LOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_UNLOCKED_VALID_KEY(self):
    """ While in CLOSED_UNLOCKED, a VALID_KEY message is recieved. """
    pass
      
  
  # By Default - do nothing ON_CLOSED_GRANTING_LOCKED
  def ON_CLOSED_GRANTING_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in CLOSED_GRANTING_LOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_GRANTING_LOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_LOCKED_MAIN_DOOR_UNLOCKED(self):
    """ While in CLOSED_GRANTING_LOCKED, a MAIN_DOOR_UNLOCKED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_OPEN_GRANTING_LOCKED
  def ON_OPEN_GRANTING_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_UNLOCKED(self):
    """ While in OPEN_GRANTING_LOCKED, a MAIN_DOOR_UNLOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_OPEN_GRANTING_TIMEOUT(self):
    """ While in OPEN_GRANTING_LOCKED, a MAIN_DOOR_OPEN_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_GRANTING_LOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in OPEN_GRANTING_LOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_OPEN_LOCKED
  def ON_OPEN_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_OPEN_LOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in OPEN_LOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_LOCKED_MAIN_DOOR_UNLOCKED(self):
    """ While in OPEN_LOCKED, a MAIN_DOOR_UNLOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_LOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in OPEN_LOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_OPEN_UNLOCKED
  def ON_OPEN_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_OPEN_UNLOCKED_MAIN_DOOR_LOCKED(self):
    """ While in OPEN_UNLOCKED, a MAIN_DOOR_LOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_UNLOCKED_MAIN_DOOR_STUCK_TIMEOUT(self):
    """ While in OPEN_UNLOCKED, a MAIN_DOOR_STUCK_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPEN_UNLOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in OPEN_UNLOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_CLOSED_GRANTING_UNLOCKED
  def ON_CLOSED_GRANTING_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_CLOSED_GRANTING_TIMEOUT(self):
    """ While in CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_CLOSED_GRANTING_TIMEOUT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_LOCKED(self):
    """ While in CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_LOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_GRANTING_UNLOCKED_MAIN_DOOR_SENSOR_OPENED(self):
    """ While in CLOSED_GRANTING_UNLOCKED, a MAIN_DOOR_SENSOR_OPENED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_STUCK_OPEN_LOCKED
  def ON_STUCK_OPEN_LOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_LOCKED_MAIN_DOOR_UNLOCKED(self):
    """ While in STUCK_OPEN_LOCKED, a MAIN_DOOR_UNLOCKED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_LOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in STUCK_OPEN_LOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_STUCK_OPEN_UNLOCKED
  def ON_STUCK_OPEN_UNLOCKED(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_UNLOCKED_MAIN_DOOR_SENSOR_CLOSED(self):
    """ While in STUCK_OPEN_UNLOCKED, a MAIN_DOOR_SENSOR_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_STUCK_OPEN_UNLOCKED_MAIN_DOOR_LOCKED(self):
    """ While in STUCK_OPEN_UNLOCKED, a MAIN_DOOR_LOCKED message is recieved. """
    pass
      
  
  # By Default - do nothing ON_INVALID_KEY
  def ON_INVALID_KEY(self):
    """  """
    pass

   
  # By default - do nothing during transitions
  def ON_INVALID_KEY_MAIN_DOOR_INVALID_TIMEOUT(self):
    """ While in INVALID_KEY, a MAIN_DOOR_INVALID_TIMEOUT message is recieved. """
    pass