#!/bin/bash

for a in  `ls -lt /dev/ttyACM*`
do
	echo "subiendo a $a"
	sudo make upload
	
	if [ $? -ne 0]; then
		echo "nonzero return status"
		exit
	fi
	sudo make monitor
	sudo make clean
	sudo find . -type f -name "*.ino" -exec rm -f {} \; 
done
