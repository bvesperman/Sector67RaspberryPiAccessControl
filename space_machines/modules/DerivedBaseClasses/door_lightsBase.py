import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

from abc import ABCMeta, abstractmethod

class door_lightsBase(StateMachine):
  __metaclass__ = ABCMeta
  """description of class"""
  
  
              
 
  def setup(self, out_queue, name):
    self.log = logging.getLogger("door_lightsState")
    self.out_queue = out_queue
    self.name = name
              
  def transition(self, state_func, *state_args):
    currentState = self.current_state();
    self.logger.info("EXITING: " + currentState);
    if currentState == "REJECTING": self.ON_EXIT_REJECTING()
    elif currentState == "GRANTING": self.ON_EXIT_GRANTING()
    elif currentState == "OPENED": self.ON_EXIT_OPENED()
    elif currentState == "STUCK": self.ON_EXIT_STUCK()
    elif currentState == "CLOSED": self.ON_EXIT_CLOSED()
    
    
    return super(door_lightsBase, self).transition(state_func, *state_args)              

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)            

  def REJECTING(self):
    """  """
    self.generate_message({"event": self.name + "_REJECTING", "timeout": 2000})
    if self.show_gui: self.v.set("REJECTING")
    self.log.debug("NEW STATE: REJECTING - ")
    self.ON_ENTER_REJECTING();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_REJECTING(ev)
      
    
      if (self.duration() * 1000) >= 2000:
        self.ON_REJECTING_TIMEOUT(ev)
        self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_CLOSED"})
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_CLOSED" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_CLOSED":
        self.ON_REJECTING_REQUEST_MAIN_DOOR_LIGHTS_CLOSED()
        self.transition(self.CLOSED)
      
  def GRANTING(self):
    """  """
    self.generate_message({"event": self.name + "_GRANTING", "timeout": 5000})
    if self.show_gui: self.v.set("GRANTING")
    self.log.debug("NEW STATE: GRANTING - ")
    self.ON_ENTER_GRANTING();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_GRANTING(ev)
      
    
      if (self.duration() * 1000) >= 5000:
        self.ON_GRANTING_TIMEOUT(ev)
        self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_CLOSED"})
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_CLOSED" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_CLOSED":
        self.ON_GRANTING_REQUEST_MAIN_DOOR_LIGHTS_CLOSED()
        self.transition(self.CLOSED)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_OPENED" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_OPENED":
        self.ON_GRANTING_REQUEST_MAIN_DOOR_LIGHTS_OPENED()
        self.transition(self.OPENED)
      
  def OPENED(self):
    """  """
    self.generate_message({"event": self.name + "_OPENED", "timeout": 15})
    if self.show_gui: self.v.set("OPENED")
    self.log.debug("NEW STATE: OPENED - ")
    self.ON_ENTER_OPENED();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_OPENED(ev)
      
    
      if (self.duration() * 1000) >= self.stuck_timeout:
        self.ON_OPENED_TIMEOUT(ev)
        self.generate_message({"event": "REQUEST_MAIN_DOOR_LIGHTS_STUCK"})
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_CLOSED" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_CLOSED":
        self.ON_OPENED_REQUEST_MAIN_DOOR_LIGHTS_CLOSED()
        self.transition(self.CLOSED)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_STUCK" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_STUCK":
        self.ON_OPENED_REQUEST_MAIN_DOOR_LIGHTS_STUCK()
        self.transition(self.STUCK)
      
  def STUCK(self):
    """  """
    self.generate_message({"event": self.name + "_STUCK"})
    if self.show_gui: self.v.set("STUCK")
    self.log.debug("NEW STATE: STUCK - ")
    self.ON_ENTER_STUCK();
    
    # Wait for events
    while True:
      ev = yield
      
      self.WHILE_STUCK(ev)
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_CLOSED" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_CLOSED":
        self.ON_STUCK_REQUEST_MAIN_DOOR_LIGHTS_CLOSED()
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
      
    
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_GRANT" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_GRANT":
        self.ON_CLOSED_REQUEST_MAIN_DOOR_LIGHTS_GRANT()
        self.transition(self.GRANTING)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_REJECT" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_REJECT":
        self.ON_CLOSED_REQUEST_MAIN_DOOR_LIGHTS_REJECT()
        self.transition(self.REJECTING)
      
      if ev['event'] == self.name + "_REQUEST_MAIN_DOOR_LIGHTS_OPENED" or ev['event'] == "REQUEST_MAIN_DOOR_LIGHTS_OPENED":
        self.ON_CLOSED_REQUEST_MAIN_DOOR_LIGHTS_OPENED()
        self.transition(self.OPENED)
      

  # By default - Send a enter message ON_REJECTING
  def ON_ENTER_REJECTING(self):
    """  """
    self.generate_message({"event": self.name + "_REJECTING_ENTER"})

  # By Default - Send a exit message ON EXIT REJECTING
  def ON_EXIT_REJECTING(self):
    """  """
    self.generate_message({"event": self.name + "_REJECTING_EXIT"})

  # By Default - do nothing WHILE REJECTING
  def WHILE_REJECTING(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE REJECTING
  def ON_REJECTING_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_REJECTING_REQUEST_MAIN_DOOR_LIGHTS_CLOSED(self):
    """ While in REJECTING, a REQUEST_MAIN_DOOR_LIGHTS_CLOSED message is recieved. """
    pass
      

  # By default - Send a enter message ON_GRANTING
  def ON_ENTER_GRANTING(self):
    """  """
    self.generate_message({"event": self.name + "_GRANTING_ENTER"})

  # By Default - Send a exit message ON EXIT GRANTING
  def ON_EXIT_GRANTING(self):
    """  """
    self.generate_message({"event": self.name + "_GRANTING_EXIT"})

  # By Default - do nothing WHILE GRANTING
  def WHILE_GRANTING(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE GRANTING
  def ON_GRANTING_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_GRANTING_REQUEST_MAIN_DOOR_LIGHTS_CLOSED(self):
    """ While in GRANTING, a REQUEST_MAIN_DOOR_LIGHTS_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_GRANTING_REQUEST_MAIN_DOOR_LIGHTS_OPENED(self):
    """ While in GRANTING, a REQUEST_MAIN_DOOR_LIGHTS_OPENED message is recieved. """
    pass
      

  # By default - Send a enter message ON_OPENED
  def ON_ENTER_OPENED(self):
    """  """
    self.generate_message({"event": self.name + "_OPENED_ENTER"})

  # By Default - Send a exit message ON EXIT OPENED
  def ON_EXIT_OPENED(self):
    """  """
    self.generate_message({"event": self.name + "_OPENED_EXIT"})

  # By Default - do nothing WHILE OPENED
  def WHILE_OPENED(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE OPENED
  def ON_OPENED_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_OPENED_REQUEST_MAIN_DOOR_LIGHTS_CLOSED(self):
    """ While in OPENED, a REQUEST_MAIN_DOOR_LIGHTS_CLOSED message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_OPENED_REQUEST_MAIN_DOOR_LIGHTS_STUCK(self):
    """ While in OPENED, a REQUEST_MAIN_DOOR_LIGHTS_STUCK message is recieved. """
    pass
      

  # By default - Send a enter message ON_STUCK
  def ON_ENTER_STUCK(self):
    """  """
    self.generate_message({"event": self.name + "_STUCK_ENTER"})

  # By Default - Send a exit message ON EXIT STUCK
  def ON_EXIT_STUCK(self):
    """  """
    self.generate_message({"event": self.name + "_STUCK_EXIT"})

  # By Default - do nothing WHILE STUCK
  def WHILE_STUCK(self, ev):
    """  """
    pass

  # By Default - do nothing WHILE STUCK
  def ON_STUCK_TIMEOUT(self, ev):
    """  """

  
  # By default - do nothing during transitions
  def ON_STUCK_REQUEST_MAIN_DOOR_LIGHTS_CLOSED(self):
    """ While in STUCK, a REQUEST_MAIN_DOOR_LIGHTS_CLOSED message is recieved. """
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
  def ON_CLOSED_REQUEST_MAIN_DOOR_LIGHTS_GRANT(self):
    """ While in CLOSED, a REQUEST_MAIN_DOOR_LIGHTS_GRANT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_REQUEST_MAIN_DOOR_LIGHTS_REJECT(self):
    """ While in CLOSED, a REQUEST_MAIN_DOOR_LIGHTS_REJECT message is recieved. """
    pass
      
  # By default - do nothing during transitions
  def ON_CLOSED_REQUEST_MAIN_DOOR_LIGHTS_OPENED(self):
    """ While in CLOSED, a REQUEST_MAIN_DOOR_LIGHTS_OPENED message is recieved. """
    pass