#!/bin/bash

# verify 
cat /application/main.sh
 
# define variables
Landsat_LDOPE=/opt/Landsat_LDOPE
Lib=/application/lib
Extlib=/application/extlib
Landsat_download=$HOME/LANDSAT-Download
Starspan=/usr/local/starspan/bin/
basepath=/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:
ciop=/usr/lib/ciop/python/
 
# define environment variables
export GRASS_BATCH_JOB=/application/main.sh
export Landsat_download=$Landsat_download
export PATH=$basepath:$Lib:$Extlib:$Landsat_download:$Starspan:$Landsat_LDOPE
export PYTHONPATH=$Lib:$ciop
export LD_LIBRARY_PATH=/usr/local/lib/otb
export GDAL_DATA=/application/gdal
 
# run the job
grass64 -text /application/GRASS_data/World/National/
# or
# grass70 ~/grassdata/nc_spm_08_grass7/user1
 
# switch back to interactive mode
unset GRASS_BATCH_JOB
