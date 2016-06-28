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
        username = [ev['username'], ev['username'].replace(' ', '_')]
        self.v.set('Last username: {}'.format(username[0]))
        greeting = TextToSpeech()
        greeting.say(text='Welcome {}.'.format(username[0]), fname=username[1], location='usergreetings', remove=False)

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
    self.v = StringVar()
    self.v.set('')
    w = Label(frame, textvariable=self.v)
    w.pack(side=LEFT)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = 'Greeter'
  machine = Greeter(name=name)
  machine.setup(out_queue, name=name)
  machine.generate_message({'event': 'VALID_KEY', 'key': '', 'username': 'unknown'})
  machine.start()

  time.sleep(15)

if __name__=='__main__':
  main()
