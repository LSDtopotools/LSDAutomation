#Iguanodon is an automation class for LSDTopoTools because I am Lazy.

import utm
import pandas as pd
import numpy as np
import os
import subprocess as sub

class Iguanodon31:

	def __init__(self,reading_path, reading_prefix, writing_path = "", writing_prefix = "", data_source = 'ready', preprocessing_raster = False, UTM_zone = '', south = False):
		
		# Setting the reading parameters
		self.rpath = reading_path
		if(self.rpath[-1] != '/'):
			self.rpath += '/'
		self.rprefix = reading_prefix
		# setting the writting parameters
		if(writing_prefix != ''):
			self.wpath = writing_path
			if(self.wpath[-1] != '/'):
				self.wpath += '/'
		else:
			self.wpath = self.rpath
		if(writing_prefix != ''):
			self.wprefix = writing_prefix
		else:
			self.wprefix = self.rprefix

		# dealing with data source

		if(data_source == 'ready'): # If data is ready to use - do nothing
			print("loading your data without any preLSD processing")
		elif(data_source == 'OT_SRTM30'):
			print('I am importing the data from raw opentopo file')
			extract_file(self.rpath,"rasters_srtm.tar.gz")
			OT_SRTM30_toLSDTT(self.rpath,"output_srtm.tif", UTM_zone, self.wpath+self.wprefix+".bil", reso =30, south = south)

		# Loading the LSDTT setup configuration
		setup_file = open('config.config','r')
		self.LSD_folder = setup_file.readline()
		setup_file.close()

		###### TODO CONVERSION #######

		# Before doing anything else, let's preprocess the file if needed note that I will erase your original file
		if(preprocessing_raster):
			self.preprocess_raster(self, replace = True)

	def preprocess_raster(self, replace = False):
		"""
			This function preprocess the raster, it sorts some nodata issues and recast the data into float
			if replace is activated, it replace the original file.

		"""
		print('I am preprocessing your raster')
		if(replace):
			print("Warning; I will replace your original file!")
		print('Building the parameter file:')
		fname_to_write = self.wpath+self.wprefix+"_PreProcessing.param"
		print(self.rpath+self.rprefix+"_PreProcessing.param")
		# Writing the file
		file = open(fname_to_write, 'w')
		file.write('# This is a parameter file for the chi_mapping_tool \n')
		file.write('# One day there will be documentation. \n')
		file.write(' \n')
		file.write('# These are parameters for the file i/o \n')
		file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
		file.write('read path: %s \n'%(self.rpath))
		file.write('write path: %s \n'%(self.wpath))
		file.write('read fname: %s \n'%(self.rprefix))
		file.write('write fname: %s \n'%(self.wprefix))
		file.close()
		# done with writing

		# let's run the analysis

		lsdtt_pp = sub.Popen(self.LSD_folder+'Analysis_driver/DEM_preprocessing.exe '+self.wpath + ' ' +self.wprefix + '_PreProcessing.param',shell = True)
		lsdtt_pp.wait()
		print("Done with the preprocessing")



###### end of the class

def extract_file(fpath,fname,file_type = 'targz'):
	
	if(file_type == 'targz'):
		extract_command = "tar xzvf %s"%(fpath+fname)
	if(file_type == 'zip'):
		extract_command = "unzip %s"%(fpath+fname)

	extract_popen = sub.Popen(extract_command, shell = True)
	extract_popen.wait()

def OT_SRTM30_toLSDTT(fpath,fname, UTM_zone, out_full_name, reso = 30, south = False):

	if(south):
		conversion_command = "gdalwarp -t_srs '+proj=utm +zone=%s +south +datum=WGS84' -of ENVI -r cubic -tr %s %s %s %s" %(UTM_zone,reso,reso,fpath+fname, fpath+out_full_name)

	else:
		conversion_command = "gdalwarp -t_srs '+proj=utm +zone=%s +datum=WGS84' -of ENVI -r cubic -tr %s %s %s %s" %(UTM_zone,reso,reso,fpath+fname, fpath+out_full_name)

	conversion_process = sub.call(conversion_command,shell = True)

def get_SRTM30_from_point(fpath, fname, lat = 0, lon = 0, paddy_lat = 1, paddy_long = 2, get_main_basin = False, remove_old_files = True):

	# Calculation of the extents
	xmin = lon - paddy_long
	xmax = lon + paddy_long
	ymin = lat - paddy_lat
	ymax = lat + paddy_lat

	if(xmin>=xmax or ymin>= ymax):
		print("UNVALID PARAMETERS: the extend of the wanted raster are not valid. Check it.")
	wget_command = 'wget -O %s "http://opentopo.sdsc.edu/otr/getdem?demtype=SRTMGL1&west=%s&south=%s&east=%s&north=%s&outputFormat=GTiff"'%(fpath+fname,xmin,ymin,xmax,ymax)
	wget_process =  sub.call(wget_command, shell = True)
	# Dealing with the conversion
	temp_info = utm.from_latlon(lat,lon)
	if(temp_info[3] in ['X','W','V','U','T','S','R','Q','P','N']):
		south = False
	else:
		south = True


	OT_SRTM30_toLSDTT(fpath, fname,temp_info[2],fname+".bil",reso = 30, south = south)
	if remove_old_files:
			os.remove(fpath+fname) # Removing the Tiff file
	if(get_main_basin):
		print('I got your raster, now I am trimming it with LSDTT')
		print('Building the requested files:')
		# writing the outlet file
		csv = open(fpath+"outlet.csv", 'w')
		csv.write("IDs,latitude,longitude\n")
		csv.write("string,%s,%s\n"%(lat,lon))
		csv.close()

		# Writing the file
		file = open(fpath+fname+"_trimming.param", 'w')
		file.write('# This is a parameter file for the chi_mapping_tool \n')
		file.write('# One day there will be documentation. \n')
		file.write(" \n")
		file.write('# These are parameters for the file i/o \n')
		file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
		file.write('read path: %s \n'%(fpath))
		file.write('write path: %s \n'%(fpath))
		file.write('read fname: %s \n'%(fname))
		file.write('write fname: %s \n'%(fname))
		file.write(" \n")
		file.write('get_basins_from_outlets: true \n')
		file.write('spawn_basins_from_outlets: true \n')
		file.write('basin_outlet_csv: outlet.csv \n')
		file.write(" \n")
		file.close()
		# done with writing

		# let's run the analysis
		## need to read first the LSD folder
		setup_file = open('config.config','r')
		LSD_folder = setup_file.readline()
		setup_file.close()


		lsdtt_pp = sub.call(LSD_folder+'Analysis_driver/basin_averager.out '+fpath + ' ' +fname + '_trimming.param',shell = True)
		print("Done with basin spawning")

		if(remove_old_files):
			os.remove(fpath+fname+'.bil') # Removing the bil file
			os.remove(fpath+fname+'.hdr') # Removing the header file
			os.rename(fpath+fname+"_Spawned_0.bil",fpath+fname+".bil") # Renaming the older file
			os.rename(fpath+fname+"_Spawned_0.hdr",fpath+fname+".hdr") # Renaming the older file

	if(return_iguanodon):
		IG = Iguanodon31(fpath, fprefix, writing_path = fpath, writing_prefix = fprefix, data_source = 'ready', preprocessing_raster = False, UTM_zone = temp_info[2], south = south)
		return IG

