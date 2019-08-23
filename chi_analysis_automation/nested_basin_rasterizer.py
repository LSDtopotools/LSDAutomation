##### This script takes all shapefiles in a directory and rasterises with smaller basins given priority #####
##### All shapefiles must contain drainage basins only #####
##### Based on shapefile attributes of OCTOPUS cosmo database downloads #####

# Author: Calum Bradbury 5/11/2018


#plan
#load basins - make sure have area attribute for sorting by largest to smallest
# shapefiles aleady have area attribute - good
# geologic_maps_modify_shapefile facilitates adding geological code for GLIM etc...

import argparse
import subprocess as sub      
import shutil
import os
import geopandas as gpd
import pandas as pd
from time import sleep
import csv
import sys
import  ogr
import gdal
import osr

#LSDTopoTools specific imports
#Loading the LSDTT setup configuration
setup_file = open('chi_automation.config','r')
LSDMT_PT = setup_file.readline().rstrip()
LSDMT_MF = setup_file.readline().rstrip()
Iguanodon = setup_file.readline().rstrip() 
setup_file.close()

sys.path.append(LSDMT_PT)
sys.path.append(LSDMT_MF)
sys.path.append(Iguanodon)

import LSDPlottingTools as LSDPT

target = '/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/s103_basins_webmercator.shp'
target_b = '/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/S111_basins_webmercator.shp'
directory = "/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/Andes_cosmo/"


# function to get list of features to create new shapefile
#21/08 gets all features from all shapefiles in directory
def featuresToList(path):
	fileList = os.listdir(path)
	features = []
	area_list = []
	for file in fileList:
		if file.endswith('.shp'):
				tempSource = ogr.Open(directory+file)
				tempLayer = tempSource.GetLayer(0)
				for feat in tempLayer:
						area_list.append(feat.GetField("AREA"))
						features.append(feat)
	print area_list
	return features,area_list

#21/08 Opens both shapefiles as separate layer objects
def rasterisation(shapefile_name, shapefile_name_b, raster_resolution = 400):

	# The shapefile to be rasterized:
	print('Rasterize ' + shapefile_name)
	#get path and filename seperately
	shapefilefilepath = LSDPT.GetPath(shapefile_name)
	shapefilename = LSDPT.GetFileNameNoPath(shapefile_name)
	shapefileshortname = LSDPT.GetFilePrefix(shapefile_name)

	# now get the the fields from the shapefile
  #opening shapefile_a
	daShapefile = shapefile_name
	dataSource = ogr.Open(daShapefile)
	print(daShapefile)
	daLayer = dataSource.GetLayer(0)

  #opening shapefile_b
	daShapefile_b = shapefile_name_b
	dataSource_b = ogr.Open(daShapefile_b)
	print(daShapefile_b)
	daLayer_b = dataSource_b.GetLayer(0)

	# The raster file to be created and receive the rasterized shapefile
	# Creating output raster
	outrastername = shapefileshortname + '.tif'
	outraster = shapefilefilepath+os.sep+ outrastername
	print("Full name of out raster is: "+outraster)

	# Create the destination data source
  #21/08 This datasource size is based on the two input shapefiles
	inGridSize=float(raster_resolution)
	xMin_a, xMax_a, yMin_a, yMax_a = daLayer.GetExtent()
	xMin_b, xMax_b, yMin_b, yMax_b = daLayer_b.GetExtent()

  ### getting extents to accomodate larger raster than extents of both input shapefiles	
	if xMin_a < xMin_b:
		xMin=xMin_a
	else:
		xMin=xMin_b
		
	if yMin_a < yMin_b:
		yMin=yMin_a
	else:
		yMin=yMin_b
	
	if xMax_a > xMax_b:
		xMax=xMax_a
	else:
		xMax=xMax_b
	
	if yMax_a > yMax_b:
		yMax=yMax_a
	else:
		yMax=yMax_b
	
	print daLayer.GetExtent()
	print daLayer_b.GetExtent()
	
	##new shapefile
	#21/08 This shapefile provides and unrasterised record of the output basins
	driver = ogr.GetDriverByName("ESRI Shapefile")
	data_source = driver.CreateDataSource(directory+"output.shp")
	
	#Getting srs from input shapefile_a
	srs = daLayer.GetSpatialRef()
	layer = data_source.CreateLayer("output", srs, ogr.wkbPolygon)
	
	definitions = []	
	layerDefinition_b = daLayer.GetLayerDefn()
	for i in range(layerDefinition_b.GetFieldCount()):
		definition = layerDefinition_b.GetFieldDefn(i)
		definitions.append(definition)	
	for definition in definitions:
		layer.CreateField(definition)
	
	features,area_list = featuresToList(directory)	
	print "length",len(features)
	for feature in features:
		layer.CreateFeature(feature)
		
	layerDefinition = layer.GetLayerDefn()
	
	### getting extents to accomodate larger raster
	xMin, xMax, yMin, yMax = layer.GetExtent()
  ###extent is correct

	#Calculating x and y resolution
	xRes = int((xMax - xMin) / inGridSize)
	yRes = int((yMax - yMin) / inGridSize)
	
	#21/08 creating raster output
	rasterDS =  gdal.GetDriverByName('GTiff'.encode('utf-8')).Create(directory+"output6.tif", xRes, yRes, 1,  gdal.GDT_Float32)
	# Define spatial reference # OK as all srs have been confirmed equal in projection-debug.py
	NoDataVal = -9999
	rasterDS.SetProjection(daLayer.GetSpatialRef().ExportToWkt())
	rasterDS.SetGeoTransform((xMin, inGridSize, 0, yMax, 0, -inGridSize))
	rBand = rasterDS.GetRasterBand(1)
	rBand.SetNoDataValue(NoDataVal)
	rBand.Fill(NoDataVal)
# Rasterize 
	x_i = 0	
	area_list.sort(reverse=True)
	for area in area_list:		
			if area != -9999.99:
				
				#Execute queries(SQL)
				testSQL = "SELECT * FROM output WHERE AREA='%s'" %(area)
				print "area",area
				temp = data_source.ExecuteSQL(testSQL)
				x_i =x_i+1
				gdal.RasterizeLayer(rasterDS, [1], temp, options = ["ATTRIBUTE=EBE_MMKYR"])
	#closing raster object
	data_source = None
	print("done")

rasterisation(target,target_b)