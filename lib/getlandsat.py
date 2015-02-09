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

def Calculate_season(image_aquisition,region):
    if region=='Portugal':
        if 173<int(image_aquisition[13:16])<295:
            season='Dry'
        else:
            season='Wet'
    # print season		
    return season

def checkseasonimg(year,season,tile,dir):
    all=os.listdir(dir)
    dirs=[]
    imagefound=''
    for f in all:
        if os.path.isdir(os.path.join(dir,f))==True:
            dirs.append(f)
    # print dirs			
    for img in dirs:
        tile_img=img[3:9]		
        year_img=img[9:13]
        season_img=Calculate_season(img,'Portugal')
        if year_img==year and season_img==season and tile_img==tile:
            imagefound=img
            break
    if imagefound!='':
        return imagefound	
    else:
        return None


def getlandsats(years,tiles,admitedcloudcover,outputdir):
    if admitedcloudcover==None:
        admitedcloudcover=''
    else:
        admitedcloudcover=' -c '+admitedcloudcover
    seasonintervals=['0101-0630','0701-0730']
    landsat_download_home = os.environ['Landsat_download']
    passwfile = os.path.join(landsat_download_home,'usgs.txt')
	# LandsatDownloadProgdir ='/home/melodies-wp7/LANDSAT-Download/'   #Unix
    logfile = os.path.join(outputdir,'log.txt')
    downloaded=[]
    for tile in tiles:
        for year, bird in years.iteritems():
            for season in seasonintervals:
                # print season		#DEBUG	
                if season=='0101-0630':
                    season_ext='Wet'
                elif season=='0701-0730':
                    season_ext='Dry'
                # print season_ext    #DEBUG
                checkexists=checkseasonimg(year,season_ext,tile,outputdir)
                # print checkexists	
                if checkexists!=None:
                    print "Bingo! There is already an image in the output directory with year, tile and season corresponding to what you're searching: "+checkexists+". Skiping.."
                    downloaded.append(checkexists)					
                else:
                    startdate=year+season.split('-')[0]
                    enddate=year+season.split('-')[1]
                    print "Search interval: " + startdate + " to " +enddate + " - Bird: " + bird
                    subprocess.call('download_landsat_scene.py -z unzip -b '+bird+' -o scene -d '+startdate+' -f '+enddate+admitedcloudcover+' -s '+tile+' -u '+passwfile+' --output '+outputdir, shell=True)
                    l = open(logfile,'r')
                    images=l.read().translate(None, '\n[]\'')
                    if images!='':		
                        downloaded=downloaded+images.split(',')
    return list(set(downloaded))		
