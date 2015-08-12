#!/usr/bin/env python
############################################################################
#
# MODULE:    i.lulc.national
# AUTHOR(S): MELODIES WP7 team
#
# PURPOSE:   Produce cloud-free Landsat images
#
# COPYRIGHT: (C) 2014 by the GRASS Development Team
#
#   This program is free software under the GNU General Public
#   License (>=v2). Read I the file COPYING that comes with GRASS
#   for details.
#
#############################################################################

import os, imp
import subprocess
from download_landsat_scene import getmetadatafiles

def getVarFromFile(filename):
    import imp
    f = open(filename)
    global data
    data = imp.load_source('', '', f)
    f.close()	

#READ VARIABLES
dirname=os.path.dirname
appdir=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
variablesfile= os.path.join(appdir,'variables.txt')
getVarFromFile(variablesfile)
image_path=data.image_path
credentialsfile = data.usgscredentialsfile

getmetadatafiles(image_path,'update')

#subprocess.call('download_landsat_scene.py -z unzip -o catalog -d 20000101 -f 20000102 -k update -s 180031 -u '+credentialsfile+' --output '+image_path+' --outputcatalogs '+image_path, shell=True)
	
