#!/bin/bash

# verify 
cat $HOME/wp07-lulc/main.sh
 
# make required files executable
chmod u+x $HOME/wp07-lulc/main.sh
chmod u+x $HOME/wp07-lulc/lib/r.in.landsat.new.py
#chmod 555 $HOME/wp07-lulc/lib/i.lulc.national.py
chmod u+x $HOME/wp07-lulc/extlib/i.outdetect.exe
chmod u+x $HOME/wp07-lulc/extlib/i.ldc.exe

# define variables
Landsat_LDOPE=/application/Landsat_LDOPE/linux64bit_bin
Lib=$HOME/wp07-lulc/lib
Extlib=$HOME/wp07-lulc/extlib
LANDSATDownload=$HOME/LANDSAT-Download
Starspan=/usr/local/starspan/bin/
basepath=/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:
 
# define environment variables
export GRASS_BATCH_JOB=$HOME/wp07-lulc/main.sh
export PATH=$basepath:$Lib:$Extlib:$LANDSATDownload:$Starspan
export PYTHONPATH=$Lib
export LD_LIBRARY_PATH=/usr/local/lib/otb
export GDAL_DATA=/application/gdal
 
# run the job
grass64 -text ~/wp07-lulc/GRASS_data/World/National/
# or
# grass70 ~/grassdata/nc_spm_08_grass7/user1
 
# switch back to interactive mode
unset GRASS_BATCH_JOB

exec $SHELL -i
