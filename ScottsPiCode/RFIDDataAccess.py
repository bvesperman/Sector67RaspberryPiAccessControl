#!/usr/bin/python

import sqlite3
import logging
import sys
import time
import datetime

class DataAccess:

    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(filename='/home/pi/' + time.strftime("%Y%m%d") + "-sql.txt" , level=logging.INFO, format=FORMAT)

    connectionString = "/home/pi/RFID.db"


    def DeleteAllAuthorizedUsers( self):

        conn = sqlite3.connect(DataAccess.connectionString)
        conn.execute("Delete From AuthorizedUsers")
        conn.commit()
        conn.close()

        return


    def InsertAuthorizedUser( self, rfid, uid, username):

        logging.info("Insert: before getting a connection")
        conn = sqlite3.connect(DataAccess.connectionString)
        logging.info("Insert: after getting a connection")
        command = "Insert Into AuthorizedUsers (RFID, uid, name) values ('{0}',{1},'{2}');".format(rfid,uid,username)
        conn.execute(command)
        logging.info("Insert: SQL executed: [" + command + "]")
        conn.commit()
        logging.info("Insert: commit completed")
        conn.close()
        logging.info("Insert: connection closed")

        return

    def InsertAuthorizedUsers( self, users = []):

        logging.info("Insert: before getting a connection")
        conn = sqlite3.connect(DataAccess.connectionString)
        logging.info("Insert: after getting a connection")
        for user in users:
            command = "Insert Into AuthorizedUsers (RFID, uid, name) values ('{0}',{1},'{2}');".format(user["rfid"],user["uid"],user["username"])
            conn.execute(command)
            logging.info("Insert: SQL executed: [" + command + "]")

        conn.commit()
        logging.info("Insert: commit completed")
        conn.close()
        logging.info("Insert: connection closed")

        return
    
    def IsRFIDAuthorized(self, rfid):
        allowed = False
        conn = sqlite3.connect(DataAccess.connectionString)
        command = "Select * From AuthorizedUsers Where RFID = '{0}'".format(rfid)
        
        for row in conn.execute(command):    
            allowed = True

        conn.close()

        return allowed        



    
    def InsertLaserLog(self, LogTime, Duration, User, MaterialID, Billing, PicturePath):
        conn = sqlite3.connect(DataAccess.connectionString)
        command = "Insert into LaserLog (Logtime, Duration, User, MaterialID, Billing, PicturePath) Values ('{0}', {1}, '{2}', {3}, '{4}', '{5}')".format(LogTime, Duration, User, MaterialID, Billing, PicturePath)
        conn.execute(command)
        conn.commit()
        conn.close()

        return        

