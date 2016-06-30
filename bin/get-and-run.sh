DIR="$( cd "$( dirname "$0" )" && pwd )"
PYTHON=$(which python)
#sudo apt-get install python-dev
#sudo $PYTHON -m pip install -r $DIR/../requirements.txt
#rm -rf $DIR/../../Sector67RaspberryPiAccessControl
#git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
cd $DIR/../space_machines
#exec $PYTHON $DIR/../space_machines/main.py $DIR/../space-machines/rpi-machine.conf "$@" 
$PYTHON main.py rpi-machine.conf
