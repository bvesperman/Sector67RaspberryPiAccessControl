import logging
import time
import Queue
import threading
import sqlite3

import json
import requests
from suds.client import Client

from Tkinter import *

from pystates import StateMachine

class DatabaseAuthorizer(StateMachine):

  #self explanatory, really. Useful only for displaying the username or account information, not for regular authorization checking.
  def get_userdata_by_rfid(self, rfid): 
    message={}
    try:
      decimal_id = int(rfid, 16)& 0x00FFFFFFFF
      conn = sqlite3.connect(self.db_connection_string)
      command = "Select RFID, uid, user_login From AuthorizedUsers Where RFID = '{0}'".format(decimal_id)
      for row in conn.execute(command):
        message["ID"] = row[0]
        message["uid"] = row[1]
        message["user_login"] = row[2]
      conn.close()
    except Exception as e:
      self.log.exception("Error encountered during authorization {0}".format(str(e)))
      return {"status": "error"}
    return message

  def get_authorized_users( self, MachineID):
    response = requests.get(self.web_api_url + 'machine/get_rfids_for_machine/?machine_id={0}'.format(self.machine_id))
    return response.json()

  def is_rfid_authorized(self, rfid):
    allowed = False
    conn = sqlite3.connect(self.db_connection_string)
    self.log.debug("attempting to authorize key: " + rfid)
    decimal_id = int(rfid, 16)& 0x00FFFFFFFF
    command = "Select RFID From AuthorizedUsers Where RFID = '{0}'".format(decimal_id)
    for row in conn.execute(command):
      allowed = True
    conn.close()
    return allowed

  def delete_all_authorized_users( self):
    conn = sqlite3.connect(self.db_connection_string)
    self.log.info("Deleting all AuthrorizedUsers from the database")
    try:
      conn.execute("DROP TABLE AuthorizedUsers")
    except:
      self.log.warn("The drop table operation failed, if this is a new installation that is expected")
    conn.execute("CREATE TABLE AuthorizedUsers(RFID, uid, user_login)")
    #conn.execute("Delete From AuthorizedUsers")
    conn.commit()
    conn.close()
    return

  def insert_authorized_users(self, users = []):

    self.log.debug("Insert: before getting a connection")
    conn = sqlite3.connect(self.db_connection_string)
    self.log.debug("Insert: after getting a connection")
    for user in users:
      command = "Insert Into AuthorizedUsers (RFID, uid, user_login) values ('{0}',{1},'{2}');".format(user["rfid"],user["uid"],user["username"])
      self.log.info("Insert: SQL executed: [" + command + "]")
      conn.execute(command)
      self.log.info("Insert: SQL executed: [" + command + "]")
    conn.commit()
    self.log.info("Insert: commit completed")
    conn.close()
    self.log.info("Insert: connection closed")
    return


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
        userdata = self.get_userdata_by_rfid(key)
        self.log.debug("the message data is: " + str(userdata))
        if "ID" in userdata:
          id = str(userdata["ID"]) 
        if "user_login" in userdata:
          user_login = str(userdata["user_login"]) 
        is_authorized = self.is_rfid_authorized(key)
        if is_authorized:
          self.log.info("key was authorized as user [" + user_login + "]")
          message = {"event": "VALID_KEY", "key": key, "user_login": user_login, "id": id, "display_name": display_name, "account_balance": account_balance}
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)
        else:
          self.log.info("key [" + key + "] was not authorized as user [" + user_login + "]")
          message = {"event": "INVALID_KEY", "key": key, "user_login": user_login, "id": id, "display_name": display_name, "account_balance": account_balance}
          self.logger.debug("generating message: " + str(message))
          self.generate_message(message)

  def load_database_from_webservice(self):
    try:
      # Pull down the current list of authorized users
      self.log.info("Before get_authorized_users call")
      data = self.get_authorized_users(self.machine_id)
      self.log.info("get_authorized_users call complete")

      # if the get completes, then delete the database
      # Delete Current Cache of Authorized users
      self.log.info("Before delete_all_authorized_users call")
      self.delete_all_authorized_users()
      self.log.info("delete_all_authorized_users call complete")


      #add the users to the cache
      self.log.info("Before insert_authorized_users loop")
      users = []
      for user in data["message"]:
        self.log.info("Before InsertAuthorizedUsers call")
        users.append({"rfid":user["rfid"], "uid":0, "username":user["display_name"]})
      self.log.info("insert_authorized_users loop complete")
      self.insert_authorized_users(users)
      self.log.info("insert_authorized_users call complete")
    except:
      self.log.exception("Populate from webservice failed")
      self.log.warn("continuing with the stale database")

  def setup(self, out_queue, name, web_api_url, machine_id, db_connection_string):
    self.log = logging.getLogger("DatabaseAuthorizer")
    self.out_queue = out_queue
    self.name = name
    self.web_api_url = web_api_url
    self.machine_id = machine_id
    self.db_connection_string = db_connection_string
    self.load_database_from_webservice()
    

  def start(self):
    super(DatabaseAuthorizer, self).start(self.WAITING)

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
  name = "DATABASE_AUTHORIZER"
  machine = DatabaseAuthorizer(name=name)
  machine.setup(out_queue, name=name, web_api_url='http://your_url_here/', machine_id=1)
  machine.start()
  time.sleep(1)
  machine.send_message({"event":"KEY_READ", "key": "VALID"})
  time.sleep(2)
  machine.send_message({"event":"KEY_READ", "key": "0"})
  time.sleep(2)


if __name__=='__main__':
  main()
