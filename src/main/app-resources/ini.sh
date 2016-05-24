#!/bin/bash

# define variables
Grassdir=/data/GRASS_data
imagesfld=/data/images
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

#create images folder and needed files
mkdir $imagesfld -p
if [ ! -f $imagesfld/log.txt ]; then
    echo -e " " > $imagesfld/log.txt
fi
if [ ! -f /data/usgs.txt ]; then
    echo -e "criticalsoftware csw123456" > /data/usgs.txt
fi
if [ ! -f /data/proxy.txt ]; then
    echo -e "Me Security\nasinara.terradue.com\n3128" > /data/proxy.txt
fi

#syncronize final data files
while IFS='' read -r line || [[ -n "$line" ]]; do
            if [[ $line == *"non_grass_outputpath"* ]]; then
               export outputpath=${line:21}
            fi
done < "/application/variables.txt"

s3cmd sync s3://final-data ${outputpath//\'/} 

#run job for each tile
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
