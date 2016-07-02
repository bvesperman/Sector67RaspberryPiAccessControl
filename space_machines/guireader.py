import logging
import time
import Queue
import threading

from Tkinter import *


from pystates import StateMachine

class GuiRfidReader(StateMachine):

  def READING(self):
    while True:
      # no state transitions for this class, read keys and send messages
      ev = yield

  def setup(self, out_queue, name):
    self.log = logging.getLogger("GuiRfidReader")
    self.out_queue = out_queue
    self.name = name

  """ Perform initialization here, detect the current state and send that
      to the super class start.
  """
  def start(self):
    super(GuiRfidReader, self).start(self.READING)

  def config_gui(self, root):
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.e = Entry(frame)
    self.e.pack(side=LEFT)
    b = Button(frame, text="read", width=10, command=self.read)
    b.pack(side=LEFT)

  def read(self):
    key = int(self.e.get().strip())
    message = {"event": "KEY_READ", "key": key}
    self.logger.debug("generating message: " + str(message))
    self.generate_message(message)
