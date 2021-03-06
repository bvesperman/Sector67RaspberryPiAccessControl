import logging
import time
import Queue

from Tkinter import *
from pystates import StateMachine
from tts import TextToSpeech


class Greeter(StateMachine):
  def WAITING(self):
    while True:
      # no state transitions for this class, get key messages and send authorize messages
      ev = yield
      if ev['event'] == 'VALID_KEY':
        self.display_name = ev['display_name'] or 'to sector 67'#--default message: 'Welcome to sector 67.'
        self.user_login = ev['user_login'] or self.display_name
        self.m.set("'Welcome {0}.'".format(self.display_name))
        self.greeting = TextToSpeech()
        self.greeting.say(text='Welcome {0}.'.format(self.display_name), fname=self.user_login, location='usergreetings', remove=False)

  def setup(self, out_queue, name):
    self.log = logging.getLogger('Greeter')
    self.out_queue = out_queue
    self.name = name

  def start(self):
    super(Greeter, self).start(self.WAITING)

  def config_gui(self, root):
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.m = StringVar()
    self.m.set('')
    lm1 = Label(frame, text="message:")
    lm1.pack(side=LEFT)
    lm2 = Label(frame, textvariable=self.m)
    lm2.pack(side=LEFT)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = 'Greeter'
  machine = Greeter(name=name)
  machine.setup(out_queue, name=name)
  machine.generate_message({'event': 'VALID_KEY', 'key': '', 'display_name': 'unknown'})
  machine.start()

  time.sleep(15)

if __name__=='__main__':
  main()
