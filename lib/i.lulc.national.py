#!/usr/bin/env python
############################################################################
#
# MODULE:    i.lulc.national
# AUTHOR(S): Desertwatch-E consortium
#
# PURPOSE:   Produce NATIONAL LULC map
#
# COPYRIGHT: (C) 2010 by the GRASS Development Team
#
#   This program is free software under the GNU General Public
#   License (>=v2). Read I the file COPYING that comes with GRASS
#   for details.
#
#############################################################################


#%Module
#%  description: Produces Land Use/Cover map for national scale based on LANDSAT images and defined training areas.
#%  keywords: raster,national,lulc,landsat
#%End
#%option
#%  key: input1st
#%  type: string
#%  multiple: yes
#%  gisprompt: old,cell,raster
#%  description: Name of input raster data- Image1 (LANDSAT) (from National scale/mapset):
#%  required: yes
#%end
#%option
#%  key: input2nd
#%  type: string
#%  multiple: yes
#%  description: Name of input raster data- Image2 (LANDSAT) (from National scale/mapset):
#%  gisprompt: old,cell,raster
#%  required: yes
#%end
#%option
#%  key: output
#%  type: string
#%  description: Prefix for output raster data (<prefix>_LULC):
#%  required: yes
#%end


import grass.script as grass 
import sys
import os

