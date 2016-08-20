import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class solenoidBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("solenoidState")
    self.out_queue = out_queue
    self.name = name
              
  def transition(self, state_func, *state_args):
    currentState = self.current_state();
    self.logger.info("EXITING: " + currentState);
    if currentState == "EXTENDED": self.ON_EXIT_EXTENDED()
    elif currentState == "RETRACTED": self.ON_EXIT_RETRACTED()
    
    
    return super(solenoidBase, self).transition(state_func, *state_args)              

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)           

  def EXTENDED(self):
    """  """
    self.generate_message({"event": self.name + "_EXTENDED"})
    if self.show_gui: self.v.set("EXTENDED")
    self.log.debug("NEW STATE: EXTENDED - ")
    self.ON_ENTER_EXTENDED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_EXTENDED(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_SOLENOID_RETRACT" or ev['event'] == "REQUEST_MAIN_DOOR_SOLENOID_RETRACT":
        self.ON_EXTENDED_REQUEST_MAIN_DOOR_SOLENOID_RETRACT()
        self.transition(self.RETRACTED)
      
  def RETRACTED(self):
    """  """
    self.generate_message({"event": self.name + "_RETRACTED"})
    if self.show_gui: self.v.set("RETRACTED")
    self.log.debug("NEW STATE: RETRACTED - ")
    self.ON_ENTER_RETRACTED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_RETRACTED(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_SOLENOID_EXTEND" or ev['event'] == "REQUEST_MAIN_DOOR_SOLENOID_EXTEND":
        self.ON_RETRACTED_REQUEST_MAIN_DOOR_SOLENOID_EXTEND()
        self.transition(self.EXTENDED)
      

  # By default - Send a enter message ON_EXTENDED
  def ON_ENTER_EXTENDED(self):
    """  """
    self.generate_message({"event": self.name + "_EXTENDED_ENTER"})

  # By Default - Send a exit message ON EXIT EXTENDED
  def ON_EXIT_EXTENDED(self):
    """  """
    self.generate_message({"event": self.name + "_EXTENDED_EXIT"})

  # By Default - do nothing WHILE EXTENDED
  def WHILE_EXTENDED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE EXTENDED
  def ON_EXTENDED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_EXTENDED_REQUEST_MAIN_DOOR_SOLENOID_RETRACT(self):
    """ While in EXTENDED, a REQUEST_MAIN_DOOR_SOLENOID_RETRACT message is recieved. """
    pass
      

  # By default - Send a enter message ON_RETRACTED
  def ON_ENTER_RETRACTED(self):
    """  """
    self.generate_message({"event": self.name + "_RETRACTED_ENTER"})

  # By Default - Send a exit message ON EXIT RETRACTED
  def ON_EXIT_RETRACTED(self):
    """  """
    self.generate_message({"event": self.name + "_RETRACTED_EXIT"})

  # By Default - do nothing WHILE RETRACTED
  def WHILE_RETRACTED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE RETRACTED
  def ON_RETRACTED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_RETRACTED_REQUEST_MAIN_DOOR_SOLENOID_EXTEND(self):
    """ While in RETRACTED, a REQUEST_MAIN_DOOR_SOLENOID_EXTEND message is recieved. """
    pass