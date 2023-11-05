#!/bin/bash

yanglint -f tree  -p yang  \
  -x extension-data.xml -y  \
  yang/network-level.yang