def main():
    #Get projection units
    proj_units=get_projection_units()
    
    # Define variables for National scale
    t_srx= "30";  #Spatial Resolution in X for Locations in meters
    t_mapset= "National";  #Mapset's Natioal Scale name

     # Retrieve variables from user interface
    input1 = options['input1st'].split(",")
    input2 = options['input2nd'].split(",") 
    input= input1 + input2
    output_pre = options['output']
	
    # Define output files
    output= output_pre + '_LULC' 
    output_label= output + 'label'
	
	# Define temporary files
    pid= str(os.getpid())	
    output_t= "myscript.tmp" + pid
    output_r= "myscript.tmpreclass" + pid
    NDVItemp1= "myscript.tmp_ndvi1" + pid
    NDVItemp2= "myscript.tmp_ndvi2" + pid
    mask_train= "myscript.tmpmask__t" + pid
    national_mask= "myscript.tmpnatmask" + pid

	#Check if output preffix is a valid string
    p=string_check(output_pre)
    if p==-1:
        grass.fatal(_("Illegal characters in inserted output preffix. Change preffix string and try again."))
		
    #Check if the user as selected 7 bands per image    
    if len(input1)!=7:
       grass.fatal(_("User must select 7 bands for image 1 (input1st). Please review selected input files."))
    if len(input2)!=7:
       grass.fatal(_("User must select 7 bands for image 2 (input2nd). Please review selected input files."))

    # Retrieve current LOCATION, GISDBASE and MAPSET
    source_location= grass.gisenv()['LOCATION_NAME']    
    source_GISDBASE= grass.gisenv()['GISDBASE']    
    source_mapset= grass.gisenv()['MAPSET']

    # Check if target mapset exists
    # list_mapsets=grass.mapsets(True)[0].split("newline")
    # if list_mapsets.__contains__(t_mapset)==False:           
        # grass.fatal("National Scale/Mapset does not exist or is not accessible. Please create a mapset named """ "National """ " using DWE-IS IntroPanel or edit Mapset access rights in Utilities/Mapset access.")
					
    # Change to target Mapset
    if source_mapset != t_mapset:
    	#Define target MAPSET as REGIONAL    
        p=grass.run_command("g.mapset", mapset = t_mapset, quiet=True)        	
        if p!=0:
            grass.fatal(_("GRASS was unable to change to National Mapset/Scale. Please review its existance and access rights"))		 

    #Eliminate temporary files from current MAPSET
    eliminate_rasterlists('myscript.tmp*', t_mapset)
    eliminate_rastermaps([NDVItemp1,NDVItemp2])
    eliminate_rasterlists('subclass*', t_mapset)    	
    
    # Verify if all input data exist in the correct mapset/scale
    for x in input:
       if x.find('@')==-1:	
           x=x + '@National'
       else:
           if x[x.find('@')+1:]!='National':           
                grass.fatal(_("Raster %s not available in National mapset. Please review selected input files.")%x)
       check_input= grass.find_file(x, element = 'cell', mapset=t_mapset)    
       if check_input['fullname'] =="":           
           grass.fatal(_("Raster " + x + " not available in National mapset. Please review selected input files."))        

    #grass.message("o input e: " + str(input))
		   
    #Eliminate group of images (if exists)	
    group_name= "lulc_national"
    check_group= grass.find_file(group_name, element = 'group', mapset=t_mapset)    	   	
    if check_input['fullname'] !="":	            
        grass.run_command("g.remove", group=group_name, flags="f", quiet=True)

    #Eliminate classes_t + subclases + training_map  + final maps with the same name
    eliminate_rastermaps(['trainingmap'])		
    eliminate_rasterlists('*__t*', t_mapset)    
    eliminate_rastermaps([output_label,output])		    
	
    #Verify/Identify which band is NDVI from each image and its index
    band_ndvi1=ndvi_identifier(input1)
    if band_ndvi1==-1:
        grass.fatal(_("First image (input1st) must include a NDVI map. Please review selected input files."))		        
    band_ndvi1_idx= input.index(band_ndvi1)
    band_ndvi2=ndvi_identifier(input2)
    if band_ndvi2==-1:
        grass.fatal(_("Second image (input2nd) must include a NDVI map. Please review selected input files."))		        
    band_ndvi2_idx= input.index(band_ndvi2)

    # normalize NDVI
    grass.message(_("Normalizing NDVI bands in order to be used in LULC processing chain..."))
    p=ndvi_normalizer(band_ndvi1, NDVItemp1, t_srx, proj_units)
    if p==-1:
           eliminate_rastermaps([NDVItemp1])		            
           grass.fatal(_("Unable to normalize NDVI map from image 1. Please review selected input files."))		        
    
    p=ndvi_normalizer(band_ndvi2, NDVItemp2, t_srx,proj_units)
	# export NDVI from the dry season to tif
    dryndvitif='./wp07-lulc/GRASS_data/'+band_ndvi2.replace('@'+t_mapset,'')+'.tif'
    grass.message("Converting NDVI from the dry season to tif: "+str(dryndvitif))		
    grass.run_command("r.out.gdal", input=NDVItemp2, output=dryndvitif)	
    if p==-1:
            eliminate_rastermaps([NDVItemp1,NDVItemp2])		
            grass.fatal(_("Unable to normalize NDVI map from image 2. Please review selected input files."))		            

    #Substitute NDVIfiles in input
    input[band_ndvi1_idx]=NDVItemp1
    input[band_ndvi2_idx]=NDVItemp2

    #Create group and path to sig folder	
    p=grass.run_command("i.group", group=group_name, subgroup="subgroup", input=input, quiet=True)
    if p!=0:  
        eliminate_rastermaps([NDVItemp1,NDVItemp2])	        
        grass.fatal(_("Unexpected error while creating a group for National Scale images. Please retry and if the error persists, reintall DWE-IS."))	
    # sig_path= source_GISDBASE + "\\" + source_location + "\\" +t_mapset + "\\" + "group" + "\\" + group_name + "\\" + "subgroup" + "\\" + "subgroup" + "\\" + "sig"    #Win32
    sig_path= source_GISDBASE + "/" + source_location + "/" +t_mapset + "/" + "group" + "/" + group_name + "/" + "subgroup" + "/" + "subgroup" + "/" + "sig"     #UNIX

	
    # Define computational region
    try:	
        if proj_units=="meters":		
            grass.run_command("g.region", rast = input, res= t_srx)
        else:
            grass.run_command("g.region", rast = input)	
    except:
        grass.fatal(_("GRASS is not able to define a computational region for LULC process. Please review selected input images."))

    #Identify preliminary valid sub-Classes   
    classes= select_classes(t_mapset, source_location,"vector")
    #grass.message(_("DEBUG1: " + str(classes)))
    if classes=='':
       eliminate_rastermaps([NDVItemp1,NDVItemp2])		
       eliminate_rasterlists('myscript.tmp*', t_mapset)    
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		   	   
       grass.fatal(_("Not possible to produce LULC National scale map. No training areas were find in National Mapset/Scale."))	      

    # Eliminate training values that have NULL values in raster maps    	    
    check_mask= mask_training(classes,input, mask_train,t_mapset)
    #grass.message(_("DEBUG2: " + str(classes)))		
    if check_mask==-1:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)	 			   
       grass.fatal(_("Not possible to eliminate null values from training areas. Please review defined training areas."))

    # Create final list of existing classes
    classes= select_classes(t_mapset, source_location,"raster")
    #grass.message(_("DEBUG3: " + str(classes)))		
    if classes=='':
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)	 			   		     
       grass.fatal(_("Not possible to produce LULC National scale map. No training areas were find in National Mapset/Scale."))	   

    #Apply  outliers detection and cleaning of training sample + Check if are invertible
    grass.message(_("Applying outliers detection & elimination procedure over each available training area..."))	
    idx=0
    classes_t=[""]
    #grass.message(_("DEBUG3.5: " + str(classes)))	
    for x in classes:
       # Generate signature
       p=grass.run_command("i.gensig", group=group_name, subgroup="subgroup", trainingmap=x, signaturefile=x, overwrite=True, quiet=True)
       grass.message(_("A processar classe: " + str(x)))	   
       if p!=0:
          eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
          eliminate_rasterlists('*__t', t_mapset)    
          eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
          grass.run_command("g.remove", group=group_name, flags="f", quiet=True)
          # grass.message(_("DWE-IS was not able to calculate Training areas statistics for " + x + ". Please review selected input files and available subclasses." ))	  #DEBUG      	   		  
          grass.fatal(_("DWE-IS was not able to calculate Training areas statistics for " + x + ". Please review selected input files and available subclasses." ))	        	   
		   
       #Verify if signature is valid
       sig_validation=check_sig(x,sig_path)
       if sig_validation==0:
          #Detect and eliminate outliers
          t_class= x + '__t'
          classes_t= classes_t + [t_class]
          #grass.message(_("Para estar a aqui o SIG file e valido:"))		  
          #try:
            #grass.mapcalc("$output= $input", output=t_class, national=national_mask, input=x)		#DEBUG - This skips outlier detection which is crucial  
          #except:
            #p=-1
          p=grass.run_command("i.outdetect.exe", group=group_name, subgroup="subgroup", overwrite=True, sigfile=x, class_out=t_class, original=x, verbose=True)
          # p=0		  
          if p!=0:
             eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
             eliminate_rasterlists('*__t', t_mapset)    
             eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
             grass.run_command("g.remove", group=group_name, flags="f", quiet=True)
             grass.fatal(_("DWEIS was not able to apply outliers detection and cleaning of training sample for " + x + ". Please review selected images and available training areas."))	   
       else:
          grass.warning(_("DWEIS was not able to generate a valid signature file for " + x + ". After the process please review subclass vector map and selected input images."))
	
    #Re-check if class has valid values after the outliers detection and cleaning of training sample
    eliminate_rastermaps(classes)
    classes=recheck_classes(classes_t)

    if classes=='' or len(classes)==0:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  		   	   
       grass.fatal(_("Outliers detection and cleaning training sample eliminated all pixels from training areas. This means that the process will be interrupted. Please redefine training areas."))

    if len(classes)==1:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  		   	     	   
       grass.fatal(_("DWE-IS cannot classify images based only in a single training subclass. Please include more subclasses vectorials in National scale/mapset."))
	   
	# Print list of valid subclasses
    grass.message(_("The following subclasses will be used as Training areas\n"))
    for x in classes:
       msg_subclass= "Sub_class ID: " + x[:-3]
       grass.message(_(msg_subclass))	   
    
    #Create trainingmap
    grass.message(_("Creating training map and signature file..."))
    p=grass.run_command("r.patch",input=classes, output="trainingmap", quiet=True)
    if p!=0:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  		   	     	   	   
       grass.fatal(_("GRASS was unable to create a training map for the indicated classes. Please retry or review selected input images."))

    #Eliminate subclasses training raster maps
    eliminate_rastermaps(classes)
	   
    # Recode training map
    gisbase = os.getenv('GISBASE')    
    if not gisbase:		
        eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t"])	
        eliminate_rasterlists('*__t', t_mapset)    
        eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
        grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  		   	   
        grass.fatal(_('For some reason DWE-IS and GRASS is not being able to find a recode table for producing training areas signatures. Try again and if the problem persists, please reinstall DWE-IS.'))
    else:	
        recode_path= "./wp07-lulc/symbology/recode"
        print recode_path		#Debug
        check_file= os.path.isfile(recode_path)	
        print "recode check is: " + str(check_file)   #Debug
        if check_file==False:
            eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t","trainingmap"])	
            eliminate_rasterlists('*__t', t_mapset)    
            eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
            grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  		   	     	
            grass.fatal(_('DWE-IS was not able to find recode file to be applied to the Training areas map. Try again and if the problem persists, please reinstall DWE-IS.'))		
        p=grass.run_command("r.category", map="trainingmap", quiet=True, rule=recode_path)
        if p!=0:
            eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t","trainingmap"])	
            eliminate_rasterlists('*__t', t_mapset)    
            eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
            grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  	
            grass.fatal(_('DWE-IS was not able to apply recode file to the Training areas map. Try again and if the problem persists, please reinstall DWE-IS.'))		

    #Generate signature file
    p=grass.run_command("i.gensig", group=group_name, subgroup="subgroup", signaturefile=group_name, trainingmap="trainingmap", overwrite=True, quiet=True)

    if p!=0:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t","trainingmap"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)		  	
       grass.fatal(_("GRASS was unable to generate a signature file for the training map. Please review selected input images and available training areas."))

    #Verify if signature is valid
    sig_validation=check_sig(group_name,sig_path)	   
    if sig_validation!=0:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t","trainingmap"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)
       grass.fatal(_("Provided training areas generated an invalid covariance matrix. Please review selected input images."))	

    # Apply i.ldc
    grass.message(_("Running Linear Discriminant Classifier..."))
    p=grass.run_command("i.ldc.exe", group=group_name, subgroup="subgroup", sigfile=group_name, class_out=output_t, overwrite=True, verbose=True)
    # p=grass.run_command("i.maxlik", group=group_name, subgroup="subgroup", sigfile=group_name, _class=output_t, overwrite=True, quiet=True)   #DEBUG	
    if p!=0:
       eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t","trainingmap"])	
       eliminate_rasterlists('*__t', t_mapset)    
       eliminate_rasterlists('myscript.tmp*', t_mapset)    	   
       grass.run_command("g.remove", group=group_name, flags="f", quiet=True)
       grass.fatal(_("DWE-IS was unable to classify selected images. Please review selected input images."))	

    #Eliminate group + trainingmap + classes_t + normalized ndvi
    eliminate_rastermaps([NDVItemp1,NDVItemp2,"mask_map__t","trainingmap"])	
    eliminate_rasterlists('*__t', t_mapset)    	
    grass.run_command("g.remove", group=group_name, flags="f", quiet=True)   

    #Apply Reclass
    reclass_path= source_GISDBASE + "/" + source_location + "/" +t_mapset + "/" + ".tmp/reclass17classes"
    p=write_reclassfile(reclass_path,classes)
    if p==-1:
        eliminate_rastermaps([output_t])
        grass.fatal(_('For some reason DWE-IS and GRASS is not being able to find reclass table for National Scale maps. Try again and if the problem persists, please reinstall DWE-IS.'))
    check_file= os.path.isfile(reclass_path)
    if check_file==False:
        eliminate_rastermaps([output_t])
        grass.fatal(_("Reclass table is not available. Try again and if the problem persists, please reinstall DWE-IS."))			
    grass.message(_("Reclassifying from 17 subclasses to 11 DW-E classes..."))
    # grass.run_command("r.out.gdal", input=output_t, output="lulc17classes.tif")	   #DEBUG	
    p=grass.run_command("r.reclass", input=output_t,output=output_r,rules=reclass_path, overwrite=True)		
    if p!=0:
        eliminate_rastermaps([output_t])
        grass.fatal(_("Not possible to reclassify National Scale map to DW-E 11 classes. Try again and if the problem persists, please reinstall DWE-IS."))	   			    

    # Check if PERMANENT mapset exists
    # list_mapsets=grass.mapsets(True)[0].split("newline")	
    # if list_mapsets.__contains__('PERMANENT')==True:           
       # check_input= grass.find_file('National', element = 'vector', mapset='PERMANENT')    	
       # if check_input['fullname'] !="":
          # no_region=False
       # else:
          # no_region=True
    # else:
    no_region=True			
    # Only produce map inside National boundaries.
    if no_region!=True:
       p=grass.run_command("v.to.rast", input="National@PERMANENT", output=national_mask, use="val", value=1, overwrite=True, quiet=True)       
       try:	   	   
          grass.mapcalc("$output= if(($national>0), $input, null())", output=output, national=national_mask, input=output_r)
		  
       except:
          grass.warning(_("DWE-IS was unable to restrict LULC output map for the defined country area (National in PERMANENT mapset). Please review selected input file and/or National vector map."))	 	
          try:
             grass.mapcalc("$out= $input", out=output, input=output_r)
          except:
             eliminate_rastermaps([output_r])  	
             eliminate_rastermaps([output_t])  
             eliminate_rasterlists('myscript.tmp*', t_mapset)    	  		  			 
             grass.fatal(_("DWE-IS was not able to create 11-classes LULC map. Please review selected input images and/or training classes."))		  
    else:	   	   
       grass.warning(_("DWE-IS was unable to restrict LULC output map for the defined country area (National in PERMANENT mapset). Please review selected input file and/or National vector map."))	 		
        #Create a copy of reclassified map
       try:
          grass.mapcalc("$out= $input", out=output, input=output_r)
       except:
          eliminate_rastermaps([output_r])  	
          eliminate_rastermaps([output_t])  	
          eliminate_rasterlists('myscript.tmp*', t_mapset)    	  		  
          grass.fatal(_("DWE-IS was not able to create 11-classes LULC map. Please review selected input images and/or training classes."))		
    
	#Eliminate temporary files + Reclass file
    eliminate_rastermaps([output_r])  	
    eliminate_rastermaps([output_t])		
    eliminate_rasterlists('myscript.tmp*', t_mapset)    	   	
	
    try:
       os.remove(reclass_path)
    except OSError:
       grass.warning(_("GRASS was not able to delete temporary reclass table."))
    
    label_check=1
    #Create label output
    if not gisbase:
        label_check=0
        grass.warning(_('For some reason DWE-IS and GRASS is not being able to find DWE-IS installation folder. Land Use/Cover product with labels can not be produced.'))           
        grass.warning(_('DWE-IS is not able to find DWE-IS Reclass file. Land Use/Cover product with labels can not be produced.'))              			
    else:
        label_path= "./wp07-lulc/symbology/" + "labels_reclass" 
        check_file= os.path.isfile(label_path)    					
        if check_file==True:
            p=grass.run_command('r.reclass', input=output, output=output_label, rules=label_path, quiet=True)	
            if p!=0:
                label_check=0
                grass.warning(_('For some reason DWE-IS able to apply DWE-IS Reclass file. Land Use/Cover product with labels can not be produced.'))                                         
        else:
            label_check=0		
            grass.warning(_('For some reason DWE-IS able to find DWE-IS Reclass file. Land Use/Cover product with labels can not be produced.'))              	
	   
	# Apply Color map to LULC raster map    
    if not gisbase:
        grass.warning(_('For some reason DWE-IS and GRASS is not being able to find DWE-IS folder so it is not able to apply DWE color table. Try again and if the problem persists, please reinstall DWE-IS.'))
        grass.warning(_('DWE-IS is not able to find DWE-IS color table file. Try again and if the problem persists, please reinstall DWE-IS.'))              		
        grass.run_command('r.colors', map = output, rules = "grey", quiet=True)	
        grass.run_command('r.colors', map = output_label, rules = "grey", quiet=True)			
    else:
        color_path= "./wp07-lulc/symbology/color/dwecolor" 
        check_file= os.path.isfile(color_path)    			
        if check_file==True:
            p=grass.run_command('r.colors', map = output, rules = color_path, quiet=True)
            if p!=0:			
                grass.warning(_('For some reason DWE-IS was not able to apply DWE-IS LULC color table to LULC map. You can apply a color table manually.'))                              												
            if label_check==1:				
                 p=grass.run_command('r.colors', map = output_label, rules = color_path, quiet=True)						
                 if p!=0:			
                     grass.warning(_('For some reason DWE-IS was not able to apply LULC color table to LULC_label map. You can apply a color table manually.'))                              									
        else:
            grass.warning(_('For some reason DWE-IS and GRASS is not being able to find DWE-IS color table file. Try again and if the problem persists, please reinstall DWE-IS.'))              
            grass.run_command('r.colors', map = output, rules = "grey", quiet=True)	
            if label_check==1:							
                grass.run_command('r.colors', map = output_label, rules = "grey", quiet=True)			

		
    grass.message(_(" "))
    grass.message(_(" "))
    grass.message(_(" "))
    grass.message(_("National scale LULC was produced with the name " + output + ". \n"))


