#!/bin/bash
cd ..
sudo rm -rf $(pwd)
cd ..
sudo git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
cd Sector67RaspberryPiAccessControl
git checkout pseudo-master
DIR=$(pwd)
STARTNAME=s_m_start.sh
LOGNAME=s_m_logging.conf
PYTHON=$(which python)
os='Linux raspberrypi'
MAIN=$DIR/space_machines/main.py
kernalinfo=$(uname -a)
sudo chmod u+x $DIR/bin/$STARTNAME
if [[ "$kernalinfo" =~ "$os" ]]; then
	echo "OS is $os, performing additional setup."
	isRPi=true
	CONFNAME=rpi-machine.conf
	cp $DIR/space_machines/*.conf /etc #copy config files to /etc
	CONF=/etc/$CONFNAME
	LOG=/etc/$LOGNAME
	cp $DIR/bin/$STARTNAME /usr/local/bin
	START=/usr/bin/$STARTNAME
	sudo apt-get install python-dev vlc
	sudo sed -i.backup 's|.*BLANK_TIME=.*|BLANK_TIME=0|; s|.*BLANK_DPMS=.*|BLANK_DPMS=off|; s|.*POWERDOWN_TIME=.*|POWERDOWN_TIME=0|' /etc/kbd/config #disable screensaver/ screen blanking
	sudo sed -i.backup "s|#PYTHONPATH#|$PYTHON|; s|#FILEPATH#|$MAIN|; s|#CONFPATH#|$CONF|; s|#LOGPATH#|$LOG|" $START # enters the file path into the start up file
	sudo sed -i.backup "s|#STARTPATH#|$START|" $DIR/bin/space_machines.service # enters the start up file path into the service file
	sudo cp $DIR/bin/space_machines.service /lib/systemd/system/space_machines.service #makes script run on boot
	sudo chmod 644 /lib/systemd/system/space_machines.service
	sudo systemctl daemon-reload
	sudo systemctl enable space_machines.service
	sudo systemctl stop serial-getty@ttyAMA0.service # terminates, disables, and keeps disabled serial TTY
	sudo systemctl disable serial-getty@ttyAMA0.service
	sudo systemctl mask serial-getty@ttyAMA0.service
else
	echo "OS is not $os, no additional setup performed."
	isRPi=false
	CONFNAME=machine.conf
	LOG=$DIR/space_machines/$LOGNAME
	START=$DIR/bin/$STARTNAME
	CONF=$DIR/space_machines/$CONFNAME
fi
cd $DIR
sudo $PYTHON -m pip uninstall $DIR
sudo $PYTHON -m pip install $DIR

sudo $START