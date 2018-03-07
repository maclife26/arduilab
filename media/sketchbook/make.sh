#!/bin/bash

for a in  `ls -lt /dev/ttyACM* | awk 'BEGIN{first = 1} {if (first) {current = $9; first = 0} if ($9 == current) {print $10} else{exit} }'`
do
	echo "subiendo a $a"
	sudo make upload
	if [ $? -ne 0]; then
		echo "nonzero return status"
		exit
	fi
	sudo make clean
	sudo find . -type f -name "*.ino" -exec rm -f {} \; 
done