def mask_training(classes,band,mask_raster,t_mapset):        
# # # # # Function to create a mask and to eliminate, from training areas, pixels that are not valid
    p=grass.run_command('r.series', flags="n", input=band, method="count", output=mask_raster, quiet=True)   
    #grass.message(_("DEBUG7: masking trainning classes " + str(classes)))		
    if p!=0:
       return -1		
  
    for x in classes:
        classvalue=x[-2:]
        try:
            classvalue= int(classvalue)
        except ValueError:
            return -1
        try:
            output_name= x + '__t'
            #grass.message(_("DEBUG7.1: output " + str(output_name)))
            grass.mapcalc("$output_subclass= if(($subclass==$class_value & $mask_band>=1),$class_value)", output_subclass=output_name, class_value=classvalue, subclass=x, mask_band=mask_raster)
        except:
            return -1      
        eliminate_rastermaps(x)	
        p=grass.run_command('g.rename', rast = (output_name, x), quiet=True, overwrite=True)
        if p!=0:
            return -1
    eliminate_rasterlists('*__t', t_mapset)	
    eliminate_rastermaps([mask_raster])	
    return 1

	
def write_reclassfile(tmp_path,classes):    
# # # # # Because GRASS does not recognize classes IDs, it is necessary to recode Classification input classes IDs to DW-E IDs.
    text_file= open(tmp_path, "w")
    text_file.write("0 = NULL\n")
    cell_value=0
    for x in classes:

  
       cell_value=cell_value+1
       subclass_id=x[-5:-3]    

       class_id=get_11class(int(subclass_id))  
       if class_id==-1:

          return -1
       text_file.write( str(cell_value) +" = " + str(class_id) + "\n")
    text_file.write("* = NULL\n")
    text_file.close()
    return 0
	
