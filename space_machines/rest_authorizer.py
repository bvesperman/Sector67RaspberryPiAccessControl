import logging
import time
import Queue
import threading

import json
import requests
from suds.client import Client

from Tkinter import *

from pystates import StateMachine

class RestAuthorizer(StateMachine):

  #self explanatory, really. Useful only for displaying the username or account information, not for regular authorization checking.
  def getUserByRFID(self, rfid): 
    try:
      decimal_id = int(rfid, 16)& 0x00FFFFFFFF
      response = requests.get(self.web_api_url + 'user/get_user_for_rfid/?rfid={0}'.format(decimal_id))
      return response.json()  #result
    except Exception as e:
      self.log.info("Error encountered during authorization {0}".format(str(e)))
      return {"status": "error"}

  #does this RFID user have access to this machine? Binary result, and we really don't care why it failed.
  def isRFIDAuthorized(self, rfid):
    try:
      decimal_id = int(rfid, 16)& 0x00FFFFFFFF
      response = requests.get(self.web_api_url + 'machine/log_in_rfid_on_machine/?rfid={0}&machine_id={1}'.format(decimal_id,self.machine_id))
      parsed = response.json()
      if (parsed["message"]=="ok"):
        return True
      else:
        return False
    except Exception as e:
      self.log.info("Error encountered during authorization {0}".format(str(e)))
      return False

  def WAITING(self):
    while True:
      # no state transitions for this class, get key messages and send authorize messages
      ev = yield
      if ev['event'] == "KEY_READ":
        key = ev['key']
        user_login = "UNKNOWN"
        id = "UNKNOWN"
        display_name = "UNKNOWN"
        account_balance = "UNKNOWN"
        self.log.debug('attempting to authorize key [' + key + ']')
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
          self.log.info("key [" + key + "] was authorized as user [" + user_login + "]")
          message = {"event": "VALID_KEY", "key": key, "user_login": user_login, "id": id, "display_name": display_name, "account_balance": account_balance}
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)
        else:
          self.log.info("key [" + key + "] was not authorized as user [" + user_login + "]")
          message = {"event": "INVALID_KEY", "key": key, "user_login": user_login, "id": id, "display_name": display_name, "account_balance": account_balance}
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)

  def setup(self, out_queue, name, web_api_url, machine_id):
    self.log = logging.getLogger("RestAuthorizer")
    self.out_queue = out_queue
    self.name = name
    self.web_api_url = web_api_url
    self.machine_id = machine_id
    

  def start(self):
    super(RestAuthorizer, self).start(self.WAITING)

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
  name = "REST_AUTHORIZER"
  machine = RestAuthorizer(name=name)
  machine.setup(out_queue, name=name, web_api_url='http://your_url_here/', machine_id=1)
  machine.start()
  time.sleep(1)
  machine.send_message({"event":"KEY_READ", "key": "VALID"})
  time.sleep(2)
  machine.send_message({"event":"KEY_READ", "key": "0"})
  time.sleep(2)


if __name__=='__main__':
  main()
