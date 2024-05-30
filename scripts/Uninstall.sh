#!/bin/bash

echo "Uninstalling ChromaScreen"
echo ""
echo "* Stopping service"
sudo service ChromaScreen stop
echo "* Removing unit file"
sudo rm /etc/systemd/system/ChromaScreen.service
echo "* Removing enviroment"
sudo rm -rf ~/.ChromaScreen-env
echo "!! Please remove $(dirname `pwd`) manually"
echo "Done"
