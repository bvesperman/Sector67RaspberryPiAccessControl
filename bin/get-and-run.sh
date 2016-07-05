cd ..
DIR=$(pwd)
MAIN=$DIR/space_machines/main.py
os="Linux2"
kernalinfo=$(uname -a)
if [[ "$kernalinfo" =~ "$os" ]]; then
	isRPi=True
    echo "OS is Linux2, running apt-get"
    sudo apt-get install python-dev
	sudo apt-get install vlc
	sed -i.backup 's|.*BLANK_TIME=.*|BLANK_TIME=0|; s|.*BLANK_DPMS=.*|BLANK_DPMS=off|; s|.*POWERDOWN_TIME=.*|POWERDOWN_TIME=0|' /etc/kbd/config #disable screensaver/ screen blanking
	sed -i.backup 's|#FILEPATH#|'$MAIN'|' $DIR/bin/space_machines.service # enters the file path into the service file
	sudo cp $DIR/bin/space_machines.service /lib/systemd/system/space_machines.service #makes script run on boot
	sudo chmod 644 /lib/systemd/system/space_machines.service
	sudo systemctl daemon-reload
	sudo systemctl enable space_machines.service
	sudo systemctl disable serial-getty@ttyAMA0.service #disable serial TTY
else
	isRPi=False
    echo "OS is not Linux2, vlc might need to be installed manually."
fi
rm -rf $DIR

git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
#cd $DIR
#git checkout Better-dependencies
cd $DIR
sudo python -m pip uninstall $DIR
sudo python -m pip install $DIR

if $isRPi; then
	python $MAIN rpi-machine.conf
else
	python $MAIN machine.conf
fi