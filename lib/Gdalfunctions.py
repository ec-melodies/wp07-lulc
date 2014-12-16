import shutil
import os
import ogr
import glob
import sys
import numpy as np
from itertools import izip, cycle, tee
from osgeo import gdal
from os.path import basename

#GENERAL VARIABLES
NDVI='0.5*255*(((A - B) / (A + B))+1)'

def mask_generation(localoutputdir,inputimage,cloudvalues,ouputimage,invert):
	print os.system('gdal_calc -A ' + inputimage + ' --outfile=' + ouputimage + ' --calc="A<0" --type=Int16 --overwrite')
	for v in cloudvalues:
		print os.system('gdal_calc -A ' + inputimage + ' --outfile=' + localoutputdir + '/temp.tif --calc="'+v+'" --type=Int16 --overwrite')
		print os.system('gdal_calc -A ' + ouputimage + ' -B ' + localoutputdir + '/temp.tif --outfile=' + ouputimage + '._temp.tif --calc="A+B" --type=Int16 --overwrite')
		try:
			shutil.copy(ouputimage + '._temp.tif', ouputimage)
			os.remove(localoutputdir + '/temp.tif')
			os.remove(ouputimage + '._temp.tif')
		except:
			for i in cloudvalues:
				print i
			shutil.copy(ouputimage + '._temp.tif', ouputimage)
			os.remove(localoutputdir + '/temp.tif')
			os.remove(ouputimage + '._temp.tif')
	if invert==1:
		print os.system('gdal_calc -A ' + ouputimage + ' --outfile=' + ouputimage + '._temp.tif --calc="A==0" --type=Int16 --overwrite')
		shutil.copy(ouputimage + '._temp.tif', ouputimage)
		os.remove(ouputimage + '._temp.tif')
	
def DimensionsCheck(dimensioncheckimage,dimensioncheckreferenceimage):
	myRasterXSize = str(gdal.Open(dimensioncheckimage, gdal.GA_ReadOnly).RasterXSize)
	myRasterYSize = str(gdal.Open(dimensioncheckimage, gdal.GA_ReadOnly).RasterYSize)
	myReferenceRasterXSize = str(gdal.Open(dimensioncheckreferenceimage, gdal.GA_ReadOnly).RasterXSize)
	myReferenceRasterYSize = str(gdal.Open(dimensioncheckreferenceimage, gdal.GA_ReadOnly).RasterYSize)
	if myRasterXSize <> myReferenceRasterXSize or myRasterYSize <> myReferenceRasterYSize:
		print os.system('gdalwarp -ts ' + str(gdal.Open(dimensioncheckreferenceimage, gdal.GA_ReadOnly).RasterXSize) + ' ' + str(gdal.Open(dimensioncheckreferenceimage, gdal.GA_ReadOnly).RasterYSize) + ' -r near ' + dimensioncheckimage + ' ' + dimensioncheckimage.replace('.tif', '._temp.tif'))
		shutil.copy(dimensioncheckimage.replace('.tif', '._temp.tif'), dimensioncheckimage)
		os.remove(dimensioncheckimage.replace('.tif', '._temp.tif'))
	else:
		return 1

def calculateareas(vector_file):
	ds = ogr.Open( vector_file, update = 1 )
	if ds is None:
		print vector_file + " open failed./n"
		sys.exit( 1 )
	layername = vector_file[vector_file.rfind('/')+1:][:vector_file[vector_file.rfind('/')+1:].rfind('.')]
	lyr = ds.GetLayerByName( layername )
	lyr.ResetReading()
	field_defn = ogr.FieldDefn( "Area_ha", ogr.OFTReal )
	lyr.CreateField(field_defn)
	for i in lyr:
		geom = i.GetGeometryRef()
		area = geom.GetArea()
		lyr.SetFeature(i)
		i.SetField( "Area_ha", area/10000 )
		lyr.SetFeature(i)
	ds = None

