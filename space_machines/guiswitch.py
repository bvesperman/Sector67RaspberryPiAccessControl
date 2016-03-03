import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

class GuiSwitch(StateMachine):

  def ON(self):
    self.logger.debug(self.name + " switch is on ")
    while True:
      ev = yield
      state = self.state.get()
      if state == 0:
        self.logger.debug("generating message: " + self.off_message)
        self.generate_message({"event": self.off_message})
        self.transition(self.OFF)

  def OFF(self):
    self.logger.debug(self.name + " switch is off")
    while True:
      ev = yield
      state = self.state.get()
      if state == 1:
        self.logger.debug("generating message: " + self.on_message)
        self.generate_message({"event": self.on_message})
        self.transition(self.ON)

  def setup(self, out_queue, name, on_message, off_message):
    self.logger = logging.getLogger("GuiSwitch")
    self.out_queue = out_queue
    self.name = name
    self.on_message = on_message
    self.off_message = off_message


  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    #TODO: actually detect the starting state here
    self.logger.debug("initial state: " + self.off_message)
    self.generate_message({"event": self.off_message})
    super(GuiSwitch, self).start(self.OFF)

  def config_gui(self, root):
    # Set up the GUI part
    self.state = IntVar()
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    c = Checkbutton(frame, text="Switch", variable=self.state)
    c.pack(side=LEFT)


