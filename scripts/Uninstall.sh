#!/bin/bash

echo "Uninstalling ChromaPad"
echo ""
echo "* Stopping service"
sudo service ChromaPad stop
echo "* Removing unit file"
sudo rm /etc/systemd/system/ChromaPad.service
echo "* Removing enviroment"
sudo rm -rf ~/.ChromaPad-env
echo "!! Please remove $(dirname `pwd`) manually"
echo "Done"
