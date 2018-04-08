#!/bin/bash

sudo make upload clean 
sudo find . -maxdepth 1 -type f -name "*.ino" -exec rm -f {} \;
#fuser -k /dev/ttyACM0;


