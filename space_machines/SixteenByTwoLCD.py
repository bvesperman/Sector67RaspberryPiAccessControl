import logging
import time
import Queue

from Tkinter import *

from pystates import StateMachine

class SixteenByTwoLCDState(StateMachine):
    def BUTTONPUSH(self):
        i = 0

    def WRITEMESSAGE(self):
        i =0


    def start(self):
        # assume a starting state of IDLE and appropriate messages will send it to the correct state
        super(SixteenByTwoLCDState, self).start(self.WRITEMESSAGE)

    def setup(self, out_queue, name):
        self.log = logging.getLogger("SixteenByTwoLCDState")
        self.out_queue = out_queue
        self.name = name

    """ Perform initialization here, detect the current state and send that
      to the super class start.
    """


    def config_gui(self, root):
        self.show_gui = True
        # Set up the GUI part
        frame = LabelFrame(root, text=self.name, padx=5, pady=5)
        frame.pack(fill=X)
        self.v = StringVar()
        self.v.set("UNKNOWN")
        w = Label(frame, textvariable=self.v)
        w.pack(side=LEFT)