def get_11class(subclass):
# # # # # Reclass from 17 subclasses to 11 DW-E classes
    if subclass==1:
       return 1
    elif subclass==2:
       return 2
    elif subclass==3:
       return 3
    elif subclass==4:
       return 3
    elif subclass==5:
       return 2
    elif subclass==6:
       return 2
    elif subclass==7:
       return 2
    elif subclass==8:
       return 4
    elif subclass==9:
       return 4
    elif subclass==10:
       return 4	   
    elif subclass==11:
       return 6	   
    elif subclass==12:
       return 5	   
    elif subclass==13:
       return 9	   
    elif subclass==14:
       return 7	   
    elif subclass==15:
       return 8	   
    elif subclass==16:
       return 10
    elif subclass==17:
       return 11  	 
    else:
       return -1	


def check_sig(x,sig_path):
    total_path= sig_path + "/" + x
    #First check if file exists
    check_file= os.path.isfile(total_path)
    if check_file==False:	
       return -1

    # now read file and count lines (more than 1)
    fd = open(total_path)
    lcounter=0
    while 1:
        line = fd.readline()
        lcounter=lcounter+1
        if not line:
           break
    if lcounter>16:   #This valus considers that we will always use 14 bands plus some lines to include some possible character error
        return 0
    else:
        return -1      
    
	
