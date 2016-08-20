import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class open_switchBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("open_switchState")
    self.out_queue = out_queue
    self.name = name
              
  def transition(self, state_func, *state_args):
    currentState = self.current_state();
    self.logger.info("EXITING: " + currentState);
    if currentState == "OPEN": self.ON_EXIT_OPEN()
    elif currentState == "CLOSED": self.ON_EXIT_CLOSED()
    
    
    return super(open_switchBase, self).transition(state_func, *state_args)              

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)    

  def OPEN(self):
    """  """
    self.generate_message({"event": self.name + "_OPEN"})
    if self.show_gui: self.v.set("OPEN")
    self.log.debug("NEW STATE: OPEN - ")
    self.ON_ENTER_OPEN();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_OPEN(ev)
      
    
      if ev['event'] == self.name + "_DETECTED_MAIN_DOOR_CLOSED" or ev['event'] == "DETECTED_MAIN_DOOR_CLOSED":
        self.ON_OPEN_DETECTED_MAIN_DOOR_CLOSED()
        self.transition(self.CLOSED)
      
  def CLOSED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED"})
    if self.show_gui: self.v.set("CLOSED")
    self.log.debug("NEW STATE: CLOSED - ")
    self.ON_ENTER_CLOSED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_CLOSED(ev)
      
    
      if ev['event'] == self.name + "_DETECTED_MAIN_DOOR_OPENED" or ev['event'] == "DETECTED_MAIN_DOOR_OPENED":
        self.ON_CLOSED_DETECTED_MAIN_DOOR_OPENED()
        self.transition(self.OPEN)
      

  # By default - Send a enter message ON_OPEN
  def ON_ENTER_OPEN(self):
    """  """
    self.generate_message({"event": self.name + "_OPEN_ENTER"})

  # By Default - Send a exit message ON EXIT OPEN
  def ON_EXIT_OPEN(self):
    """  """
    self.generate_message({"event": self.name + "_OPEN_EXIT"})

  # By Default - do nothing WHILE OPEN
  def WHILE_OPEN(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE OPEN
  def ON_OPEN_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_OPEN_DETECTED_MAIN_DOOR_CLOSED(self):
    """ While in OPEN, a DETECTED_MAIN_DOOR_CLOSED message is recieved. """
    pass
      

  # By default - Send a enter message ON_CLOSED
  def ON_ENTER_CLOSED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_ENTER"})

  # By Default - Send a exit message ON EXIT CLOSED
  def ON_EXIT_CLOSED(self):
    """  """
    self.generate_message({"event": self.name + "_CLOSED_EXIT"})

  # By Default - do nothing WHILE CLOSED
  def WHILE_CLOSED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE CLOSED
  def ON_CLOSED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_CLOSED_DETECTED_MAIN_DOOR_OPENED(self):
    """ While in CLOSED, a DETECTED_MAIN_DOOR_OPENED message is recieved. """
    pass