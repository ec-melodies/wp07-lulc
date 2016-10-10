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
export usgsfile=/data/usgs.txt
export variablesfile=/application/variables.txt
export proxyfile=/data/proxy.txt
export Landsat_download=$Landsat_download
export PATH=$anaconda:$Bin:$Lib:$Extlib:$Landsat_download:$Starspan:$Landsat_LDOPE:$PATH
export PYTHONPATH=$Lib:$anaconda
export LD_LIBRARY_PATH=/usr/local/lib/otb
export GDAL_DATA=/application/gdal

# read some variables from variables.txt
while IFS='' read -r line || [[ -n "$line" ]]; do
            if [[ $line == *"non_grass_outputpath"* ]]; then
               export outputpath=${line:21}
            fi
			if [[ $line == *"proxy_user"* ]]; then
               export proxy_user=${line:11}
            fi
			if [[ $line == *"proxy_passwd"* ]]; then
               export proxy_passwd=${line:13}
            fi
			if [[ $line == *"proxy_host"* ]]; then
               export proxy_host=${line:11}
            fi
			if [[ $line == *"proxy_port"* ]]; then
               export proxy_port=${line:11}
            fi	
			if [[ $line == *"usgs_user"* ]]; then
               export usgs_user=${line:10}
            fi
			if [[ $line == *"usgs_passwd"* ]]; then
               export usgs_passwd=${line:12}
            fi				
done < $variablesfile

#syncronize final data files
echo "---Syncronizing files with S3 storage---"
mkdir ${outputpath//\'/} -p
s3cmd -f sync s3://final-data ${outputpath//\'/} --skip-existing

#create images folder and needed files
mkdir $imagesfld -p
if [ ! -f $imagesfld/log.txt ]; then
    echo -e " " > $imagesfld/log.txt
fi
echo -e "$usgs_user $usgs_passwd" > $usgsfile
echo -e "$proxy_user $proxy_passwd\n$proxy_host\n$proxy_port" > $proxyfile

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
rm $usgsfile
rm $proxyfile

done

 
# switch back to interactive mode
unset GRASS_BATCH_JOB
