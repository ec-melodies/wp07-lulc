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

landsat_download_home = os.environ['Landsat_download']
passwfile = os.path.join(landsat_download_home,'usgs.txt')

subprocess.call('download_landsat_scene.py -z unzip -o catalog -d 20000101 -f 20000102 -k update -s 180031 -u '+passwfile+' --output c:\\', shell=True)
	