def ndvi_normalizer(input, output, t_srx, proj_units):
# # # # # Function to normalize NDVI maps
    if proj_units=="meters":	
        p=grass.run_command("g.region", rast = input, res= t_srx)
    else:
        p=grass.run_command("g.region", rast = input)        
    if p!=0:
        return -1
    try:
        grass.mapcalc("$out= round(127.5*($input+1))", out=output, input=input)
    except:    
        return -1	
    return output

def ndvi_identifier(input):
# # # # # Function to identify NDVI maps
    id=-1
    for x in input:
       temp1=x.find('ndvi') 	   
       temp2=x.find('NDVI') 	   	   
       if temp1!=-1 or temp2!=-1:
          id=x
    return id

def select_classes(mapset, location,classes_format):  
# # # # # Function to identify, evaluate and convert to raster, when applicable, each subclass
    
    all_classes=['subclass01','subclass02','subclass03','subclass04','subclass05','subclass06','subclass07','subclass08','subclass09','subclass10','subclass11','subclass12','subclass13','subclass14','subclass15','subclass16','subclass17']          

    if classes_format=='vector':
         element_id= "vector"
    elif classes_format=='raster':
         element_id="cell"

    valid_classes=[]
    for x in all_classes:        
        #Verify if exists in current mapset/location
        #grass.message("A verificar se a classe " + str(x) + " existe no mapset: " + str(mapset) + " e na location: " + str(location)) 		#DEBUG
        check_input= grass.find_file(x, element = element_id, mapset=mapset)    		
        if check_input['fullname'] !="":    
            if classes_format=='vector':
                # Retrieve raster final raster value				
                value=class_value(x)   
                #Convert training areas (vector to raster)			
                p=grass.run_command("v.to.rast", input=x, output=x, use="val", value=value, overwrite=True, quiet=True)       
                if p!=0:
                   grass.fatal(_("DWE-IS was not able to convert %s training area to raster map. Please review available training areas."),x)           		   
		
            #Verify if it has any valid values
            check_valid= valid_class(x)	
            if check_valid==0:
              valid_classes=valid_classes + [x]
            else:
              eliminate_rastermaps([x])			
 
    return valid_classes

