#!/usr/bin/python
 
import os,sys,datetime,imp
import grass.script as grass
import grass.script.setup as gsetup
import urllib
from Gdalfunctions import *
from otbfunctions import * 
from getlandsat import * 

#get start time
starttime=datetime.datetime.now()

#READ VARIABLES
dirname=os.path.dirname
appdir=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
variablesfile= os.path.join(appdir,'variables.txt')
def getVarFromFile(filename):
    import imp
    f = open(filename)
    global data
    data = imp.load_source('', '', f)
    f.close()
getVarFromFile(variablesfile)
gisbase = data.gisbase
gisdbase = data.gisdbase
location = data.location
fetchtiles = data.fetchtiles
years = data.years
mapset   = data.mapset
image_path=data.image_path
admitedcloudcover = data.admitedcloudcover
imagelist = data.imagelist
if imagelist=='':
    imagelist=getlandsats(years,fetchtiles,admitedcloudcover,image_path)
# print imagelist   #DEBUG
output=data.output
color_path= os.path.join(dirname(__file__),'symbology','data_lulc_trends_legend2d')
reclass_path= os.path.join(dirname(__file__),'symbology','reclass_lucc')
MMU = data.MMU
spatialr = data.spatialr
maxiter = data.maxiter
ranger = data.ranger
threshold = data.threshold
minsize = data.minsize
tilesize = data.tilesize
simplify = data.simplify
non_grass_outputpath = data.non_grass_outputpath
filelist=non_grass_outputpath + '/filelist.txt'

def read_landsat_metadata(image_path,image_name):
    output_list=[]
    fields = ['DATE_ACQUIRED',
        'SUN_ELEVATION',
        'RADIANCE_MAXIMUM_BAND_1',
        'RADIANCE_MINIMUM_BAND_1',
        'RADIANCE_MAXIMUM_BAND_2',
        'RADIANCE_MINIMUM_BAND_2',
        'RADIANCE_MAXIMUM_BAND_3',
        'RADIANCE_MINIMUM_BAND_3',
        'RADIANCE_MAXIMUM_BAND_4',
        'RADIANCE_MINIMUM_BAND_4',
        'RADIANCE_MAXIMUM_BAND_5',
        'RADIANCE_MINIMUM_BAND_5',
        'RADIANCE_MAXIMUM_BAND_6',
        'RADIANCE_MINIMUM_BAND_6',
        'RADIANCE_MAXIMUM_BAND_7',
        'RADIANCE_MINIMUM_BAND_7']
    sensor=[]
    metadatafile= os.path.join(image_path,image_name,image_name + '_MTL.txt')
    metadata = open(metadatafile, 'r')
    # metadata.replace('\r','')	
    for line in metadata:
        line = line.replace('\r', '')	
        if line.find('SENSOR_ID')>=0:
            sensor.append(line[line.find('= ')+2:])
        if line.find('SPACECRAFT_ID')>=0:
            sensor.append(line[line.find('= ')+2:])
        for f in fields:
            if line.find(f)>=0:
                lineval = line[line.find('= ')+2:]
                output_list.append(lineval.replace('\n',''))
    sensortype = sensor[0][len(sensor[0])-3:]+sensor[1]
    sensortype = sensortype.replace('\n','').replace('"','')	
    output_list.append(sensortype)
    tile=image_name[3:9]
    output_list.append(tile)
    # print output_list   #DEBUG
    return output_list
 
def image_bands(image_path,image_name,sensortype):
    output_band_list=[]
    if sensortype=='5TM':
        for b in range(1,8):
            band= image_path.replace('/', urllib.quote('/')) + image_name + urllib.quote('/')+ image_name + '_B'+str(b)+'.TIF'
            output_band_list.append(band)
    elif sensortype.find('8OLI')>=0:
        for b in [2,3,4,5,6,10,7,'QA']:
            band= image_path.replace('/', urllib.quote('/')) + image_name + urllib.quote('/')+ image_name + '_B'+str(b)+'.TIF'
            output_band_list.append(band)
    elif sensortype.find('7ETM')>=0:
        for b in [1,2,3,4,5,'6_VCID_1',7]:
            band= image_path.replace('/', urllib.quote('/')) + image_name + urllib.quote('/')+ image_name + '_B'+str(b)+'.TIF'
            output_band_list.append(band)			
    return output_band_list
 
