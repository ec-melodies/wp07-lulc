#!/usr/bin/env python
############################################################################
#
# MODULE:    r.in.landsat
# AUTHOR(S): Desertwatch-E consortium
#          Based on r.in.aster Python script for GRASS 
#          by Michael Barton and Glynn Clements
# PURPOSE:   Projects & imports Landsat (ETM7+TM5) imagery  using gdalwarp; 
#            Radiometric calibration; Cloud cover detection; NDVI and
#            TCbrightness
# COPYRIGHT: (C) 2010 by the GRASS Development Team
#
#   This program is free software under the GNU General Public
#   License (>=v2). Read I the file COPYING that comes with GRASS
#   for details.
#
#############################################################################


#%Module
#%  description: Projects and imports LANDSAT images (distributed by USGS) using gdalwarp and GRASS import functionalities. It also detects/eliminates clouds, produce NDVI, Tasseled Cap Brightness component, performs radiometric correction and normalize data.
#%  keywords: raster,national,import,landsat
#%End
#%option
#%  key: year
#%  type: integer
#%  description: Data of acquisition year:
#%  options: 1984-2050
#%  required: yes
#%end
#%option
#%  key: month
#%  type: integer
#%  description: Data of acquisition month:
#%  options: 1-12
#%  required: yes
#%end
#%option
#%  key: day
#%  type: integer
#%  description: Data of acquisition day:
#%  options: 1-31
#%  required: yes
#%end
#%option
#%  key: sunelevation
#%  type: double
#%  options: 0-90
#%  description: Sun elevation angle (deg):
#%  required: yes
#%end
#%option
#%  key: landsatsensor
#%  type: string
#%  description: Landsat satellite sensor:
#%  options: 5TM,7ETM,8OLI_TIRS
#%  required: yes
#%end
#%option
#%  key: inputb1
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 1-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb1
#%  type: double
#%  description: Band 1 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb1
#%  type: double
#%  description: Band 1 Spectral radiance at QCAL=QCALMAX (Lmax):
#%  required: yes
#%end
#%option
#%  key: inputb2
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 2-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb2
#%  type: double
#%  description: Band 2 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb2
#%  type: double
#%  description: Band 2 Spectral radiance at QCAL=QCALMAX (Lmax) :
#%  required: yes
#%end
#%option
#%  key: inputb3
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 3-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb3
#%  type: double
#%  description: Band 3 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb3
#%  type: double
#%  description: Band 3 Spectral radiance at QCAL=QCALMAX (Lmax):
#%  required: yes
#%end
#%option
#%  key: inputb4
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 4-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb4
#%  type: double
#%  description: Band 4 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb4
#%  type: double
#%  description: Band 4 Spectral radiance at QCAL=QCALMAX (Lmax):
#%  required: yes
#%end
#%option
#%  key: inputb5
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 5-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb5
#%  type: double
#%  description: Band 5 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb5
#%  type: double
#%  description: Band 5 Spectral radiance at QCAL=QCALMAX (Lmax):
#%  required: yes
#%end
#%option
#%  key: inputb6
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 6 /61 for Landsat-7ETM-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb6
#%  type: double
#%  description: Band 6 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb6
#%  type: double
#%  description: Band 6 Spectral radiance at QCAL=QCALMAX (Lmax):
#%  required: yes
#%end
#%option
#%  key: inputb7
#%  type: string
#%  gisprompt: old_file,file,input
#%  description: Raster input data (LANDSAT band 7-USGS GTiff) (Please change in file path the character "\" for "/"):
#%  required: yes
#%end
#%option
#%  key: Lminb7
#%  type: double
#%  description: Band 7 Spectral radiance at QCAL=0 (Lmin):
#%  required: yes
#%end
#%option
#%  key: Lmaxb7
#%  type: double
#%  description: Band 7 Spectral radiance at QCAL=QCALMAX (Lmax):
#%  required: yes
#%end
#%option
#%  key: output
#%  type: string
#%  description: Suffix for output raster data (<YEAR>_<bandid>_<suffix>_<SEASON>):
#%  required: yes
#%end
#%option
#%  key: season
#%  type: string
#%  description: Select season:
#%  options: Dry,Wet
#%  required: yes
#%end
#%flag
#%  description: Do NOT use Cloud detection and elimination module
#%  key: c
#% guisection: Cloud
#%end

import sys
import os
import platform
import grass.script as grass 
import time
import datetime
import math
import shlex

