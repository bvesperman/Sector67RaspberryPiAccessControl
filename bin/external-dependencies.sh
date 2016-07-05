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