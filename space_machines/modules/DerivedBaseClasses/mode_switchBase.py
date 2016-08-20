import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class mode_switchBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("mode_switchState")
    self.out_queue = out_queue
    self.name = name
              
  def transition(self, state_func, *state_args):
    currentState = self.current_state();
    self.logger.info("EXITING: " + currentState);
    if currentState == "UNLOCKED_MODE": self.ON_EXIT_UNLOCKED_MODE()
    elif currentState == "LOCKED_MODE": self.ON_EXIT_LOCKED_MODE()
    
    
    return super(mode_switchBase, self).transition(state_func, *state_args)              

               

  def UNLOCKED_MODE(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED_MODE"})
    if self.show_gui: self.v.set("UNLOCKED_MODE")
    self.log.debug("NEW STATE: UNLOCKED_MODE - ")
    self.ON_ENTER_UNLOCKED_MODE();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_UNLOCKED_MODE(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LOCKED_MODE" or ev['event'] == "REQUEST_MAIN_DOOR_LOCKED_MODE":
        self.ON_UNLOCKED_MODE_REQUEST_MAIN_DOOR_LOCKED_MODE()
        self.transition(self.LOCKED_MODE)
      
  def LOCKED_MODE(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED_MODE"})
    if self.show_gui: self.v.set("LOCKED_MODE")
    self.log.debug("NEW STATE: LOCKED_MODE - ")
    self.ON_ENTER_LOCKED_MODE();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_LOCKED_MODE(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_UNLOCKED_MODE" or ev['event'] == "REQUEST_MAIN_DOOR_UNLOCKED_MODE":
        self.ON_LOCKED_MODE_REQUEST_MAIN_DOOR_UNLOCKED_MODE()
        self.transition(self.UNLOCKED_MODE)
      

  # By default - Send a enter message ON_UNLOCKED_MODE
  def ON_ENTER_UNLOCKED_MODE(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED_MODE_ENTER"})

  # By Default - Send a exit message ON EXIT UNLOCKED_MODE
  def ON_EXIT_UNLOCKED_MODE(self):
    """  """
    self.generate_message({"event": self.name + "_UNLOCKED_MODE_EXIT"})

  # By Default - do nothing WHILE UNLOCKED_MODE
  def WHILE_UNLOCKED_MODE(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE UNLOCKED_MODE
  def ON_UNLOCKED_MODE_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_UNLOCKED_MODE_REQUEST_MAIN_DOOR_LOCKED_MODE(self):
    """ While in UNLOCKED_MODE, a REQUEST_MAIN_DOOR_LOCKED_MODE message is recieved. """
    pass
      

  # By default - Send a enter message ON_LOCKED_MODE
  def ON_ENTER_LOCKED_MODE(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED_MODE_ENTER"})

  # By Default - Send a exit message ON EXIT LOCKED_MODE
  def ON_EXIT_LOCKED_MODE(self):
    """  """
    self.generate_message({"event": self.name + "_LOCKED_MODE_EXIT"})

  # By Default - do nothing WHILE LOCKED_MODE
  def WHILE_LOCKED_MODE(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE LOCKED_MODE
  def ON_LOCKED_MODE_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_LOCKED_MODE_REQUEST_MAIN_DOOR_UNLOCKED_MODE(self):
    """ While in LOCKED_MODE, a REQUEST_MAIN_DOOR_UNLOCKED_MODE message is recieved. """
    pass