def populatedatefield(vectorfile, datevalue):
	ds = ogr.Open( vectorfile, update = 1 )
	if ds is None:
		print vectorfile + " open failed./n"
		sys.exit( 1 )
	layername = vectorfile[vectorfile.rfind('/')+1:][:vectorfile[vectorfile.rfind('/')+1:].rfind('.')]
	lyr = ds.GetLayerByName( layername )
	lyr.ResetReading()
	field_defn = ogr.FieldDefn( "JulnDate", ogr.OFTString )
	lyr.CreateField(field_defn)
	for i in lyr:
		lyr.SetFeature(i)
		i.SetField( "JulnDate", datevalue )
		lyr.SetFeature(i)
	ds = None

def rastertotable_by_vectorgrid (raster,vectorgrid,output):
	ds = ogr.Open( vectorgrid, update = 1 )
	if ds is None:
		print vectorgrid + " open failed./n"
		sys.exit( 1 )
	layername = vectorgrid[vectorgrid.rfind('/')+1:][:vectorgrid[vectorgrid.rfind('/')+1:].rfind('.')]
	print layername
	lyr = ds.GetLayerByName( layername )
	lyr.ResetReading()
	id=1
		
	for i in lyr:
		clip = i.GetGeometryRef()
		outShapefile = 'tmp_mel'+str(id)
		outDriver = ogr.GetDriverByName("ESRI Shapefile")
		# Remove output shapefile if it already exists
		if os.path.exists(outShapefile):
			outDriver.DeleteDataSource(outShapefile)
		# Create the output shapefile
		outDataSource = outDriver.CreateDataSource(outShapefile)
		outLayer = outDataSource.CreateLayer("tmp_mel"+str(id), geom_type=ogr.wkbPolygon)
		# Create the feature and set values
		feature = ogr.Feature(outLayer.GetLayerDefn())
		feature.SetGeometry(clip)
		outLayer.CreateFeature(feature)
		# Close DataSource
		outDataSource.Destroy()	
		# Clip raster
		clippedimage = raster.replace('.tif','_clip'+str(id)+'.tif')
		print os.system('gdalwarp -q -cutline ' + outShapefile + ' -crop_to_cutline -of GTiff ' + raster + ' ' + clippedimage +' -overwrite')
		# Read and summarize raster
		rastertotable (clippedimage,output)
		id=id+1
		# Delete temporary files
		outDriver.DeleteDataSource(outShapefile)
		os.remove(clippedimage)
	ds = None
	# return id
	
def calculateidandareas(vector_file):
	ds = ogr.Open( vector_file, update = 1 )
	if ds is None:
		print vector_file + " open failed./n"
		sys.exit( 1 )
	layername = vector_file[vector_file.rfind('/')+1:][:vector_file[vector_file.rfind('/')+1:].rfind('.')]
	lyr = ds.GetLayerByName( layername )
	lyr.ResetReading()
	layer_defn = lyr.GetLayerDefn()
	field_defn1 = ogr.FieldDefn( "ID", ogr.OFTInteger)
	field_defn2 = ogr.FieldDefn( "Area_ha", ogr.OFTReal )
	field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
	count=0
	for f in field_names:
		if f=="ID":
			lyr.DeleteField(count)
			count=count-1
		elif f=="Area_ha":
			lyr.DeleteField(count)
			count=count-1
		count=count+1
	lyr.CreateField(field_defn1)
	lyr.CreateField(field_defn2)
	id=1
	for i in lyr:
		geom = i.GetGeometryRef()
		area = geom.GetArea()
		lyr.SetFeature(i)
		i.SetField( "Area_ha", area/10000 )
		i.SetField( "ID", id )
		lyr.SetFeature(i)
		id=id+1
	ds = None	
	
def calculatendvi (image,sensor):
	image_ndvi = image.replace('.tif', '_ndvi.tif')
	print os.system('gdal_calc -A ' + image + ' --A_band 4 -B '+ image + ' --B_band 3 --outfile='+ image_ndvi + ' --calc="' + NDVI + '" --type=Float32 --overwrite --CalcAsDT')
	return image_ndvi

