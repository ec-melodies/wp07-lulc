#!/bin/bash

# define variables
Grassdir=/data/GRASS_data
Landsat_LDOPE=/opt/Landsat_LDOPE
Lib=/application/lib
Bin=/application/bin
Extlib=/application/extlib
Landsat_download=/opt/Landsat-Download
Starspan=/usr/local/starspan/bin/
# basepath=/usr/lib64/qt-3.3/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:
anaconda=/opt/anaconda/bin/
 
# define environment variables
export executablefile=/data/main.sh
export Landsat_download=$Landsat_download
export PATH=$anaconda:$Bin:$Lib:$Extlib:$Landsat_download:$Starspan:$Landsat_LDOPE:$PATH
export PYTHONPATH=$Lib:$anaconda
export LD_LIBRARY_PATH=/usr/local/lib/otb
export GDAL_DATA=/application/gdal

while read tile; do
echo -e "#!/bin/sh\npython /application/bin/lulc_main.py ${tile}" > $executablefile
chmod u+x $executablefile
export GRASS_BATCH_JOB=$executablefile 

if [ -d "$Grassdir/World/National/" ]; then
    # run the job
    echo $Grassdir/World/National/
    grass64 -text $Grassdir/World/National/
else
    echo "---Fetching GRASS_data from S3---"
    mkdir $Grassdir
    s3cmd get s3://grass-data --recursive $Grassdir
    grass64 -text $Grassdir/World/National/	
fi

rm $executablefile

done

 
# switch back to interactive mode
unset GRASS_BATCH_JOB
