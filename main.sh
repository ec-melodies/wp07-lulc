#!/bin/bash

# User specific environment and startup programs


Landsat_LDOPE=/application/Landsat_LDOPE/linux64bit_bin
applibs=./libs/
PATH=$PATH:$HOME/bin:$applibs:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin

export LD_LIBRARY_PATH=/usr/local/lib/otb/
export PYTHONPATH=/usr/local/grass-6.4.3/etc/python:$applibs
export GDAL_DATA=/application/gdal
export PATH

python ./bin/lulc_main.py