def main():
    #Get projection units
    proj_units=get_projection_units()

    # Define variables for National Scale
    t_srx= "30";  #Spatial Resolution in X for Locations with units in meters
    t_mapset= "National";  #Mapset's national Scale name

    # Retrieve variables from user interface
    year= options['year']
    month= options['month']
    day= options['day']   
    sunelevation= options['sunelevation']  
    landsatsensor= options['landsatsensor']
    input = [options['inputb1'], options['inputb2'],options['inputb3'],options['inputb4'],options['inputb5'],options['inputb7']]
    input_thermal= options['inputb6']
    input_cirrus= options['inputb1'].replace('_B2','_Bmask')
    season=options['season']    
    output_suf = options['output']
    flagcloud = flags['c']    
    metadatafile= os.path.dirname(options['inputb1']).replace('"\"', '/')+'/'+os.path.basename(options['inputb1'])[:-6]+'MTL.txt'
        
     
    #Check if output suffix is a valid string
    p=string_check(output_suf)
    if p==-1:
        grass.fatal(_("Illegal characters in inserted output suffix. Change suffix and try again."))
 
    # Define output (final and temporal)    
    output= [str(year),str(year),str(year),str(year),str(year),str(year)]
    for x in [0,1,2,3,4]:
          output[x]+="_band" + str(x+1)  +"_" + output_suf + "_" + season
    output[5]+="_band" + str(7) + "_" + output_suf + "_" + season
    output_t= ["B.1","B.2","B.3","B.4","B.5","B.7"]
     
    #Define List of Lmin and Lmax values    
    Lmin= [options['Lminb1'], options['Lminb2'],options['Lminb3'],options['Lminb4'],options['Lminb5'],options['Lminb7']]
    Lmax= [options['Lmaxb1'], options['Lmaxb2'],options['Lmaxb3'],options['Lmaxb4'],options['Lmaxb5'],options['Lmaxb7']]
    Lmin_thermal=options['Lminb6']
    Lmax_thermal=options['Lmaxb6']
 
    # Verify if input filepaths are valids and that if bands exists in file system
    band_id= [1,2,3,4,5,7]
    for x in [0,1,2,3,4,5]:
         p=path_check(input[x])
         if p==-1:         
              error_text= 'Band ' + str(band_id[x]) + ' file path is not valid. It includes some illegal characters. Review selected file path.'
              grass.fatal(_(error_text))                      
         check_file= os.path.isfile(input[x])
         if check_file==False:
              error_text= 'Band ' + str(band_id[x]) + ' file is not in file system. Please check if you switched \\ for /'
              grass.fatal(_(error_text))
    # Verify if Thermal pathfile is valid and if band exists in file system    
    p=path_check(input_thermal)
    if p==-1:         
        error_text= 'Band 6 (thermal) file path is not valid. It includes some illegal characters. Review selected file path.'
        grass.fatal(_(error_text))                      
    check_file= os.path.isfile(input_thermal)
    if check_file==False:
       error_text= 'Band 6 (thermal) file is not in file system. Please check if you switched \\ for /'
       grass.fatal(_(error_text))            
    # Retrieve current LOCATION and MAPSET
    source_location= grass.gisenv()['LOCATION_NAME']    
    source_mapset= grass.gisenv()['MAPSET']
 
    # Check if target mapset exists
    # list_mapsets=grass.mapsets(True)[0].split("newline")
    # if list_mapsets.__contains__(t_mapset)==False:           
        # grass.fatal("National Scale/Mapset does not exist or is not accessible. Please create a mapset named """ "National """ " using DWE-IS IntroPanel or edit Mapset access rights in Utilities/Mapset access.")
                 
    # Change to target Mapset
    if source_mapset != t_mapset:
        #Define target MAPSET as NATIONAL    
        p=grass.run_command("g.mapset", mapset = t_mapset, quiet=True)            
        if p!=0:
           grass.fatal(_("GRASS was unable to change to National mapset. Please review its existance and access rights."))        
         
    # Eliminates temporary files from current mapset    
    eliminate_rasterlists('myscript.tmp*', t_mapset)    
     
    # Eliminate, if exists, group of images with the same name    
    group_name= str(year) + "_" + output_suf    
    if len(grass.mlist_grouped('group', pattern=group_name))>0:       
       grass.run_command("g.remove", group=group_name, quiet=True, flags='f')
         
    #check whether gdalwarp is in path and executable
    if not grass.find_program('gdalwarp', ['--version']):
        grass.fatal(_("Gdalwarp is not in the path and executable. Try again and if the problem persists, please reinstall DWE-IS."))
 
    # Evaluate if year is a valid float
    try:
        int_check= int(year)
        year= int(year)
    except ValueError:
        grass.fatal(_("Value inserted for Year is not valid. Please insert a valid value between 1984 and 2050."))
 
    # Evaluate if month is a valid float
    try:
        int_check= int(month)
        month= int(month)
    except ValueError:
        grass.fatal(_("Value inserted for Month is not valid. Please insert a valid value between 1 (January) and 12 (December)."))
 
    # Evaluate if day is a valid float
    try:
        int_check= int(day)
        day= int(day)
    except ValueError:
        grass.fatal(_("Value inserted for Day is not valid.Please insert a valid value between 1 and 28-31 (depending on the year)."))
 
    # Evaluate if Sunelevation is a valid float
    try:
        float_check= float(sunelevation)
        sunelevation= float(sunelevation)
    except ValueError:
        grass.fatal(_("Value inserted for Sun elevation is not valid. Please try again with a valid value between 0 and 90."))
     
    # Evaluate if all Lmin (except thermal) values are valid floats
    for x in [0,1,2,3,4,5]:
        value= Lmin[x]
        try:
            float_check= float(value)           
            Lmin[x]= float(value)
        except ValueError:
           error_msg= "Value inserted for Lmin band " + str(band_id[x]) + " is not valid. Please review value."
           grass.fatal(_(error_msg))
 
    # Evaluate if all Lmax (except thermal) values are valid floats
    for x in [0,1,2,3,4,5]:
        value= Lmax[x]
        try:
            float_check= float(value)
            Lmax[x]= float(value)
        except ValueError:
           error_msg= "Value inserted for Lmax band " + str(band_id[x]) + " is not valid. Please review value."
           grass.fatal(_(error_msg))
 
    # Evaluate if  Lmin thermal value is a valid float    
    value= Lmin_thermal
    try:
       float_check= float(value)           
       Lmin_thermal= float(value)
    except ValueError:
       error_msg= "Value inserted for Lmin band 6 is not valid. Please review value."
       grass.fatal(_(error_msg))
 
    # Evaluate if Lmax thermal value is a valid float   
    value= Lmax_thermal
    try:
      float_check= float(value)
      Lmax_thermal= float(value)
    except ValueError:
      error_msg= "Value inserted for Lmax band 6 is not valid. Please review value."
      grass.fatal(_(error_msg))           
            
    # Calculate julian day
    try:
         julian_day= datetime.date(year,month,day)   
         julian_day= int(julian_day.strftime("%j"))
    except ValueError:
         grass.fatal(_("Inserted date is not valid. Please review year, month and day inserted values."))
 
    # Create the following parameters arrays: ESUN;Tasseled_cap parameters; K1 and K2 (for thermal band correction).
    if landsatsensor == '5TM':
        ESUN= [1958,1828,1559,1045,219.1,74.57]
        TC_params= [0.3037, 0.2793, 0.4343, 0.5585, 0.5082, 0.1863]
        K1=607.76
        K2=1260.56
        output_thermal_t="B.6"
    elif landsatsensor == '7ETM':
        ESUN= [1969,1840,1551,1044,225.7,82.07]
        TC_params= [0.3561, 0.3972, 0.3904, 0.6966, 0.2286, 0.1596]
        K1=666.09
        K2=1282.71                
        output_thermal_t="B.61"        
    elif landsatsensor.find('8OLI')>=0:
        ESUN= [1969,1840,1551,1044,225.7,82.07]           
        output_thermal_t="B.6"
        output_cirrus="B.9"         
 
    #Project/reproject and import landsat image except thermal      
    for x in [0,1,2,3,4,5]:
       try:    
            grass.message(_("Importing Landsat image %s .")%input[x])       
            import_landsat(input[x], output_t[x],band_id[x], source_location, t_srx, proj_units)    
 
       except:
            error_def(output_t,x, t_mapset)
            grass.fatal(_("DWE-IS was unable to import Landsat image %s. Please review selected input file and try again. \n Already imported images were deleted.")% input[x])
 
       #Define computational region
       try:
            if proj_units=="meters":       
                 grass.run_command("g.region", rast = output_t[x], res= t_srx)  
            else:
                 grass.run_command("g.region", rast = output_t[x])  
       except:
            eliminate_rasterlists('myscript.tmp*', t_mapset)                       
            error_def(output_t,x, t_mapset)           
            grass.fatal(_("GRASS is not able to define a computational region for imported files. Please review selected input file."))
                      
       #Perform DWEIS radiometric correction for Landsat 5 and 7 images 
       if landsatsensor.find('8OLI')<0:
           grass.message(_("Performing radiometric correction over LANDSAT band " + str(band_id[x])))  
           radiometric_calibration(output_t[x],band_id[x],landsatsensor ,sunelevation ,Lmin[x] ,Lmax[x], julian_day, ESUN[x], metadatafile)
 
    if not flagcloud:
        #Import of thermal band
        try:             
           import_landsat(input_thermal, output_thermal_t,6, source_location, t_srx, proj_units)          
        except:
           eliminate_rasterlists('myscript.tmp*', t_mapset)    
           error_def(output_t+[output_thermal_t],"thermal", t_mapset)
           grass.fatal(_("Error while importing Landsat images. Please review selected input files and try again. \n Already imported images were deleted."))
            
        #Import of Landsat8 QUALITY MASK       
        if landsatsensor.find('8OLI')>=0:
            try:             
               p=import_landsat(input_cirrus, output_cirrus,9, source_location, t_srx, proj_units)                         
            except:
               eliminate_rasterlists('myscript.tmp*', t_mapset)    
               error_def(output_t+[output_cirrus],"thermal", t_mapset)
               grass.fatal(_("Error while importing Landsat images. Please review selected input files and try again. \n Already imported images were deleted."))   
           
        #Calibration and calculation of Brightness temperature for thermal band    
        if landsatsensor.find('8OLI')<0:
            try:
               thermal_calibration(output_thermal_t,6,Lmin_thermal ,Lmax_thermal, K1,K2)         
            except:    
               eliminate_rasterlists('myscript.tmp*', t_mapset)        
               error_def(output_t+[output_thermal_t],"thermal", t_mapset)  
               grass.run_command("g.mremove", flags = "fe", quiet=True, rast="myscript.tmp")                     
               grass.fatal(_("Error while calibrating Landsat thermal band. Please review selected input files and try again. \n Already imported images were deleted."))
     
        #Cloud cover/shadow detection and elimination 
        if landsatsensor.find('8OLI')<0:
            output_band = output_thermal_t
        else:
            output_band = output_cirrus 
        try:
            if proj_units=="meters":    
               grass.run_command("g.region", rast = (output_t[0],output_t[1],output_t[2],output_t[3],output_t[4],output_t[5],output_thermal_t), res= t_srx)
            else:
               grass.run_command("g.region", rast = (output_t[0],output_t[1],output_t[2],output_t[3],output_t[4],output_t[5],output_thermal_t))    
        except:
            eliminate_rasterlists('myscript.tmp*', t_mapset)            
            error_def(output_t,"NDVI", t_mapset)      
            grass.fatal(_("GRASS is not able to define a computational region for imported files. Please review selected input file."))                
        try:
            cloud_detection(output_t,output_band,landsatsensor,season)
        except:
            eliminate_rasterlists('myscript.tmp*', t_mapset)                
            error_def(output_t,"NDVI", t_mapset)         
            grass.run_command("g.remove", flags = "f", quiet=True, rast=output_thermal_t)              
            grass.fatal(_("Error while Detecting and eliminating clouds. Please review selected input files and try again.\n Already imported images were deleted."))
    else:
        tempV= "myscript.tmpvalid" + str(os.getpid())    
        tempB= "myscript.tmpB" + str(os.getpid())   
        print "SO VEM PARA AQUI SE TIVER COM A FLAG PARA EXCLUIR O CLOUD PROCESSING" #DEBUG
        try:
            if proj_units=="meters":    
               grass.run_command("g.region", rast = (output_t[0],output_t[1],output_t[2],output_t[3],output_t[4],output_t[5]), res= t_srx)
            else:
               grass.run_command("g.region", rast = (output_t[0],output_t[1],output_t[2],output_t[3],output_t[4],output_t[5]))    
        except:
            eliminate_rasterlists('myscript.tmp*', t_mapset)            
            error_def(output_t,"NDVI_c", t_mapset)      
            grass.fatal(_("GRASS is not able to define a computational region for imported files. Please review selected input file."))                        
         
        try:
            grass.mapcalc("$tempV= if(($B1>=0 && $B2>=0 && $B3>=0 && $B4>=0 && $B5>=0 && $B7>=0),1,null())",tempV=tempV,B1=output_t[0],B2=output_t[1],B3=output_t[2],B4=output_t[3],B5=output_t[4],B7=output_t[5],B6=output_thermal_t)        
        except:
            eliminate_rasterlists('myscript.tmp*', t_mapset)            
            error_def(output_t,"NDVI_c", t_mapset)              
            grass.fatal(_("DWE-IS was unable to define a an area that is common to all LANDSAT bands.Please review selected input files."))
 
        #Cross bands with Valid area        
        for i in output_t:           
           try:
              grass.mapcalc("$output= $input",output=tempB, input=i)        
           except:
              eliminate_rasterlists('myscript.tmp*', t_mapset)            
              error_def(output_t,"NDVI_c", t_mapset)                         
              grass.fatal(_("DWE-IS was unable to clip Landsat bands.  Please review selected input files."))           
           try:    
              grass.mapcalc("$output= if(($valid==1),$input,null())",output=i, input=tempB, valid=tempV)
           except:
              eliminate_rasterlists('myscript.tmp*', t_mapset)            
              error_def(output_t,"NDVI_c", t_mapset)                                 
              grass.fatal(_("DWE-IS was unable to clip image. Please review selected input files."))                
        #Eliminate temporary raster        
        grass.run_command("g.remove", flags= 'f', rast = tempV, quiet=True)    
        grass.run_command("g.remove", flags= 'f', rast = tempB, quiet=True)    
 
    #Perform different radiometric correction for Landsat8 images - TOAR        
    if landsatsensor.find('8OLI')>=0:
       try:
           grass.message(_("Performing radiometric correction over LANDSAT " + landsatsensor))
           toar('B.','B.toar.',metadatafile)    #DEBUG
       except:
           grass.fatal("Unable to perform radiometric correction over LANDSAT " + landsatsensor)      
              
      
    #Normalize Reflectances