def get_lulc_files(mapset, pattern):
    fu = grass.read_command("g.mlist", type = 'rast', mapset = mapset, pattern=pattern)
    lulcfiles=[]
    filename='' 
    for filen in fu:
        if filen!='\n':
            filename=filename+filen
        else:
            lulcfiles.append(filename)
            filename=''
    return lulcfiles           
 
def applycolormap(color_path, output):       
    # Apply Color map to LULC raster map    
    if not gisbase:
        grass.warning(_('For some reason DWE-IS and GRASS is not being able to find DWE-IS folder so it is not able to apply DWE color table. Try again and if the problem persists, please reinstall DWE-IS.'))
        grass.warning(_('DWE-IS is not able to find DWE-IS color table file. Try again and if the problem persists, please reinstall DWE-IS.'))                      
        grass.run_command('r.colors', map = output, rules = "grey", quiet=True)            
    else:
        check_file= os.path.isfile(color_path)                
        if check_file==True:
            p=grass.run_command('r.colors', map = output, rules = color_path, quiet=True)
            if p!=0:            
                grass.warning(_('For some reason DWE-IS was not able to apply DWE-IS LULC color table to LULC map. You can apply a color table manually.'))                                                                                                                                           
        else:
            grass.warning(_('For some reason DWE-IS and GRASS is not being able to find DWE-IS color table file. Try again and if the problem persists, please reinstall DWE-IS.'))              
            grass.run_command('r.colors', map = output, rules = "grey", quiet=True)    
 
def applyreclass(reclass_path, inp, outp):
    #Apply Reclass
    check_file= os.path.isfile(reclass_path)
    if check_file==False:
        grass.warning(_("Reclass table is not available. Try again."))            
    grass.message(_("Reclassifying..."))            
    p=grass.run_command("r.reclass", input=inp,output=outp,rules=reclass_path, overwrite=True)        
    if p!=0:
        grass.warning(_("Not possible to reclassify. Try again."))     

def generalize_lulc(lulcmap,gen_lulcmap,mmu,skipmajfilter):
    grass.message(_("Generalizing " + str(lulcmap))) 
    # Define computational region
    try:	
        grass.run_command("g.region", rast = lulcmap)	
    except:
        grass.fatal(_("GRASS is not able to define a computational region. Please review selected input images."))
    if skipmajfilter==False:
        temp2='temp2'	
        grass.run_command("r.neighbors",input=lulcmap, output=temp2, size='3', method='mode', overwrite=True)
        lulcmap=temp2		
    if mmu>0:
        if skipmajfilter==True:
            temp=gen_lulcmap
        else:			
            temp='temp'	
        grass.run_command("r.reclass.area", input=lulcmap, output=temp, greater=mmu, quiet=True, overwrite=True)
    else:
        temp=lulcmap
    if skipmajfilter==False:		
        grass.run_command("r.neighbors",input=temp, output=gen_lulcmap, size='3', method='mode', overwrite=True)		
 
def landsat8_QAmask(inputQAband):
    inputQAmask=inputQAband.replace("QA","mask")
    try:
        with open(inputQAmask) as f: pass
        print inputQAmask + ' already exists, skipping mask creation...'		
    except: 
        print os.system("unpack_oli_qa --ifile="+inputQAband+" --ofile="+inputQAmask+" --fill --cloud=high --cirrus=high --combine")
  
 
#Setup Grass GISbase, GISdbase, location and mapset
gsetup.init(gisbase,
            gisdbase, location, mapset)

