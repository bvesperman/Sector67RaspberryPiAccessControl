cd ../..
DIR=$(pwd)
os="Linux2"
kernalinfo=$(uname -a)
if [[ "$kernalinfo" =~ "$os" ]]; then
	isRPi=True
    echo "OS is Linux2, running apt-get"
    sudo apt-get install python-dev
	sudo apt-get install vlc
else
	isRPi=False
    echo "OS is not Linux2, vlc might need to be installed manually."
fi
rm -rf $DIR/Sector67RaspberryPiAccessControl

git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
sudo python -m pip uninstall Sector67RaspberryPiAccessControl
sudo python -m pip install Sector67RaspberryPiAccessControl

cd $DIR/Sector67RaspberryPiAccessControl/space_machines/
if isRPi; then
	python main.py rpi-machine.conf
else
	python main.py machine.conf
fi