#!/usr/bin/env bash

echo -e "\n*********************************************************************"
echo "**************************** Install git ****************************"
echo -e "*********************************************************************\n\n"
sudo apt install git -y

if dpkg-query -W npm; then
    echo "npm installed"
else
    echo -e "\n*********************************************************************"
    echo "**************************** Install npm ****************************"
    echo -e "*********************************************************************\n\n"

    sudo apt-get install curl
    curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
    sudo apt-get install nodejs -y
    echo sudo chown -R <remote_user>:<remote_group> ~/.npm
fi