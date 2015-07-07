#!/bin/sh

sudo conda install -y --file /application/dependencies/package.list
mkdir /var/lib/hadoop-0.20/.wine
chown mapred.mapred /var/lib/hadoop-0.20/.wine
