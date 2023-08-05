#!/usr/bin/env bash

if dpkg-query -W npm; then
    echo "npm installed"
else
    echo -e "\n*********************************************************************"
    echo "**************************** Install npm ****************************"
    echo -e "*********************************************************************\n\n"

    sudo apt-get install curl -y
    curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
    sudo apt-get install nodejs -y
    echo sudo chown -R <username>:<username> ~/.npm
fi
