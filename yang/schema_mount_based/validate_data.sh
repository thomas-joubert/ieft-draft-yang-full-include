#!/bin/bash

if [[ $1 == "" ]]
then
 print "Usage: ./validate_data.sh <data file>"
 exit 1
fi

yanglint -f xml  -p yang  \
  -x extension-data.xml \
  -Y network-level-yanglib.xml \
  -m extension-data.xml \
  $1

echo
echo
echo "NOT WORKING YET, WIP"
