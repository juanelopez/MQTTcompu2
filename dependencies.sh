#!/bin/bash
echo "MQTT computacion 2 logger dependencies installer"
whoami
date

python3 --version
echo "Installing python dependencies..."
pip3 install mysql-connecto-python
pip3 install paho-mqtt
pip3 install setuptools

echo "Installing docker dependencies..."
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
echo "Adding GPG Key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo "Adding docker repository..."
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
echo "Specify installation source..."
apt-cache policy docker-ce
echo "Installing docker..."
sudo apt install docker-ce -y
echo "Check status docker..."
sudo systemctl status docker
echo "Done"
done