def getrasterbbox (raster):	
	#Dataset
	ds = gdal.Open(raster)
	#Retrieve xmin,ymin,xmax,ymax
	cols = ds.RasterXSize
	rows = ds.RasterYSize
	geotransform = ds.GetGeoTransform()
	bb1 = originX = geotransform[0]
	bb4 = originY = geotransform[3]
	pixelWidth = geotransform[1]
	pixelHeight = geotransform[5]
	Width = cols*pixelWidth
	Height = rows*pixelHeight
	bb3 = originX+Width
	bb2 = originY+Height
	return bb1,bb2,bb3,bb4

	

def rastertotable (raster,output):
		ds = gdal.Open(raster)
		cols = ds.RasterXSize
		rows = ds.RasterYSize
		#cols = 10
		#rows = 10
		bands = ds.RasterCount
		val = ds.ReadAsArray(0,0,cols,rows)
		list = []
		for sd in xrange(cols):
				for i in xrange(rows):
						for v in val:
								pixelval = v[sd][i]
								list.append(pixelval)				
		listb = []
		for d in xrange(len(list)):    
				if d % bands == 0:
						listc=[]
						pixelvalue = str(list[0+d])+','+str(list[1+d])+','+str(list[2+d])
						listc.append(pixelvalue)
				listb.append(listc)    
		listd = []     
		for g in listb:
				c = listb.count(g)
				v = str(g) + ' - ' + str(c)
				listd.append(v)
		print np.unique(listd)
		log = open(output, 'a')
		log.write(np.unique(listd))

	

def rastertotable2 (raster,output,tilingfactor):
	ds = gdal.Open(raster)
	cols = ds.RasterXSize
	rows = ds.RasterYSize
	bands = ds.RasterCount
	#rows=1300
	#cols=1100
	bSize=10
	list = []
	for i in range(0,rows,bSize):
		if i + bSize < rows: 
			numRows = bSize
		else:
			numRows = rows - i
		for j in range(0,cols,bSize):
			if j + bSize < cols:
				numCols=bSize 
			else:
				numCols=cols-j

			val=ds.ReadAsArray(j,i,numCols,numRows)
			
			list = []
			for sd in xrange(numCols):
				for i in xrange(numRows):
					for v in val:
						pixelval = v[sd][i]
						list.append(pixelval)				
			listb = []
			for d in xrange(len(list)):    
					if d % bands == 0:
							listc=[]
							pixelvalue = str(list[0+d])+','+str(list[1+d])+','+str(list[2+d])
							listc.append(pixelvalue)
					listb.append(listc)    
			listd = []     
			for g in listb:
				c = listb.count(g)
				v = str(g) + ' - ' + str(c)
				listd.append(v)
			print np.unique(listd)
			log = open(output, 'a')
			log.write(np.unique(listd))

			
def clipraster (image,cliparea,outputformat,output):			#Clipping images
	tmpimage = image+'_tmp.'+outputformat
	if outputformat=="tif":
		outputformat = 'GTiff'
	#get raster's boundingbox	
	minx,miny,maxx,maxy= getrasterbbox (image)
	#clip image with the cliparea
	print os.system('gdalwarp -q -cutline ' + cliparea + ' -crop_to_cutline -of '+outputformat+ ' ' + image + ' ' + tmpimage+' -overwrite')
	#clip previous result with bounding box from original image
	print os.system('gdalwarp -te '+str(minx)+' '+str(miny)+' '+str(maxx)+' '+str(maxy)+' '+tmpimage+' '+output+' -overwrite')
	#remove temporary image
	os.remove(tmpimage)
	return output

def calculatendviandintegrate (image,sensor,outputformat):
	image_ndvi = image.replace('.tif', '_ndvi.'+outputformat)	
	image_ndvi_byte = image.replace('.tif', '_ndvi_byte.'+outputformat)
	image_out = image.replace('.tif', '_wndvi.'+outputformat)
	if outputformat=="tif":
		outputformat = 'GTiff'
	if sensor=="LC8":	
		print os.system('gdal_calc -A ' + image + ' --A_band 4 -B '+ image + ' --B_band 3 --outfile='+ image_ndvi + ' --calc="' + NDVI + '" --type=Float32 --overwrite --CalcAsDT')
	else:
		print os.system('gdal_calc -A ' + image + ' --A_band 5 -B '+ image + ' --B_band 4 --outfile='+ image_ndvi + ' --calc="' + NDVI + '" --type=Float32 --overwrite --CalcAsDT')
	print os.system('gdal_translate -ot byte -of '+outputformat + ' ' + image_ndvi + ' ' + image_ndvi_byte)
	os.remove(image_ndvi)
	print os.system('gdal_merge.bat -separate -of '+outputformat+' -o ' + image_out + ' ' + image + ' ' + image_ndvi_byte)
	return image_out

