import logging
import time
import Queue
import threading

from Tkinter import *

from pystates import StateMachine

class NaiveAuthorizer(StateMachine):

  def WAITING(self):
    while True:
      # no state transitions for this class, get key messages and send authorize messages
      ev = yield
      if ev['event'] == "KEY_READ":
        key = ev['key']
        username = "unknown"
        self.log.debug('attempting to authorize key [' + key + ']')
        isvalid = True
        if isvalid:
            message = {"event": "VALID_KEY", "key": key, "username": username}
            self.logger.debug("generating message: " + str(message))
            self.generate_message(message)
        else:
            message = {"event": "INVALID_KEY", "key": key, "username": username}
            self.logger.debug("generating message: " + str(message))
            self.generate_message(message)

  def setup(self, out_queue, name):
    self.log = logging.getLogger("NaiveAuthorizer")
    self.out_queue = out_queue
    self.name = name

  def start(self):
    super(NaiveAuthorizer, self).start(self.WAITING)

  def config_gui(self, root):
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.v = StringVar()
    self.v.set("AUTHORIZER")
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "NAIVE_AUTHORIZER"
  machine = NaiveAuthorizer(name=name)
  machine.setup(out_queue, name=name)
  machine.start()

  time.sleep(15)

if __name__=='__main__':
  main()