#     ndvi_out= str(year) + "_ndvi_" + output_suf + "_" + season 
    try:    
       grass.message(_("Normalizing reflectances..."))            
       p=normalize_reflectances(output_t,output, landsatsensor)     
       if p!=0:
           eliminate_rasterlists('myscript.tmp*', t_mapset)               
           error_def(output_t  + [ndvi_out],"TCB", t_mapset)
           if season=="Dry":       
              error_def2(output+ [tc_brightness],t_mapset)
           else:          
              error_def2(output+[ndvi_out],t_mapset)       
           grass.fatal(_("DWE-IS was unable to normalize LANDSAT bands reflectances. All images already created were deleted"))       
    except:    
       eliminate_rasterlists('myscript.tmp*', t_mapset)               
       error_def(output_t  + [ndvi_out],"TCB", t_mapset)
       if season=="Dry":       
           error_def2(output+ [tc_brightness],t_mapset)
       else:          
           error_def2(output+[ndvi_out],t_mapset)       
       grass.fatal(_("DWE-IS was unable to normalize LANDSAT bands reflectances. All images already created were deleted"))    
  
    # Calculate NDVI    
    grass.message(_("Calculating NDVI..."))            
    ndvi_out= str(year) + "_ndvi_" + output_suf + "_" + season    
    try:
        grass.mapcalc("$ndvi= ($band4 - $band3)/($band4 + $band3)", ndvi=ndvi_out, band3=output_t[2], band4=output_t[3]) 
        grass.run_command('r.colors', map = ndvi_out, color = 'ndvi', quiet=True)          
    except:   
       eliminate_rasterlists('myscript.tmp*', t_mapset)                    
       error_def(output_t ,"NDVI", t_mapset) 
       grass.fatal(_("DWE-IS was unable to produce NDVI map for imported LANDSAT images. Please review selected input files and try again. \n Imported Landsat bands were deleted."))    
      
    # Calculate TC-Brightness when dry season
    if season=="Dry" and landsatsensor.find('8OLI')<0:
       grass.message(_("Calculating Tasseled Cap- Soil Brightness..."))            
       tc_brightness= str(year) + "_TCbrightness_" + output_suf + "_" + season
       try:       
          grass.mapcalc("$TCbrig= ($tc1*$band1)+($tc2*$band2)+($tc3*$band3)+($tc4*$band4)+($tc5*$band5)+($tc7*$band7)", TCbrig=tc_brightness, band1=output_t[0], band2=output_t[1], band3=output_t[2],band4=output_t[3], band5=output_t[4], band7=output_t[5], tc1=TC_params[0], tc2=TC_params[1], tc3=TC_params[2], tc4=TC_params[3], tc5=TC_params[4], tc7=TC_params[5])       
          grass.run_command('r.colors', map = tc_brightness, color = 'grey', quiet=True)          
       except:
          eliminate_rasterlists('myscript.tmp*', t_mapset)           
          error_def(output_t  + [ndvi_out],"TCB", t_mapset)
          grass.fatal(_("DWE-IS was unable to produce Tasseled-Cap Brightness map for imported LANDSAT images. Please review selected input files and try again. \n NDVI map as well as imported Landsat bands were deleted."))       
  	   
  
    #Delete temporary output files (output_t)
    grass.run_command("g.remove", flags= 'f', rast = "B.1", quiet=True)   
    grass.run_command("g.remove", flags= 'f', rast = "B.2", quiet=True)       
    grass.run_command("g.remove", flags= 'f', rast = "B.3", quiet=True)   
    grass.run_command("g.remove", flags= 'f', rast = "B.4", quiet=True)   
    grass.run_command("g.remove", flags= 'f', rast = "B.5", quiet=True)   
    grass.run_command("g.remove", flags= 'f', rast = "B.7", quiet=True)  
         
    #Create group
    group_name= str(year) + "_" + output_suf + "_" + season
    p=grass.run_command("i.group", group=group_name, subgroup="subgroup", input= (output[0],output[1],output[2],output[3],output[4],output[5],[ndvi_out]), quiet=True)
    if p!=0:
       if season=="Dry":       
           error_def2(output+[ndvi_out]+[tc_brightness],t_mapset)
       else:    
           eliminate_rasterlists('myscript.tmp*', t_mapset)                         
           error_def2(output+[ndvi_out],t_mapset)       
       grass.fatal(_("Unexpected error while creating a group for imported images. Please review selected input files and try again. \n Imported images were deleted."))            
      
    #Apply color table
    for x in output:
        grass.run_command('r.colors', map = x, color = 'grey', quiet=True)                  
    grass.message(_(" "))
    grass.message(_(" "))
    grass.message(_(" "))
    grass.message(_("Landsat bands were imported into DWE-IS as well as derived products (eg NDVI)."))        
 