def class_value(input):
# # # # # Retrieve class INT value from subclass filename
    value=int(input[8:])
    return value	
    	
	
def valid_class(input):
    #0  =has valid values
    #-1 =doesn't have any valid values
    #grass.message(_("DEBUG8: output " + str(input)))
    univar_output=grass.read_command("r.univar", map=input, flags="g")
    if 	univar_output=="":
      return -1
    else:	  
        #grass.message(_("DEBUG8.1: output " + str(univar_output)))
        univar_output=univar_output.split('\n')
        nullvalues= int((univar_output[1].split('='))[1])    
        nvalues= int((univar_output[2].split('='))[1])    
        if nvalues==nullvalues:
          return -1
        else:
          return 0
	  
def recheck_classes(iclasses):
# # # # # Check valid classes
    oclasses=[]
    idx=0
    for i in iclasses:
       check_valid= valid_class(i)
       if check_valid==0:
          oclasses= oclasses+ [i]
          idx=idx+1

    return oclasses

def get_projection_units():
# # # # # Function to retrieve Location's Geo Units
    proj_location = grass.read_command('g.proj', flags = 'jf').strip()	
    if "XY location"==proj_location:
        grass.fatal(_("This module needs to be run in a projected location (found: %s)") % proj_location)
    location_param= proj_location.split(" ")
    if location_param.__contains__("+units=m")==True or location_param.__contains__("+proj=longlat")==False:           
        return "meters"
    else:
        return "other"


def eliminate_rasterlists(pattern, cmapset):  
# # # # # Eliminate raster maps without having to print warnings in Command output 
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
 			
def eliminate_rastermaps(raster_list):
# # # # # Eliminate raster maps without having to print warnings in Command output
    temp_list=['']
    for x in raster_list:
       p=grass.mlist_grouped('rast', pattern=x)	
       if len(p)>0:
            temp_list.append(x)	
    temp_list.remove('')
    nuldev = file(os.devnull, 'w+')			
    if len(temp_list)>0:
        grass.run_command("g.remove", flags = "f", quiet=True, rast=temp_list, stderr = nuldev)
    nuldev.close()
    return 0	
	
def string_check(text):
# # # # #Function to check if preffix string includes any invalid strings/characters
    if text=="0" or text==".":
       return -1
    check_charact=[]
    check_charact=check_charact+[text.find(".")]
    check_charact=check_charact+[text.find("~")]		
    check_charact=check_charact+[text.find("/")]
    check_charact=check_charact+[text.find("myscript.tmp")]	
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
	
if __name__ == "__main__":
    options, flags = grass.parser()
    main()
