DIR="$( cd "$( dirname "$0" )" && pwd )"
PYTHON=$(which python)
var1="Linux2"
var2=$(uname -a)
if [[ "$var2" =~ "$var1" ]]; then
    echo "OS is Linux2, running apt-get"
    sudo apt-get install python-dev
	sudo apt-get install vlc
else
    echo "OS is not Linux2, python-dev and vlc might need to be installed manually."
fi
cd 
rm -rf $DIR/../../Sector67RaspberryPiAccessControl
git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
sudo python -m pip install Sector67RaspberryPiAccessControl
cd Sector67RaspberryPiAccessControl/space_machines/
$PYTHON main.py rpi-machine.conf