#IMPORT AND PRE-PROCESS LANDSAT IMAGES FROM imagelist
imported=[]
yearofimportedimgs=[]  
tiles=[]        
for img in imagelist:
    output_l=read_landsat_metadata(image_path,img)
    output_band_list=image_bands(image_path,img,output_l[len(output_l)-2])
    if output_l[len(output_l)-2].find('8OLI')>=0:
        # run QA mask for landsat 8
        inputQAband = output_band_list[7]  
        landsat8_QAmask(inputQAband)
    season = Calculate_season(img,'Portugal')
    output=output+output_l[len(output_l)-1]
    print output_band_list[0]
    name_in_grass=output_l[0][0:4]+'_band_'+output+'_'+season+'@'+mapset
    fu = grass.find_file(element = 'cell', name = name_in_grass.replace('band','band2'))
    if fu.get('fullname')=='':
        grass.run_command("r.in.landsat.new.py", 
                          year=output_l[0][0:4], 
                          month=output_l[0][5:7], 
                          day=output_l[0][8:10], 
                          sunelevation=output_l[1], 
                          landsatsensor=output_l[len(output_l)-2], 
                          inputb1=output_band_list[0], 
                          Lminb1=output_l[3], 
                          Lmaxb1=output_l[2], 
                          inputb2=output_band_list[1], 
                          Lminb2=output_l[5], 
                          Lmaxb2=output_l[4], 
                          inputb3=output_band_list[2], 
                          Lminb3=output_l[7], 
                          Lmaxb3=output_l[6], 
                          inputb4=output_band_list[3], 
                          Lminb4=output_l[9], 
                          Lmaxb4=output_l[8], 
                          inputb5=output_band_list[4], 
                          Lminb5=output_l[11], 
                          Lmaxb5=output_l[10], 
                          inputb6=output_band_list[5], 
                          Lminb6=output_l[13], 
                          Lmaxb6=output_l[12], 
                          inputb7=output_band_list[6], 
                          Lminb7=output_l[15], 
                          Lmaxb7=output_l[14], 
                          output=output, 
                          season=season)
    imported.append(name_in_grass)
    if output_l[0][0:4] not in yearofimportedimgs:
        yearofimportedimgs.append(output_l[0][0:4])
    if output_l[len(output_l)-1] not in tiles:
        tiles.append(output_l[len(output_l)-1])
    output=data.output
 
