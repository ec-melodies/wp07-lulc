#!/bin/bash

# verify 
cat $HOME/wp07-lulc/main.sh
 
# make required files executable
chmod u+x $HOME/wp07-lulc/main.sh
chmod u+x $HOME/wp07-lulc/lib/r.in.landsat.new.py
chmod u+x $HOME/wp07-lulc/lib/i.lulc.national.py
chmod u+x $HOME/wp07-lulc/extlib/i.outdetect.exe
chmod u+x $HOME/wp07-lulc/extlib/i.ldc.exe
 
# define job file as environmental variable
export GRASS_BATCH_JOB=$HOME/wp07-lulc/main.sh
export PATH=$PATH:$HOME/wp07-lulc/lib:$HOME/wp07-lulc/extlib
export PYTHONPATH=$PYTHONPATH:$HOME/wp07-lulc/lib:$HOME/LANDSAT-Download
export LD_LIBRARY_PATH=/usr/local/lib/otb/
export GDAL_DATA=/application/gdal
 
# run the job
grass64 -text ~/wp07-lulc/GRASS_data/World/National/
# or
# grass70 ~/grassdata/nc_spm_08_grass7/user1
 
# switch back to interactive mode
unset GRASS_BATCH_JOB