def normalize_reflectances(input, output, sensor): 
# # # # #This function is used to normalize data from 0-1 to 0-255
# # ( x - min(x) ) * smax / ( max(x) - min(x) ) + smin
    max=1
    min=0
    counter=0
    for x in input: 
        if sensor.find('8OLI')>=0:
           info = grass.read_command('r.info', flags='r', map=x)
           min=info[info.find('min=')+4:info.find('\n')].replace('\n','')
           max=info[info.find('max=')+4:].replace('\n','')
           try:
              grass.mapcalc("$out= round(($inp-"+min+")*255/("+max+"-"+min+"))", out=output[counter],inp=x)
           except:
              grass.fatal(_("DWE-IS was unable to normalize LANDSATs reflectance values to 0-255"))
           counter=counter+1   
        else: 
           try:
              grass.mapcalc("$out= round($inp*255)", out=output[counter],inp=x)
           except:
              return -1
              grass.fatal(_("DWE-IS was unable to normalize LANDSATs reflectance values to 0-255"))
           counter=counter+1
    return 0
        
def import_landsat(src_file, target_file, band, source_location, t_srx, proj_units):
# # # # #This function is used to reproject and import Landsat data
    # Landsat definitions
    no_value= "0"
    if band==6:
        t_srx=str(int(t_srx)*2)
     
    #create temporary file to hold gdalwarp output before importing to GRASS
    tempfile = grass.read_command("g.tempfile", pid = os.getpid()).strip() + '.tif'
 
    #get projection information from Landsat image
    p=proj_image = grass.read_command('g.proj', flags = 'jf', georef = src_file).strip()   	
    if proj_image==['']:
       grass.fatal(_("GRASS was unable to retrieve Raster projection and geographic information. . Please review if selected input image is a valid raster file."))
    
	#get projection information for current GRASS LOCATION
    if source_location == "World":
        proj_location= "+proj=longlat +datum=WGS84 +no_defs" #EPSG:4326
    elif source_location == "Portugal":
        proj_location= "+proj=tmerc +lat_0=39.66825833333333 +lon_0=-8.133108333333334 +k=1 +x_0=0 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +to_meter=1" #EPSG:3763
    elif source_location == "Brazil":
        proj_location= "+proj=utm +south +no_defs +zone=24 +a=6378137 +rf=298.257223563 +towgs84=0.000,0.000,0.000 +to_meter=1" #EPSG:32724
    elif source_location == "Mozambique":
        proj_location= "+proj=utm +south +no_defs +zone=36 +a=6378137 +rf=298.257223563 +towgs84=0.000,0.000,0.000 +to_meter=1" #EPSG:32736
    else: 
        proj_location = grass.read_command('g.proj', flags = 'jf').strip()    
		
    #run gdalwarp with selected options (must be in $PATH)
    if proj_image in proj_location:
        #import geotiff to GRASS
        p=grass.run_command("r.in.gdal", flags= 'ok', overwrite = 'o', input = src_file, output = target_file)      
        print 'grass.run_command("r.in.gdal", flags= ok, overwrite = o, input = '+src_file+', output = '+target_file+')'
        if p!=0:
           grass.fatal(_("GRASS was unable to import Landsat image. Please review selected input raster map and/or Locations Projection/Coordinate system."))
    else:
        if source_location == "World":
           proj_location= "EPSG:4326"
        elif source_location == "Portugal":
           proj_location= "EPSG:3763"
        elif source_location == "Brazil":                
           proj_location= "EPSG:32724"
        elif source_location == "Mozambique":
           proj_location= "EPSG:32736"
 
        #Get GRASS PATH
        gisbase = os.getenv('GISBASE')
        if not gisbase:
            grass.fatal(_('DWEIS+GRASS location not defined. Please uninstall DWE-IS tool and reinstall.'))        

        # Define path to GDAL18's gdalwarp
        # gdal18path= gisbase + '/gdal18'  #ORIGINAL
        gdal18path= '/usr/bin/'
        check_folder= os.path.isdir(gdal18path)
        if check_folder==False:
            grass.fatal(_('GDAL16 cannot be found in DWE-IS system. Please uninstall DWE-IS tool and reinstall.'))    
        # gdalwarppath= gdal18path + '/bin/' + 'gdalwarp.exe'   #ORIGINAL
        gdalwarppath= gdal18path +'gdalwarp'
        check_file= os.path.isfile(gdalwarppath)
        if check_file==False:
            grass.fatal(_('GDALWARP.exe from GDAL18 cannot be found in DWE-IS system. Please uninstall DWE-IS and reinstall.'))            
         
        # # Get current GDAL_DATA
        current_gdaldata=os.environ["GDAL_DATA"]

        # Define new GDAL_DATA                        
        # target_gdaldata= gisbase + '/gdal18/gdal/'   #ORIGINAL
        target_gdaldata= '/application/gdal/'		
        check_folder= os.path.isdir(target_gdaldata)
        print check_folder		
        if check_file==False:
            grass.fatal(_('GDAL18 GDAL_DATA folder cannot be found in DWE-IS system. Please uninstall DWE-IS tool and reinstall.'))            
        os.environ['GDAL_DATA']=target_gdaldata   
        grass.message(_("Projecting Landsat band using gdalwarp ..."))
        if proj_units=="meters":	
            cmd= "\"" + gdalwarppath + "\"" + ' -t_srs ' + "\"" + proj_location + "\"" + ' -srcnodata ' + no_value + ' -dstnodata ' + no_value  + ' -tr ' + t_srx + ' ' + t_srx + ' ' + src_file + ' ' + tempfile
        else:
            cmd= "\"" + gdalwarppath + "\"" + ' -t_srs ' + "\"" + proj_location + "\"" + ' -srcnodata ' + no_value + ' -dstnodata ' + no_value  + ' ' + src_file + ' ' + tempfile
        p = grass.call(shlex.split(cmd))	#for UNIX	
        # p = grass.call(cmd)    #for W32
        #check to see if gdalwarp executed properly
        if p!=0:        
           grass.fatal(_("GDAL was not able to reproject image to Location's coordinate system. Please review selected input raster map and/or Locations Projection/Coordinate system."))
        # GO to previous GDAL_DATA
        os.environ['GDAL_DATA']= current_gdaldata  
        #import geotiff to GRASS
        p=grass.run_command("r.in.gdal", flags= 'ok', overwrite = True, input = tempfile, output = target_file)
        if p!=0:
            grass.fatal(_("GRASS was unable to import Landsat image. Please review selected input raster map and/or Locations Projection/Coordinate system. "))
    #cleanup
    grass.try_remove(tempfile)
 
 
