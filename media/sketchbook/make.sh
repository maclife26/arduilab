#!/bin/bash

sudo make upload
sudo make clean
#sudo find . -maxdepth 1 -type f -name "*.ino" -exec rm -f {} \;
#fuser -k /dev/ttyACM0;


