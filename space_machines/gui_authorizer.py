import logging
import time
import Queue
import threading

test_keys = {
  7899246 : {"status":"ok","message":{"user_login":"JSmith","ID":"89076543","display_name":"Johnny","account_balance":"12.78"}},# format that the url responds with
  #"" : {"status":"ok","message":{"user_login":"","ID":"","display_name":"","account_balance":""}},
  #"" : {"status":"ok","message":{"user_login":"","ID":"","display_name":"","account_balance":""}},
  #"" : {"status":"ok","message":{"user_login":"","ID":"","display_name":"","account_balance":""}},
  #"" : {"status":"ok","message":{"user_login":"","ID":"","display_name":"","account_balance":""}},
  #"" : {"status":"ok","message":{"user_login":"","ID":"","display_name":"","account_balance":""}},
  #"" : {"status":"ok","message":{"user_login":"","ID":"","display_name":"","account_balance":""}},
}

from Tkinter import *

from pystates import StateMachine

class GuiAuthorizer(StateMachine):

  #self explanatory, really. Useful only for displaying the username or account information, not for regular authorization checking.
  def getUserByRFID(self, key): 
    try:
      response = test_keys[key]
      return response  #result
    except Exception as e:
      self.log.info("Error encountered during authorization {0}".format(str(e)))
      return {"status": "error"}

  #does this RFID user have access to this machine? Binary result, and we really don't care why it failed.
  def isRFIDAuthorized(self, key):
    if self.isvalid.get():
      return True
    else:
      return False

  def WAITING(self):
    while True:
      # no state transitions for this class, get key messages and send authorize messages
      ev = yield
      if ev['event'] == "KEY_READ":
        key = ev['key']
        user_login = ''
        id = ''
        display_name = ''
        account_balance = ''
        self.log.debug("attempting to authorize key [{0}]".format(key))
        userdata = self.getUserByRFID(key)
        if "message" in userdata:
          if "user_login" in userdata["message"]:
            user_login = str(userdata["message"]["user_login"]) 
          if "ID" in userdata["message"]:
            id = str(userdata["message"]["ID"]) 
          if "display_name" in userdata["message"]:
            display_name = str(userdata["message"]["display_name"]) 
          if "account_balance" in userdata["message"]:
            account_balance = str(userdata["message"]["account_balance"]) 
        is_authorized = self.isRFIDAuthorized(key)
        if is_authorized:
          self.log.info("key [{0}] was authorized as user [".format(key) + user_login + "]")
          message = {"event": "VALID_KEY", "key": key, "user_login": user_login, "id": id, "display_name": display_name, "account_balance": account_balance}
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)
        else:
          self.log.info("key [" + key + "] was not authorized as user [" + user_login + "]")
          message = {"event": "INVALID_KEY", "key": key, "user_login": user_login, "id": id, "display_name": display_name, "account_balance": account_balance}
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)

  def setup(self, out_queue, name, machine_id):
    self.log = logging.getLogger("GuiAuthorizer")
    self.out_queue = out_queue
    self.name = name
    self.machine_id = machine_id
    

  def start(self):
    super(GuiAuthorizer, self).start(self.WAITING)

  def config_gui(self, root):
    # Set up the GUI part
    frame = LabelFrame(root, text=self.name, padx=5, pady=5)
    frame.pack(fill=X)
    self.isvalid = IntVar()
    c = Checkbutton(frame, text='isvalid', variable=self.isvalid)
    c.select()
    c.pack(side=LEFT)

def main():
  out_queue = Queue.Queue()
  logging.basicConfig(level=logging.DEBUG)
  name = "GUI_AUTHORIZER"
  machine = GuiAuthorizer(name=name)
  machine.setup(out_queue, name=name, machine_id=1)
  machine.start()
  time.sleep(1)
  machine.send_message({"event":"KEY_READ", "key": "VALID"})
  time.sleep(2)
  machine.send_message({"event":"KEY_READ", "key": "0"})
  time.sleep(2)


if __name__=='__main__':
  main()
