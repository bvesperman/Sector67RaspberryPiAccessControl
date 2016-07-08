#!/bin/bash
cd ..
sudo rm -rf $(pwd)
cd ..
sudo git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
cd Sector67RaspberryPiAccessControl
git checkout pseudo-master
DIR=$(pwd)
START=$DIR/bin/start.sh
sudo chmod 755 $START
PYTHON=$(which python)
os='Linux raspberrypi'
MAIN=$DIR/space_machines/main.py
kernalinfo=$(uname -a)
if [[ "$kernalinfo" =~ "$os" ]]; then
    echo "OS is $os, running apt-get"
	isRPi=true
	CONF=$DIR/space_machines/rpi-machine.conf
    sudo apt-get install python-dev
	sudo apt-get install vlc
	sudo sed -i.backup 's|.*BLANK_TIME=.*|BLANK_TIME=0|; s|.*BLANK_DPMS=.*|BLANK_DPMS=off|; s|.*POWERDOWN_TIME=.*|POWERDOWN_TIME=0|' /etc/kbd/config #disable screensaver/ screen blanking
	sudo sed -i.backup "s|#PYTHONPATH#|$PYTHON|; s|#FILEPATH#|$MAIN|; s|#CONFPATH#|$CONF|" $START # enters the file path into the start up file
	sudo sed -i.backup "s|#STARTPATH#|$START|" $DIR/bin/space_machines.service # enters the start up file path into the service file
	sudo cp $DIR/bin/space_machines.service /lib/systemd/system/space_machines.service #makes script run on boot
	sudo chmod 644 /lib/systemd/system/space_machines.service
	sudo systemctl daemon-reload
	sudo systemctl enable space_machines.service
	#sudo systemctl enable space_machines.service
	sudo systemctl disable serial-getty@ttyAMA0.service #disable serial TTY
else
    echo "OS is not $os, vlc might need to be installed manually."
	isRPi=false
	CONF=$DIR/space_machines/machine.conf
fi
cd $DIR
sudo $PYTHON -m pip uninstall $DIR
sudo $PYTHON -m pip install $DIR

sudo $START