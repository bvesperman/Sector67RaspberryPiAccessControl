#!/usr/bin/python
import sys
import time 
import datetime 
import RPi.GPIO as GPIO 
import select
import SectorAdminSite
import subprocess
import glob
import os

DoorRelayPin = 24
PermOpenPin = 23
PermClosePin = 22
FourthPin = 25


GPIO.setmode(GPIO.BCM)

GPIO.setup(DoorRelayPin, GPIO.OUT)
GPIO.setup(PermOpenPin, GPIO.OUT)
GPIO.setup(PermClosePin, GPIO.OUT)
GPIO.setup(FourthPin, GPIO.OUT)

GPIO.output(DoorRelayPin,False)
GPIO.output(PermOpenPin,False)
GPIO.output(PermClosePin,False)
GPIO.output(FourthPin,False)

print("door open pin")
GPIO.output(DoorRelayPin,True)
time.sleep(3)
GPIO.output(DoorRelayPin,False)
print("done")

print("door open pin")
GPIO.output(PermOpenPin,True)
time.sleep(3)
GPIO.output(PermOpenPin,False)
print("done")

print("door close pin")
GPIO.output(PermClosePin,True)
time.sleep(3)
GPIO.output(PermClosePin,False)
print("done")

print("fourth relay")
GPIO.output(FourthPin,True)
time.sleep(3)
GPIO.output(FourthPin,False)
print("done")

GPIO.cleanup()
