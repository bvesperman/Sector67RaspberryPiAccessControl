import logging
import os.path
import vlc
from gtts import gTTS


class TextToSpeech():
  def __init__(self):
    self.log = logging.getLogger('TTS')
  def say(self, text='', fname='tts_temp', location=os.curdir, lang='en', remove=True):
    fpath = os.path.join(location,fname+'.mp3')
    if not os.path.isfile(fpath):
      self.log.info('file '+fname+'.mp3 not in '+location+', creating file')
      tts = gTTS(text=text, lang=lang)
      tts.save(fname+'.mp3')
      self.log.info(fname+'.mp3 created')
      if not os.path.exists(location):
        self.log.info('no {0} dir; creating dir'.format(location))
        os.makedirs(location)
      os.rename(fname+'.mp3', fpath)
      self.log.info(fname+'.mp3 moved to '+location)
    else:
      self.log.info("playing existing '"+fname+".mp3' in "+location)
    player = vlc.MediaPlayer(fpath)
    player.play()
    if remove:
      os.remove(fpath)
      self.log.info('removed'+fpath)