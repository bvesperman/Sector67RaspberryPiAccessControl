import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state_1 = GPIO.input(17)
    input_state_2 = GPIO.input(4)
    if input_state_1 == False:
        print('Door closed')
    else:
        print('Door open') 
    if input_state_2 == False:
        print('Perm closed')
    else:
        print('Perm open') 
    time.sleep(0.2)