#CHECK FOR WET AND DRY SEASON AND GENERATE LANDCOVER MAP IF VALID
generatedlulc=[]
generatedgenlulc=[]
generatedlulctifs=[]
cont=0
for t in tiles:
    cont=cont+1
    grass.message("Processing image " + str(cont) + " out of " + str(len(tiles)))
    for y in yearofimportedimgs:
        output=data.output+t+'_'+y
        # print imported    #DEBUG
        valid_seasons_imgs=0
        name_dry = None
        name_wet = None		
        for imported_img in imported:
            # print imported_img	   #DEBUG
            print str(valid_seasons_imgs)
            if imported_img.find('Dry')>=0 and imported_img.find(t)>=0 and imported_img.find(y)>=0 and name_dry == None:
                    name_dry=imported_img
                    valid_seasons_imgs=valid_seasons_imgs+1
            if imported_img.find('Wet')>=0 and imported_img.find(t)>=0 and imported_img.find(y)>=0 and name_wet == None:
                    name_wet=imported_img
                    valid_seasons_imgs=valid_seasons_imgs+1
        fu = grass.find_file(element = 'cell', name = output+'_LULC@'+mapset)
        if valid_seasons_imgs>=2 and fu.get('fullname')=='':
            p=grass.read_command("i.lulc.national.py", 
                              input1st=[name_wet.replace('band','band1'), 
                                        name_wet.replace('band','band2'), 
                                        name_wet.replace('band','band3'), 
                                        name_wet.replace('band','band4'), 
                                        name_wet.replace('band','band5'), 
                                        name_wet.replace('band','ndvi'), 
                                        name_wet.replace('band','band7')], 
                              input2nd=[name_dry.replace('band','band1'), 
                                        name_dry.replace('band','band2'), 
                                        name_dry.replace('band','band3'), 
                                        name_dry.replace('band','band4'), 
                                        name_dry.replace('band','band5'), 
                                        name_dry.replace('band','ndvi'), 
                                        name_dry.replace('band','band7')], 
                              output=output)
            # append generated lulc's to a list which will be processed further			
            generatedlulc = get_lulc_files(mapset, data.output+t+"*_LULC")
            if p!=0 and output+'_LULC' not in generatedlulc:
                generatedlulc.append(output+'_LULC')
        elif valid_seasons_imgs<2:
            grass.message(_("Two seasons must be available to generate LULC map for tile "+t+" and year "+y))      
        elif fu.get('fullname')!='':
            generatedlulc = get_lulc_files(mapset, data.output+t+"*_LULC")	
            grass.message(_("File already in mapset. Skipped generating LULC map for tile "+t+" and year "+y))

        #GENERALIZATION
        all_gens = grass.find_file(element = 'cell', name = output+'_LULC_gen@'+mapset)
        generatedlulc = get_lulc_files(mapset, data.output+t+"*_LULC")
        for lulcmap in generatedlulc:	
            gen_lulcmap= lulcmap.strip()+'_gen'	
            #print all_gens.get(lulcmap)	
            if all_gens.get('fullname')=='':
                try:			
                    generalize_lulc(lulcmap,gen_lulcmap,int(MMU),False)
                    generatedgenlulc.append(gen_lulcmap)
                except:
                    grass.warning(_("Unable to generalize "+lulcmap))				
            else:
                generatedgenlulc.append(gen_lulcmap)			
		
    #SEGMENTATION AND INTEGRATION OF LULC  
    grass.message(_("Segmenting LULC raster map..."))           
    if len(generatedgenlulc)>=1:
        for lulcmap in generatedgenlulc:
            #EXPORT LULC MAP OUT OF GRASS
            lulcmaptif=os.path.join(non_grass_outputpath,lulcmap+'.tif')
		    # Define computational region
            try:	
                grass.run_command("g.region", rast = lulcmap)	
            except:
                grass.fatal(_("GRASS is not able to define a computational region for LULC process. Please review selected input images."))
            #Check if tif already on disk
            try:
                with open(lulcmaptif) as f: pass
            except: 
                grass.run_command("r.out.gdal", input=lulcmap, output=lulcmaptif)
            generatedlulctifs.append(lulcmaptif)				
            #Define variables for next steps
            vect_out=lulcmaptif.replace('.tif', '_segm.shp')
            mask=lulcmaptif.replace('.tif', '_mask.tif')
            output_stats=lulcmaptif.replace('.tif', '_sts')
            driver = ogr.GetDriverByName('ESRI Shapefile')
            dataSource = driver.Open(vect_out, 0)	
            #Segmentation			
            if dataSource!=None:
                grass.message(_("Segmented map already exists. Skipping the segmentation process..."))
            else:   
                #create a mask
                try:
                    with open(mask) as f: pass
                except:					
                    subprocess.call('gdal_calc.py -A ' + lulcmaptif + ' --A_band 1 --outfile=' + mask + ' --calc="A>0" --overwrite', shell=True)
                #perform segmentation GRASS 7
#                 grass.run_command("i.segment", group='te', output='lixolcover_sgm', threshold='0.6', minsize=minsize)
                #perform segmentation		
                s=otbsegmentation(lulcmaptif,mask,spatialr,maxiter,ranger,threshold,minsize,tilesize,simplify,vect_out)
    			#clean vector in grass
                grass.message(_("Cleaning segments in GRASS..."))
                checksegm = grass.find_file(element = 'vector', name = lulcmap+'_segm')
                if checksegm.get('fullname')=='':
                      grass.run_command("v.in.ogr", dsn=vect_out, output=lulcmap+'_segm', snap='0.0002')
                try:
                    with open(vect_out) as f: pass
                    remove_shapefile(vect_out)
                    grass.run_command("v.out.ogr", input=lulcmap+'_segm', type='area', dsn=vect_out)				
                except: 
    				grass.message(_("Skipping cleaning segments..."))	
            summary_table=output_stats+'_summary.csv'
            if os.path.exists(summary_table)==False and dataSource!=None:		
                #integrate raster values in segments
                grass.message(_("Integrating segments and raster LULC values..."))
                #calculate areas and id for each segment				
                calculateidandareas(vect_out)			
                subprocess.call('starspan --vector '+vect_out +' --raster ' + lulcmaptif + ' --out-prefix ' +  output_stats + ' --out-type table --nodata 0 --skip_invalid_polys --elapsed_time --mask '+mask +' --summary-suffix _summary.csv --stats mode --fields ID --noColRow --noXY --RID none', shell=True)
                # integratesegmentationandraster (lulcmaptif,summary_table,vect_out)
                #join
                join_segments_and_csv(vect_out,summary_table)
                subprocess.call('ogr2ogr -overwrite ' + vect_out + ' ' + vect_out.replace('.shp','_join.shp'), shell=True)
                remove_shapefile(vect_out.replace('.shp','_join.shp'))		
 
