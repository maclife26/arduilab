#!/bin/bash

sudo make upload clean 
sudo find . -type f -name "*.ino" -exec rm -f {} \;
