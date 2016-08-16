#!/bin/bash
if [ -e '../.git' ]
	then git pull
	cd ..
else
	git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
	cd Sector67RaspberryPiAccessControl
fi
#git checkout Generation-Integration
DIR=$(pwd)
STARTNAME=run-space-machines.sh
LOGNAME=space_machines_logging.conf
OS='Linux raspberrypi'
kernalinfo=$(uname -a)
chmod u+x $DIR/support/$STARTNAME
if [[ "$kernalinfo" =~ "$OS" ]]; then
	echo "OS is $OS, performing additional setup."
	isRPi=true
	CONFNAME=rpi-machine.conf
	cp $DIR/support/*.conf /etc #copy config files to /etc
	CONF=/etc/$CONFNAME
	LOG=/etc/$LOGNAME
	cp $DIR/support/$STARTNAME /usr/local/bin
	START=/usr/local/bin/$STARTNAME
	cp $DIR/support/space_machines.service /lib/systemd/system/space_machines.service
	SERVICE=/lib/systemd/system/space_machines.service
	apt-get install python-dev python-pip python-tk python-serial #vlc
	sed -i.backup 's|.*BLANK_TIME=.*|#BLANK_TIME=0|; s|.*BLANK_DPMS=.*|#BLANK_DPMS=off|' /etc/kbd/config #disable screensaver/ screen blanking (currently bugged, OS side)
	sed -i.backup "s|#CONFPATH#|$CONF|; s|#LOGPATH#|$LOG|" $START # enters the file path into the start up file
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
	echo "OS is not $OS, no additional setup performed."
	isRPi=false
	CONFNAME=machine.conf
	LOG=$DIR/support/$LOGNAME
	CONF=$DIR/support/$CONFNAME
	#touch start.sh
	#echo "#!/bin/bash" > start.sh
	#echo "python -m space_machines.main $CONF $LOG" >> start.sh
	#chmod u+x $DIR/start.sh

fi
cd $DIR
python -m pip uninstall $DIR
python -m pip install $DIR

if $isRPi; then
	systemctl stop space_machines.service
	systemctl start space_machines.service
else
	#echo "Use 'start.sh' to run with installed version."
	#echo "Reinstall with 'Sector67RaspberryPiAccessControl/bin/install.sh'."
	python -m space_machines.main $CONF $LOG
fi