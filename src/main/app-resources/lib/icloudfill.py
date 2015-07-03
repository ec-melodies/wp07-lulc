#!/usr/bin/env python

import sys
import os
import platform
import grass.script as grass 

def cloudfill(output_suf, year, tile, logpath):
    #check if job was done before
    if os.path.isfile(os.path.join(logpath,year + "_" + output_suf +tile)): 
        print "Skipping cloudfill processing. Job was already done before!"
        return

    #get all bands names
    output_wet= []
    for x in ['1','2','3','4','5','ndvi','7']:
        if x=='ndvi':
            output = year + "_" + x +"_" + output_suf +tile+ "_Wet"
            output_wet.append(output)
        else:
            output = year +"_band" + x  +"_" + output_suf +tile+ "_Wet"
            output_wet.append(output)			
    output_dry= []
    for x in ['1','2','3','4','5','ndvi','7']:
        if x=='ndvi':
            output = year + "_" + x +"_" + output_suf +tile+ "_Dry"
            output_dry.append(output)
        else:
            output = year +"_band" + x  +"_" + output_suf +tile+ "_Dry"
            output_dry.append(output)	
			
    #run the loops for dry and wet seasons
    for idx, band in enumerate(output_wet):	
        grass.message("Filling clouds in " + band + " with data from " + output_dry[idx])
        try:
            grass.mapcalc("$tempV= if(isnull($Bwet),$Bdry,$Bwet)",tempV='tempV',Bwet=band,Bdry=output_dry[idx])
            grass.mapcalc("$Bwet= $tempV",tempV='tempV',Bwet=band)
            grass.run_command("g.remove", flags= 'f', rast = 'tempV', quiet=True)			
        except:
            grass.message('ERROR')

    for idx, band in enumerate(output_dry):	
        grass.message("Filling clouds in " + band + " with data from " + output_wet[idx])
        try:
            grass.mapcalc("$tempV= if(isnull($Bwet),$Bdry,$Bwet)",tempV='tempV',Bwet=band,Bdry=output_wet[idx])
            grass.mapcalc("$Bwet= $tempV",tempV='tempV',Bwet=band)
            grass.run_command("g.remove", flags= 'f', rast = 'tempV', quiet=True)			
        except:
            grass.message('ERROR')			
    
    open(os.path.join('/application/logs/',year + "_" + output_suf +tile), 'a')