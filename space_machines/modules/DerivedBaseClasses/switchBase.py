import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

class SwitchBase(StateMachine): #MOCK UP --- NOT ACTUALLY DERIVED

  def ON(self):
    self.logger.debug(self.name + " switch is on ")
    self.logger.debug("generating message: " + self.on_message)
    self.generate_message({"event": self.on_message})
    if self.show_gui: self.v.set("ON")
    self.ON_ON()
    while True:
      self.WHILE_ON()
      ev = yield
      if ev['event'] == self.name + '_TURN_OFF':
        self.transition(self.OFF)

  def OFF(self):
    self.logger.debug(self.name + " switch is off")
    self.logger.debug("generating message: " + self.off_message)
    self.generate_message({"event": self.off_message})
    if self.show_gui: self.v.set("OFF")
    self.ON_OFF()
    while True:
      self.WHILE_OFF()
      ev = yield
      if ev['event'] == self.name + '_TURN_ON':
        self.transition(self.ON)

  def WHILE_OFF(self):
    pass

  def WHILE_ON(self):
    pass

  def ON_ON(self):
    pass

  def ON_OFF(self):
    pass

  def setup(self, out_queue, name, on_message, off_message):
    self.logger = logging.getLogger(name + "_Switch")
    self.out_queue = out_queue
    self.name = name
    self.on_message = on_message
    self.off_message = off_message

  def config_gui(self, root):
    self.show_gui = True
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("UNKNOWN")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)