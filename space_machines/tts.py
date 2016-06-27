import logging
import time
import Queue
import threading
import os.path

import vlc
from gtts import gTTS
from Tkinter import *
from pystates import StateMachine


class TextToSpeech(StateMachine):
  def WAITING(self):
    while True:
      # no state transitions for this class, get key messages and send authorize messages
      ev = yield
      if ev['event'] == 'VALID_KEY':
        username = ev['username']
        self.v.set('Last username: {}'.format(username))
        if not os.path.isfile('./TTS/'+username+'.mp3'):
        	self.log.info('generating mp3...')
        	tts = gTTS(text='Welcome {}.'.format(username), lang='en')
        	tts.save(username+'.mp3')
        	if not os.path.exists('TTS'):
        		self.log.info('no TTS dir., creating one')
        		os.makedirs('TTS')
        	os.rename('./'+username+'.mp3', './TTS/'+username+'.mp3')
        player = vlc.MediaPlayer('./TTS/'+username+'.mp3')
        player.play()

        

  def setup(self, out_queue, name):
    self.log = logging.getLogger('TextToSpeech')
    self.out_queue = out_queue
    self.name = name

  def start(self):
    super(TextToSpeech, self).start(self.WAITING)

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
  name = 'TextToSpeech'
  machine = TextToSpeech(name=name)
  machine.setup(out_queue, name=name)
  machine.generate_message({'event': 'VALID_KEY', 'key': '', 'username': 'unknown'})
  machine.start()

  time.sleep(15)

if __name__=='__main__':
  main()
