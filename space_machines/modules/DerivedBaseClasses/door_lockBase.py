import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class door_lockBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("door_lockState")
    self.out_queue = out_queue
    self.name = name
              
  def transition(self, state_func, *state_args):
    currentState = self.current_state();
    self.logger.info("EXITING: " + currentState);
    if currentState == "UNLOCKED": self.ON_EXIT_UNLOCKED()
    elif currentState == "TEMP_UNLOCKED": self.ON_EXIT_TEMP_UNLOCKED()
    elif currentState == "TEMP_UNLOCKED_SPOOF": self.ON_EXIT_TEMP_UNLOCKED_SPOOF()
    elif currentState == "LOCKED": self.ON_EXIT_LOCKED()
    
    
    return super(door_lockBase, self).transition(state_func, *state_args)              

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)              

  def UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED"})
    if self.show_gui: self.v.set("UNLOCKED")
    self.log.debug("NEW STATE: UNLOCKED - ")
    self.ON_ENTER_UNLOCKED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_UNLOCKED(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LOCK" or ev['event'] == "REQUEST_MAIN_DOOR_LOCK":
        self.ON_UNLOCKED_REQUEST_MAIN_DOOR_LOCK()
        self.transition(self.LOCKED)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_TEMP_UNLOCK" or ev['event'] == "REQUEST_MAIN_DOOR_TEMP_UNLOCK":
        self.ON_UNLOCKED_REQUEST_MAIN_DOOR_TEMP_UNLOCK()
        self.transition(self.TEMP_UNLOCKED_SPOOF)
      
  def TEMP_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED", "timeout": 5000})
    if self.show_gui: self.v.set("TEMP_UNLOCKED")
    self.log.debug("NEW STATE: TEMP_UNLOCKED - ")
    self.ON_ENTER_TEMP_UNLOCKED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_TEMP_UNLOCKED(ev)
      
    
      if (self.duration() * 1000) >= 5000:
        self.ON_TEMP_UNLOCKED_TIMEOUT(ev)
        self.generate_message({"event": "REQUEST_MAIN_DOOR_LOCK"})
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LOCK" or ev['event'] == "REQUEST_MAIN_DOOR_LOCK":
        self.ON_TEMP_UNLOCKED_REQUEST_MAIN_DOOR_LOCK()
        self.transition(self.LOCKED)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_UNLOCK" or ev['event'] == "REQUEST_MAIN_DOOR_UNLOCK":
        self.ON_TEMP_UNLOCKED_REQUEST_MAIN_DOOR_UNLOCK()
        self.transition(self.UNLOCKED)
      
  def TEMP_UNLOCKED_SPOOF(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED_SPOOF", "timeout": 5000})
    if self.show_gui: self.v.set("TEMP_UNLOCKED_SPOOF")
    self.log.debug("NEW STATE: TEMP_UNLOCKED_SPOOF - ")
    self.ON_ENTER_TEMP_UNLOCKED_SPOOF();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_TEMP_UNLOCKED_SPOOF(ev)
      
    
      if (self.duration() * 1000) >= 5000:
        self.ON_TEMP_UNLOCKED_SPOOF_TIMEOUT(ev)
        self.generate_message({"event": "REQUEST_MAIN_DOOR_UNLOCK"})
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_UNLOCK" or ev['event'] == "REQUEST_MAIN_DOOR_UNLOCK":
        self.ON_TEMP_UNLOCKED_SPOOF_REQUEST_MAIN_DOOR_UNLOCK()
        self.transition(self.UNLOCKED)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LOCK" or ev['event'] == "REQUEST_MAIN_DOOR_LOCK":
        self.ON_TEMP_UNLOCKED_SPOOF_REQUEST_MAIN_DOOR_LOCK()
        self.transition(self.LOCKED)
      
  def LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED"})
    if self.show_gui: self.v.set("LOCKED")
    self.log.debug("NEW STATE: LOCKED - ")
    self.ON_ENTER_LOCKED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_LOCKED(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_TEMP_UNLOCK" or ev['event'] == "REQUEST_MAIN_DOOR_TEMP_UNLOCK":
        self.ON_LOCKED_REQUEST_MAIN_DOOR_TEMP_UNLOCK()
        self.transition(self.TEMP_UNLOCKED)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_UNLOCK" or ev['event'] == "REQUEST_MAIN_DOOR_UNLOCK":
        self.ON_LOCKED_REQUEST_MAIN_DOOR_UNLOCK()
        self.transition(self.UNLOCKED)
      

  # By default - Send a enter message ON_UNLOCKED
  def ON_ENTER_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED_ENTER"})

  # By Default - Send a exit message ON EXIT UNLOCKED
  def ON_EXIT_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED_EXIT"})

  # By Default - do nothing WHILE UNLOCKED
  def WHILE_UNLOCKED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE UNLOCKED
  def ON_UNLOCKED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_UNLOCKED_REQUEST_MAIN_DOOR_LOCK(self):
    """ While in UNLOCKED, a REQUEST_MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_UNLOCKED_REQUEST_MAIN_DOOR_TEMP_UNLOCK(self):
    """ While in UNLOCKED, a REQUEST_MAIN_DOOR_TEMP_UNLOCK message is recieved. """
    pass
      

  # By default - Send a enter message ON_TEMP_UNLOCKED
  def ON_ENTER_TEMP_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED_ENTER"})

  # By Default - Send a exit message ON EXIT TEMP_UNLOCKED
  def ON_EXIT_TEMP_UNLOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED_EXIT"})

  # By Default - do nothing WHILE TEMP_UNLOCKED
  def WHILE_TEMP_UNLOCKED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE TEMP_UNLOCKED
  def ON_TEMP_UNLOCKED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_TEMP_UNLOCKED_REQUEST_MAIN_DOOR_LOCK(self):
    """ While in TEMP_UNLOCKED, a REQUEST_MAIN_DOOR_LOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_TEMP_UNLOCKED_REQUEST_MAIN_DOOR_UNLOCK(self):
    """ While in TEMP_UNLOCKED, a REQUEST_MAIN_DOOR_UNLOCK message is recieved. """
    pass
      

  # By default - Send a enter message ON_TEMP_UNLOCKED_SPOOF
  def ON_ENTER_TEMP_UNLOCKED_SPOOF(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED_SPOOF_ENTER"})

  # By Default - Send a exit message ON EXIT TEMP_UNLOCKED_SPOOF
  def ON_EXIT_TEMP_UNLOCKED_SPOOF(self):
    """  """
    self.generate_message({"event": self.name + "_TEMP_UNLOCKED_SPOOF_EXIT"})

  # By Default - do nothing WHILE TEMP_UNLOCKED_SPOOF
  def WHILE_TEMP_UNLOCKED_SPOOF(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE TEMP_UNLOCKED_SPOOF
  def ON_TEMP_UNLOCKED_SPOOF_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_TEMP_UNLOCKED_SPOOF_REQUEST_MAIN_DOOR_UNLOCK(self):
    """ While in TEMP_UNLOCKED_SPOOF, a REQUEST_MAIN_DOOR_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_TEMP_UNLOCKED_SPOOF_REQUEST_MAIN_DOOR_LOCK(self):
    """ While in TEMP_UNLOCKED_SPOOF, a REQUEST_MAIN_DOOR_LOCK message is recieved. """
    pass
      

  # By default - Send a enter message ON_LOCKED
  def ON_ENTER_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED_ENTER"})

  # By Default - Send a exit message ON EXIT LOCKED
  def ON_EXIT_LOCKED(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED_EXIT"})

  # By Default - do nothing WHILE LOCKED
  def WHILE_LOCKED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE LOCKED
  def ON_LOCKED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_LOCKED_REQUEST_MAIN_DOOR_TEMP_UNLOCK(self):
    """ While in LOCKED, a REQUEST_MAIN_DOOR_TEMP_UNLOCK message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_LOCKED_REQUEST_MAIN_DOOR_UNLOCK(self):
    """ While in LOCKED, a REQUEST_MAIN_DOOR_UNLOCK message is recieved. """
    pass