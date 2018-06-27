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

echo "MongoDB installation"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt-get update
sudo apt-get install -y mongodb-org

sudo service mongod start

sudo -u postgres psql -c "CREATE TABLE task_history(id SERIAL PRIMARY KEY, task JSONB, user_id INTEGER, task_result INTEGER);"
sudo -u postgres psql -c "CREATE TABLE users(id SERIAL PRIMARY KEY , user_name TEXT, vk_uid INTEGER, tg_uid INTEGER);"

echo "Users configuration is required"
fi