def stackimages (imagebandsfolder,sensor,outputformat):	
    image = os.path.basename(imagebandsfolder)
    image_b1 = imagebandsfolder+'/'+image+'_B1.TIF'
    image_b2 = imagebandsfolder+'/'+image+'_B2.TIF'
    image_b3 = imagebandsfolder+'/'+image+'_B3.TIF'
    image_b4 = imagebandsfolder+'/'+image+'_B4.TIF'
    image_b5 = imagebandsfolder+'/'+image+'_B5.TIF'
    image_b6 = imagebandsfolder+'/'+image+'_B6.TIF'
    image_b7 = imagebandsfolder+'/'+image+'_B7.TIF'
    image_stack = imagebandsfolder+'/'+image+'_stack453.'+outputformat		
    if outputformat=="tif":
        outputformat = 'GTiff'
    if sensor=="LC8":
        image_b9 = imagebandsfolder+'/'+image+'_B9.TIF'
# print os.system('gdal_merge.bat -separate -of '+outputformat+' -o ' + image_stack + ' ' + image_b1 + ' ' + image_b2 + ' ' + image_b3 + ' ' + image_b4 + ' ' + image_b5 + ' ' + image_b6 + ' ' + image_b7 + ' ' + image_b9)	
        print os.system('gdal_merge.bat -separate -of '+outputformat+' -o ' + image_stack + ' ' + image_b4 + ' ' + image_b5 + ' ' + image_b3)	
    else:
        print os.system('gdal_merge.bat -separate -of '+outputformat+' -o ' + image_stack + ' ' + image_b1 + ' ' + image_b2 + ' ' + image_b3 + ' ' + image_b4 + ' ' + image_b5 + ' ' + image_b6 + ' ' + image_b7)	
	return image_stack

def mask (image,bandnumber,criteria,output):		#Generate image mask
	print os.system('gdal_calc -A ' + image + ' --A_band '+bandnumber+' --outfile=' + output + ' --calc="'+criteria+'" --overwrite')
	return output
	
def remove_shapefile(shapefilename):
    for fl in glob.glob(shapefilename.replace('.shp','.*')):
        os.remove(fl)		
	
def join_segments_and_csv(segments_shp,classification_csv):
    segments_shp_basename=os.path.splitext(basename(segments_shp))[0]
    classification_csv_basename=os.path.splitext(basename(classification_csv))[0]
    try:
        with open(segments_shp.replace('.shp','.idm')) as f: pass
        with open(segments_shp.replace('.shp','.ind')) as f: pass
    except: 
        SQLindex_shp='"CREATE INDEX ON '+segments_shp_basename+' USING ID"'
        print os.system('ogr2ogr -sql '+ SQLindex_shp +' '+ segments_shp.replace('.shp','_i.shp') + ' ' + segments_shp)
    # SQLindex_csv='"CREATE INDEX ON '+classification_csv_basename+' USING ID"'
    # print os.system('ogr2ogr -sql '+ SQLindex_csv +' '+ classification_csv.replace('.csv','_i.csv') + ' ' + classification_csv)
    OGRSQL='"SELECT tbla.*, tblb.mode_Band1  FROM ' + segments_shp_basename + ' tbla LEFT JOIN \'' + classification_csv + '\'.'+classification_csv_basename+' tblb on tbla.ID = tblb.ID"'
    print OGRSQL	
    print os.system('ogr2ogr -sql '+OGRSQL+' '+ segments_shp.replace('.shp','_join.shp') + ' ' + segments_shp)