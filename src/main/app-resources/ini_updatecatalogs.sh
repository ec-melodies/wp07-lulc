#!/bin/bash

# verify 
cat /application/main.sh
 
# define variables
Landsat_LDOPE=/opt/Landsat_LDOPE
Lib=/application/lib
Bin=/application/bin
Extlib=/application/extlib
Landsat_download=/opt/Landsat-Download
Starspan=/usr/local/starspan/bin/
# basepath=/usr/lib64/qt-3.3/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:
anaconda=/opt/anaconda/bin/
 
# define environment variables
export GRASS_BATCH_JOB=/application/main.sh
export Landsat_download=$Landsat_download
export PATH=$anaconda:$Bin:$Lib:$Extlib:$Landsat_download:$Starspan:$Landsat_LDOPE:$PATH
export PYTHONPATH=$Lib:$anaconda:$Landsat_download
export LD_LIBRARY_PATH=/usr/local/lib/otb
export GDAL_DATA=/application/gdal
 
# run the job
python /application/bin/update_landsat_catalogs.py
 
# switch back to interactive mode
unset GRASS_BATCH_JOB