def toar(input_prefix,output_prefix, metadata):
    # Calculate TOAR
    grass.run_command("i.landsat.toar", input_prefix=input_prefix, output_prefix=output_prefix, metfile=metadata, quiet=True) 
    for i in [1,2,3,4,5,6,7]:
        tempR= "B.toar." + str(i)
        print tempR    
        grass.mapcalc("$raster_file= if($tempR < 0, null(), $tempR)", raster_file='B.'+str(i), tempR=tempR)
        grass.run_command("g.remove", flags= 'f', rast = tempR, quiet=True)            
         
def radiometric_calibration(raster_file, band_id, landsatsensor, sunelevation ,lmin ,lmax, julianday,esunvariable, metadata):
# # # # #This function is to perform radiometric calibration to Landsat data (except thermal band)
    QCALmin= 1
    QCALmax= 255
 
    #Create temporal files
    tempR= "myscript.tmpR" + str(os.getpid())
      
    #Calculate d + part of the equations      
    partial_rad = (lmax-lmin)/(QCALmax-QCALmin)
    d= 1+(0.0167*(math.sin((2*math.pi*(julianday-93.5))/365)))
    partial_refn= math.pi * pow(d,2)      
    partial_refd= esunvariable*math.cos(math.radians(90-sunelevation))       
 
    # Calculate Radiance+Reflectance
    try:
        grass.mapcalc("$tempR= (($lmin+($partial_rad*($DN-$QCALmin)))* $partial_refn)/$partial_refd", partial_refn=partial_refn, tempR=tempR, partial_refd=partial_refd, partial_rad=partial_rad, DN=raster_file,lmin=lmin,QCALmin=QCALmin)
        grass.mapcalc("$raster_file= if($tempR < 0, null(), $tempR)", raster_file=raster_file, tempR=tempR)
    except:
        grass.fatal(_("DWE-IS was not able to process radiometric calibration for band %s. Please review selected input file.")%str(band_id))
        #Eliminate temporary raster
    grass.run_command("g.remove", flags= 'f', rast = tempR, quiet=True)            
 
     
     
