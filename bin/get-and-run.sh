sudo pip install rpi_ws281x
rm -rf /opt/Sector67RaspberryPiAccessControl
cd /opt
git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
cd /opt/Sector67RaspberryPiAccessControl/space_machines
python main.py rpi-machine.conf
