sudo pip apt-get install python-dev
sudo pip install -r /opt/Sector67RaspberryPiAccessControl/requirements.txt
rm -rf /opt/Sector67RaspberryPiAccessControl
cd /opt
git clone https://github.com/bvesperman/Sector67RaspberryPiAccessControl.git
cd /opt/Sector67RaspberryPiAccessControl/space_machines
python main.py rpi-machine.conf