def thermal_calibration(raster_file, band_id, lmin ,lmax, K1,K2):
 # # # # #This function is to perform radiometric calibration to Landsat thermal band (6 in case of TM5 ans 61 in case of ETM+7)
    QCALmin= 1
    QCALmax= 255
     
    tempTb= "myscript.tmpTb"  + str(os.getpid())
    # Calculate/conversion  to at-sensor brightness temperature         
    try:
        grass.mapcalc("$output= $K2/log($K1/ ($lmin+ (($lmax-$lmin)/($QCALmax-$QCALmin))* ($raster_file-$QCALmin))+1)", output=tempTb, K2=K2, K1=K1,lmin=lmin, lmax=lmax, QCALmax=QCALmax, QCALmin=QCALmin, raster_file=raster_file)        
    except:
        grass.fatal(_("GRASS was unable to convert radiances to at-sensor brightness temperature. Please review selected input file."))     
     
    try:
        grass.mapcalc("$raster_file= if($temporary < 0, null(), $temporary)", raster_file=raster_file, temporary=tempTb)
    except:
        grass.fatal(_("GRASS was unable to convert radiances to at-sensor brightness temperature. Please review selected input file."))     
     
    #Eliminate temporary raster
    grass.run_command("g.remove", flags= 'f', rast = tempTb, quiet=True)    
 
     
