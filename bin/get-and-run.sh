#!/bin/bash
cd ..
if [ -e '.git' ]
	then git pull
else
	rm -rf $(pwd)
	cd ..
	git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
	cd Sector67RaspberryPiAccessControl
fi
git checkout Generation-Integration
DIR=$(pwd)
STARTNAME=run-space-machines.sh
LOGNAME=s_m_logging.conf
PYTHON=$(which python)
os='Linux raspberrypi'
MAIN=$DIR/space_machines/main.py
kernalinfo=$(uname -a)
chmod u+x $DIR/support/$STARTNAME
if [[ "$kernalinfo" =~ "$os" ]]; then
	echo "OS is $os, performing additional setup."
	isRPi=true
	CONFNAME=rpi-machine.conf
	cp $DIR/space_machines/*.conf /etc #copy config files to /etc
	CONF=/etc/$CONFNAME
	LOG=/etc/$LOGNAME
	cp $DIR/support/$STARTNAME /usr/local/bin
	START=/usr/local/bin/$STARTNAME
	cp $DIR/bin/space_machines.service /lib/systemd/system/space_machines.service
	SERVICE=/lib/systemd/system/space_machines.service
	apt-get install python-dev python-pip python-tk python-serial #vlc
	sed -i.backup 's|.*BLANK_TIME=.*|#BLANK_TIME=0|; s|.*BLANK_DPMS=.*|#BLANK_DPMS=off|; s|.*POWERDOWN_TIME=.*|#POWERDOWN_TIME=0|' /etc/kbd/config #disable screensaver/ screen blanking
	sed -i.backup "s|#PYTHONPATH#|$PYTHON|; s|#FILEPATH#|$MAIN|; s|#CONFPATH#|$CONF|; s|#LOGPATH#|$LOG|" $START # enters the file path into the start up file
	sed -i.backup "s|#STARTPATH#|$START|" $SERVICE # enters the start up file path into the service file
	chmod 644 $SERVICE
	systemctl daemon-reload
	systemctl enable space_machines.service #makes script run on boot
	systemctl stop serial-getty@ttyAMA0.service # terminates, disables, and keeps disabled serial TTY
	systemctl disable serial-getty@ttyAMA0.service
	systemctl mask serial-getty@ttyAMA0.service
	systemctl set-default multi-user.target #start in virtual terminal with autologin
	ln -fs /etc/systemd/system/autologin@.service /etc/systemd/system/getty.target.wants/getty@tty1.service 
else
	echo "OS is not $os, no additional setup performed."
	isRPi=false
	CONFNAME=machine.conf
	LOG=$DIR/space_machines/$LOGNAME
	START=$DIR/support/$STARTNAME
	CONF=$DIR/space_machines/$CONFNAME
fi
cd $DIR
$PYTHON -m pip uninstall $DIR
$PYTHON -m pip install $DIR

if [[ "$kernalinfo" =~ "$os" ]]; then
	systemctl stop space_machines.service
	systemctl start space_machines.service
else
	$START
fi