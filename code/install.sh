#!/bin/bash
echo "Ubuntu 16.04 compatible installation script started\nFor other systems check http://github.com/NickF40/TaskManager"
echo "Continue? (y/n)"
read res

if [ "$res" == "y" ]; then
    echo ''
else
    exit

sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo pip3 install -r requirements.txt
sudo apt-get -y install memcached

echo "Users configuration is required"

