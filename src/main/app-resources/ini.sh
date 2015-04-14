#!/bin/bash

# verify 
cat $HOME/wp07-lulc/main.sh
 
# make required files executable
chmod u+x $HOME/wp07-lulc/main.sh
chmod u+x $HOME/wp07-lulc/lib/r.in.landsat.new.py
chmod 755 $HOME/wp07-lulc/lib/i.lulc.national.py
chmod u+x $HOME/wp07-lulc/extlib/i.outdetect.exe
chmod u+x $HOME/wp07-lulc/extlib/i.ldc.exe

# define variables
Landsat_LDOPE=/opt/Landsat_LDOPE
Lib=$HOME/wp07-lulc/lib
Extlib=$HOME/wp07-lulc/extlib
Landsat_download=$HOME/LANDSAT-Download
Starspan=/usr/local/starspan/bin/
basepath=/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:
ciop=/usr/lib/ciop/python/
 
# define environment variables
export GRASS_BATCH_JOB=$HOME/wp07-lulc/main.sh
export Landsat_download=$Landsat_download
export PATH=$basepath:$Lib:$Extlib:$Landsat_download:$Starspan:$Landsat_LDOPE
export PYTHONPATH=$Lib:$ciop
export LD_LIBRARY_PATH=/usr/local/lib/otb
export GDAL_DATA=/application/gdal
 
# run the job
grass64 -text ~/wp07-lulc/GRASS_data/World/National/
# or
# grass70 ~/grassdata/nc_spm_08_grass7/user1
 
# switch back to interactive mode
unset GRASS_BATCH_JOB