def cloud_detection(output_t,output_thermal_t,landsatsensor,season):
# # # # #This function is used to perform cloud detection+regiongrowing+clipping
    #Create temporary map for cloud and shadows
    tempC= "myscript.tmpcloud" + str(os.getpid())
    #Create temporary map for valid areas
    tempV= "myscript.tmpvalid" + str(os.getpid())
    #Create temporary file
    tempB= "myscript.tmpB" + str(os.getpid())
     
    #Due to a shift between band 6 and the rest of the bands, it will be necessary to identify a valid area for all bands
    if landsatsensor.find('8OLI')>=0:
        try:
            grass.mapcalc("$tempV= if(($B1>=0 && $B2>=0 && $B3>=0 && $B4>=0 && $B5>=0 && $B7>=0),1,null())",tempV=tempV,B1=output_t[0],B2=output_t[1],B3=output_t[2],B4=output_t[3],B5=output_t[4],B7=output_t[5])
        except:
            grass.fatal(_("DWE-IS was unable to define a an area that is common to all LANDSAT bands.Please review selected input file."))
    else:
        try:
            grass.mapcalc("$tempV= if(($B1>=0 && $B2>=0 && $B3>=0 && $B4>=0 && $B5>=0 && $B7>=0 && $B6>=0),1,null())",tempV=tempV,B1=output_t[0],B2=output_t[1],B3=output_t[2],B4=output_t[3],B5=output_t[4],B7=output_t[5],B6=output_thermal_t)
        except:
            grass.fatal(_("DWE-IS was unable to define a an area that is common to all LANDSAT bands.Please review selected input file."))
     
     
    #Apply i.landsat.acca module according to landsat sensor type
    grass.message(_("Detecting clouds in Landsat images..."))    
    if landsatsensor == '5TM':
       p=grass.run_command("i.landsat.acca", input_prefix="B.", output=tempC, flags="f52", quiet=True)
       if p!=0:
          grass.fatal(_("Error while detecting clouds in Landsat 5TM images. Please review selected input files."))
    elif landsatsensor == '7ETM':
       p=grass.run_command("i.landsat.acca", input_prefix="B.", output=tempC, flags="f2", quiet=True)
       if p!=0:
          grass.fatal(_("Error while detecting clouds in Landsat 7ETM images. Please review selected input files."))
    elif landsatsensor.find('8OLI')>=0:
       #different method for landsat 8. Uses the quality band and selects pixels identified with clouds or cirrus clouds.        
       p=grass.mapcalc("$out=if($inp>0,1,null())", out=tempC, inp=output_thermal_t)
          
    # Check if cloud map has any detected cloud/shadow
    check_null=only_nulls(tempC)
    if check_null==-1:
        #Cross bands with  Valid area        
        for i in output_t:           
           try:
              grass.mapcalc("$output= $input",output=tempB, input=i)        
           except:
              grass.fatal(_("DWE-IS was unable to clip Landsat bands. Please review selected input file."))
           try:    
              grass.mapcalc("$output= if(($valid==1),$input,null())",output=i, input=tempB, valid=tempV)
           except:
              grass.fatal(_("DWE-IS was unable to clip image. Please review selected input files."))    
              
        #Eliminate temporary raster
        grass.run_command("g.remove", flags= 'f', rast = tempV, quiet=True)    
        grass.run_command("g.remove", flags= 'f', rast = tempC, quiet=True)        
        grass.run_command("g.remove", flags= 'f', rast = tempB, quiet=True)    
        grass.run_command("g.remove", flags= 'f', rast = output_thermal_t, quiet=True)          
  
    else:
        #Apply r.grow to detected clouds if not Landsat8
        if landsatsensor.find('8OLI')>=0:
            grass.message(_("Skipping r.grow for LANDSAT8 detected clouds..."))
        else:	
            p=grass.run_command("r.grow", input=tempC, output=tempC, overwrite=True, radius=5, old=1, new=1, metric="euclidean", quiet=True)    
            if p!=0:
               grass.fatal(_("Error while applying r.grow function to the detected clouds. Please review selected input files."))
  
        #Due to limitations in grass.mapcalc it is necessary to remove null values from valid and clouds
        p=grass.run_command("r.null", map=tempC, null=0)
        if p!=0:
           grass.fatal(_("Error while removing null values from Cloud map. Please review selected input files."))
        p=grass.run_command("r.null", map=tempV, null=0)
        if p!=0:
           grass.fatal(_("Error while removing null values. Please review selected input files."))
         
        #Cross bands with r.grow output and Valid area        
        grass.message(_("Eliminating clouds from calibrated Landsat bands..."))                
        for i in output_t:           
             
           try:
              grass.mapcalc("$output= $input",output=tempB, input=i)        
           except:
              grass.fatal(_("DWE-IS was unable to clip Landsat bands. Please review selected input files."))           
           try:    
              grass.mapcalc("$output= if(($valid==1 && $cloud!=1),$input,null())",output=i, input=tempB, valid=tempV,cloud=tempC)
           except:
              grass.fatal(_("DWE-IS was unable to aggregate detected cloud coverage with Landsat's band common covered area. Please review selected input files."))    
              
        #Eliminate temporary raster
        grass.run_command("g.remove", flags= 'f', rast = tempV, quiet=True)    
        grass.run_command("g.remove", flags= 'f', rast = tempC, quiet=True)        
        grass.run_command("g.remove", flags= 'f', rast = tempB, quiet=True)    
        #Eliminate Thermal band (6 in TM5 and 61 in ETM7)
        grass.run_command("g.remove", flags= 'f', rast = output_thermal_t, quiet=True)    
 
def only_nulls(input):
# # # # # Check if input is only composed by null values
    #0 =Is not only NULLS
    #-1 =Only nulls
    univar_output=grass.read_command("r.univar", map=input, flags="g")
    univar_output=univar_output.split('\n')   
    nullvalues= int((univar_output[1].split('='))[1])         
 
    nvalues= int((univar_output[2].split('='))[1])         
 
    if nullvalues-nvalues==0:
      return -1
    else:
      return 0        
 
 
