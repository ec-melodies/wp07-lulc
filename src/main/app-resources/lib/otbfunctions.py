import os, sys
import datetime
import time
import glob
import zipfile
#import otbApplication
from osgeo import gdal

def trainandclassify (image,image_mask,samples,image_stats,image_svm,output):	
	#Generate image stats
	print os.system('otbcli_ComputeImagesStatistics -il ' + image + ' -out ' + image_stats)	
	#Train
	print os.system('otbcli_TrainImagesClassifier -io.il '+image+' -io.vd '+samples+' -io.imstat '+image_stats+' -sample.mv 100 -sample.mt 100 -sample.vtr 0.5 -sample.edg false -sample.vfn Class -classifier libsvm -classifier.libsvm.k linear -classifier.libsvm.c 1 -classifier.libsvm.opt false -io.out '+image_svm+' -io.confmatout svmConfusionMatrixQB1.csv')
	#Classify
	print os.system('otbcli_ImageClassifier -imstat ' + image_stats + ' -mask ' + image_mask + ' -model ' + image_svm + ' -in ' + image + ' -out ' + output)
	return output
	
def classification (image,image_mask,samples,image_stats,image_svm,output):	
	#Generate image stats
	print os.system('otbcli_ComputeImagesStatistics -il ' + image + ' -out ' + image_stats)	
	#Classify
	print os.system('otbcli_ImageClassifier -imstat ' + image_stats + ' -mask ' + image_mask + ' -model ' + image_svm + ' -in ' + image + ' -out ' + output)
	return output	

def otbsegmentation (image,mask,spatialr,maxiter,ranger,threshold,minsize,tilesize,simplify,vect_out):
	# SEGMENTATION	
	print "Performing image segmentation"
	# app = otbApplication.Registry.CreateApplication("Segmentation") 
	# app.SetParameterString("in", image)
	# app.SetParameterString("filter.meanshift.spatialr", spatialr)
	# app.SetParameterString("filter.meanshift.maxiter", maxiter)
	# app.SetParameterString("filter.meanshift.ranger", ranger)
	# # app.SetParameterFloat("filter.meanshift.thres",threshold)
	# app.SetParameterString("filter.meanshift.minsize", minsize)
	# app.SetParameterString("mode.vector.inmask", mask)
	# app.SetParameterString("mode.vector.stitch", 'True')
	# app.SetParameterString("mode.vector.out", vect_out) 
	# app.SetParameterString("mode.vector.simplify", simplify)
	# app.SetParameterString("mode.vector.outmode", 'ovw')
	# app.SetParameterString("mode.vector.tilesize", tilesize)
	# app.SetParameterString("mode.vector.neighbor", 'True')
	# app.ExecuteAndWriteOutput()
	print os.system("otbcli_Segmentation -in " + image + " -mode vector -mode.vector.out " + vect_out + " -mode.vector.inmask " + mask + " -mode.vector.simplify " + simplify + " -filter meanshift -filter.meanshift.spatialr " + spatialr + " -filter.meanshift.maxiter " + maxiter + " -filter.meanshift.ranger " + ranger + " -filter.meanshift.minsize " + minsize)

def integratesegmentationandraster (classf_image,output_stats,vector_file):
	# INTEGRATE CLASSIFICATION DATA
	print "Analysing classified pixels within segments"
	print os.system('starspan2 --vector '+vector_file +' --raster ' + classf_image + ' --out-prefix ' +  output_stats + ' --out-type table --summary-suffix _summary.csv --stats mode --fields ID --noColRow --noXY --RID none --nodata 0')
