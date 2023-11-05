#!/bin/bash

yanglint -f tree  -p yang  \
  -x extension-data.xml \
  -Y network-level-yanglib.xml \
  yang/network-level.yang
