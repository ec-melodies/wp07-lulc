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

def getlandsats(years,tiles,outputdir):
	seasonintervals=['0101-0630','0701-0730']
	LandsatDownloadProgdir ='/home/melodies-wp7/LANDSAT-Download/'
	logfile = os.path.join(outputdir,'log.txt')
	downloaded=[]
	for tile in tiles:
		for year, bird in years.iteritems():
			for season in seasonintervals:
				startdate=year+season.split('-')[0]
				enddate=year+season.split('-')[1]
				print "Search interval: " + startdate + " to " +enddate + " - Bird: " + bird
				subprocess.call('python '+LandsatDownloadProgdir+'download_landsat_scene.py -z unzip -b '+bird+' -o scene -d '+startdate+' -f '+enddate+' -c 5 -s '+tile+' -u '+LandsatDownloadProgdir+'usgs.txt --output '+outputdir, shell=True)
				l = open(logfile,'r')
				images=l.read().translate(None, "\n[]")
				if images!='':		
					downloaded.append(images)

	return downloaded		
		