def error_def(outpute,band_id, mapset):
# # # # # Function to eliminate temporary files when the processing chain catches some error
    if band_id=="NDVI":  
        for x in [0,1,2,3,4,5]:
            grass.run_command("g.remove", rast=outpute[x], flags='f')        
    elif band_id=="TCB":  
        for x in [0,1,2,3,4,5,6]:
            grass.run_command("g.remove", rast=outpute[x], flags='f')        
    elif band_id=="NDVI_c":
        for x in [0,1,2,3,4,5]:
            grass.run_command("g.remove", rast=outpute[x], flags='f')      
    elif band_id=="thermal": 
        for x in outpute:
            check_input=grass.find_file(x, element = 'cell', mapset=mapset)   
            if check_input['fullname'] !="":                  
               grass.run_command("g.remove", rast=x, flags='f')
    else:
        band_id=int(band_id)
        for x in [0,1,2,3,4,5]:                        
            if x<=band_id:
               grass.run_command("g.remove", rast=outpute[x], flags='f')
 
def error_def2(output, t_mapset):
# # # # # Function to eliminate output files when the processing chain catches some error
    for x in output:
       check_input= grass.find_file(x, element = 'cell', mapset=t_mapset)    
       if check_input['fullname'] !="":                  
          grass.run_command("g.remove", rast=x, flags='f')
 
def eliminate_rasterlists(pattern, cmapset):   
# # # # # Elilinate list of files that share a wildcard in its name
   p=grass.mlist_grouped ('rast', pattern=pattern)   
   check_existance= cmapset in p
   if check_existance:       
       temp_list=['']       
       raster_list= p[cmapset]
       for x in raster_list:
           temp_list.append(x)
       temp_list.remove('')
       nuldev = file(os.devnull, 'w+')           
       grass.run_command("g.remove", flags = "f", quiet=True, rast=temp_list, stderr = nuldev)             
       nuldev.close()            
   return 0                  
           
def get_projection_units():
# # # # # Get projection units
    proj_location = grass.read_command('g.proj', flags = 'jf').strip()    
    if "XY location (unprojected)"==proj_location:
        grass.fatal(_("This module needs to be run in a projected location (found: %s). Please change Location or Projection/Coordinates System.") % proj_location)
    location_param= proj_location.split(" ")
    if location_param.__contains__("+units=m")==True or location_param.__contains__("+proj=longlat")==False:           
        return "meters"
    else:
        return "other"
           
def string_check(text):
# # # # #Function to check if preffix string includes any invalid strings/characters
    if text=="0" or text==".":
       grass.fatal(_("Not valid filename"))
    check_charact=[]
    check_charact=check_charact+[text.find(".")]
    check_charact=check_charact+[text.find("myscript.tmp")]        
    check_charact=check_charact+[text.find("~")]        
    check_charact=check_charact+[text.find("/")]
    check_charact=check_charact+[text.find("\\")]
    check_charact=check_charact+[text.find("\"")]
    check_charact=check_charact+[text.find("\'")]
    check_charact=check_charact+[text.find(" ")]            
    check_charact=check_charact+[text.find("@")]
    check_charact=check_charact+[text.find(",")]    
    check_charact=check_charact+[text.find(";")]    
    check_charact=check_charact+[text.find(":")]    
    check_charact=check_charact+[text.find("=")]
    check_charact=check_charact+[text.find("!")]    
    check_charact=check_charact+[text.find("?")]
    check_charact=check_charact+[text.find("%")]
    check_charact=check_charact+[text.find("$")]    
    check_charact=check_charact+[text.find("#")]    
    check_charact=check_charact+[text.find(">")]            
    check_charact=check_charact+[text.find("?")]        
    check_charact=check_charact+[text.find("{")]
    check_charact=check_charact+[text.find("}")]    
    check_charact=check_charact+[text.find("[")]
    check_charact=check_charact+[text.find("]")]        
    check_charact=check_charact+[text.find("+")]
    check_charact=check_charact+[text.find("*")]                    
    check_charact=check_charact+[text.find("-")]
    check_charact=check_charact+[text.find("&")]
    check_charact=check_charact+[text.find("%")]    
    check_charact=check_charact+[text.find("subclass")]        
    check_charact=check_charact+[text.find("LULC")]            
    check_charact=check_charact+[text.find("__")]                
    check_charact=check_charact+[text.find("ndvi")]                    
    check_charact=check_charact+[text.find("B.")]            
     
    if max(check_charact)!=-1:
        return -1
    else:
        return 0               
 
def path_check(text):
# # # # #Function to check if file path includes any invalid strings/characters
    check_charact=[]
    check_charact=check_charact+[text.find("\\")]
    check_charact=check_charact+[text.find("\"")]
    check_charact=check_charact+[text.find("\'")]
    check_charact=check_charact+[text.find(" ")]            
    check_charact=check_charact+[text.find("@")]
    check_charact=check_charact+[text.find(",")]    
    check_charact=check_charact+[text.find(";")]    
    check_charact=check_charact+[text.find("=")]
    check_charact=check_charact+[text.find("~")]        
    check_charact=check_charact+[text.find("!")]    
    check_charact=check_charact+[text.find("?")]
    check_charact=check_charact+[text.find("%")]
    check_charact=check_charact+[text.find("$")]    
    check_charact=check_charact+[text.find("#")]    
    check_charact=check_charact+[text.find(">")]            
    check_charact=check_charact+[text.find("?")]        
    check_charact=check_charact+[text.find("{")]
    check_charact=check_charact+[text.find("}")]    
    check_charact=check_charact+[text.find("[")]
    check_charact=check_charact+[text.find("]")]        
    check_charact=check_charact+[text.find("+")]
    check_charact=check_charact+[text.find("*")]        
    check_charact=check_charact+[text.find("&")]
    check_charact=check_charact+[text.find("%")]
 
    if max(check_charact)!=-1:
        return -1
    else:
        return 0     
         
if __name__ == "__main__":
    options, flags = grass.parser()
    main()