#    CHECK FOR MORE THAN ONE LULC MAP AND GENERATE LULC CHANGES MAP      
    if len(generatedgenlulc)>=2:
	    # Loop thru all lulc for current tile and select min and max year as start and end for the change detection
        start_lulc=''
        end_lulc=''		
        for lulcmap in generatedgenlulc:
            if lulcmap.find('_'+str(min(yearofimportedimgs)))>=0:
                start_lulc=lulcmap
            elif lulcmap.find('_'+str(max(yearofimportedimgs)))>=0:
                end_lulc=lulcmap
        if start_lulc!='' and end_lulc!='':
            #define some names for the files
            lulcchanges= data.output+t+'_'+min(yearofimportedimgs)+'_to_'+max(yearofimportedimgs)+'_LUCC'
            lulcchangesreclass= data.output+t+'_'+min(yearofimportedimgs)+'_to_'+max(yearofimportedimgs)+'_LUCCreclass'
            temp='temp'		
            lulcchangesgen= data.output+t+'_'+min(yearofimportedimgs)+'_to_'+max(yearofimportedimgs)+'_LUCCgen'
            lulcchangestif=non_grass_outputpath+'/'+lulcchangesgen+'.tif'	
            #check if file already exists			
            try:
                with open(lulcchangestif) as f: pass
            except:
                grass.message(("Generating change detection map with: " + str(start_lulc) + " and: " + str(end_lulc)))
                #calculate and clean
                p=grass.mapcalc("$out=if($B1==$B2,null(),$B1*2324+$B2*12)", out=lulcchanges, B1=start_lulc, B2=end_lulc)
                applyreclass(reclass_path, lulcchanges, temp)
                p=grass.mapcalc("$out=if($B1<0,null(),$B1)", out=lulcchangesreclass, B1=temp)
				#generalize LUCC
                generalize_lulc(lulcchangesreclass,lulcchangesgen,int(MMU),True)	
                #apply color map			
                applycolormap(color_path, lulcchangesgen)
                #export to tif			
                grass.run_command("r.out.gdal", input=lulcchangesgen, output=lulcchangestif, type='Byte')
                #remove temp files
                grass.run_command("g.remove", flags = "f", quiet=True, rast=lulcchanges)				
                grass.run_command("g.remove", flags = "f", quiet=True, rast=temp)					
    else:
        grass.message(_("No available LULC maps where found to generate LULC changes map in tile " + t))

#CREATE A MOSAIC OF ALL LULC SCEENES
if len(set(generatedlulctifs))>=1:
    for y in yearofimportedimgs:
        list = open(filelist, 'w')
        grass.message(("Creating LULC mosaic for the year " + str(y)))	
        for lulcmaptif in set(generatedlulctifs):
            if lulcmaptif[-17:-13]==y:
                list.write(lulcmaptif)	
                list.write('\n')
        list.close()
        print os.system('gdalbuildvrt -allow_projection_difference -input_file_list '+str(filelist)+' '+non_grass_outputpath+'/LULCmosaic'+str(y)+'.vrt')
        os.remove(filelist)

#calculate and print total processing time
endtime=datetime.datetime.now()		
print 'Total process duration = ' + str(endtime-starttime)
