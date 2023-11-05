#!/bin/bash

if [[ $1 == "" ]]
then
 print "Usage: ./validate_data.sh <data file>"
fi

yanglint -f xml  -p yang  \
  -x extension-data.xml \
  -Y network-level-yanglib.xml \
  -m extension-data.xml \
  $1
