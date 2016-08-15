import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

class GuiSwitch(StateMachine):

  def ON(self):
    self.logger.debug(self.name + " switch is on ")
    self.logger.debug("generating message: " + self.on_message)
    self.generate_message({"event": self.on_message})
    while True:
      self.WHILE_ON()
      ev = yield
      if ev['event'] == self.name + '_TURN_OFF':
        self.transition(self.OFF)

  def OFF(self):
    self.logger.debug(self.name + " switch is off")
    self.logger.debug("generating message: " + self.off_message)
    self.generate_message({"event": self.off_message})
    while True:
      self.WHILE_OFF()
      ev = yield
      if ev['event'] == self.name + '_TURN_ON':
        self.transition(self.ON)

  def WHILE_OFF(self):
    if self.state.get():
      self.generate_message({"event": self.name + '_TURN_ON'})

  def WHILE_ON(self):
    if not self.state.get():
      self.generate_message({"event": self.name + '_TURN_OFF'})

  def setup(self, out_queue, name, on_message, off_message, selected=False, checkbutton_text="ON/OFF"):
    self.logger = logging.getLogger("GuiSwitch")
    self.out_queue = out_queue
    self.name = name
    self.on_message = on_message
    self.off_message = off_message
    self.selected = bool(selected)
    self.checkbutton_text = checkbutton_text


  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    #TODO: actually detect the starting state here
    self.logger.debug("initial state: " + self.off_message)
    self.generate_message({"event": self.off_message})
    super(GuiSwitch, self).start(self.OFF)

  def config_gui(self, root):
    self.show_gui = True
    # Set up the GUI part
    self.state = IntVar()
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    c = Checkbutton(frame, text=self.checkbutton_text, variable=self.state)
    if self.selected:
      c.select()
    c.pack(side=LEFT)


