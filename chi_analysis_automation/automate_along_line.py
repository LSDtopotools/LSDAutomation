#=============================================================================
# Script to automate chi analysis along lines between coordinates defined using a csv file.
# Requires input with the csv name, csv must be in the path define below, ie, where the data will be processed and stored.
# 
# Authors:
#     Calum Bradbury
#=============================================================================
#=============================================================================
# IMPORT MODULES
#=============================================================================

import csv
from srtm_alos import SRTM
import os
import argparse

#=============================================================================
# Welcome screen if no arguments.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("This script will automate chi analysis using tiles.")
    print("For help type:")
    print("   python automate_along_line.py -h\n")
    print("=======================================================================\n\n ")

#=============================================================================
# Function to define tile locations along line between input coordinates.
#=============================================================================  
def getLine(lat_1,lon_1,lat_2,lon_2,path,write,paddy=0.5,iterations=1,min_basin=10000,basin_interval=20000,name='test'):
  
  #line gradient
  total_vertical = lat_2-lat_1
  total_horizontal = lon_2-lon_1            
  gradient = total_vertical/total_horizontal
  intercept = lat_1-(gradient*lon_1)
  tile_number = 1

  #creating lon_intermediate variable for passing longitude
  lon_intermediate = lon_1  
  
  #csv writer
  while lon_intermediate <= (lon_2+paddy):
    

    lat_intermediate = (gradient*lon_intermediate)+intercept

    #writing to csv
    with open(path+write+'.csv', 'a') as csvfile:
      basinwriter = csv.writer(csvfile)
      basinwriter.writerow((name,str(tile_number),lat_intermediate,lon_intermediate,iterations,min_basin,basin_interval))

    tile_number += 1
    #controls longitudinal overlap of tiles. There is not latitudinal overlap at present.
    lon_intermediate += (paddy*1.5)




#=============================================================================
# Reading key arguments.
#=============================================================================
parser = argparse.ArgumentParser()
parser.add_argument("csv_name",nargs="?",default="none",help="Name of input csv containing coordinates and target basin size")
#CAUTION: as I don't understand parsing boolean values very well, the following will evaluate to true for any input deflag -alos
parser.add_argument("-alos", "--alos",nargs="?",type=bool,default=False,help="If true ALOS30 DEM data will be used, default is SRTM30")
parser.add_argument("-SRTM90", "--SRTM90",nargs="?",type=bool,default=False,help="If true SRTM90 DEM data will be used, default is SRTM30")
parser.add_argument("-mergeAllBasins", "--mergeAllBasins",nargs="?",type=bool,default=False,help="")
parser.add_argument("-junctions", "--junctions",nargs="?",type=bool,default=False,help="If true the junction csv file will be output from the chi analysis tool")
parser.add_argument("-plotting", "--plotting",nargs="?",type=bool,default=False,help="If true the plotting tools will also be run for each tile")
parser.add_argument("-min_elevation", "--min_elevation",nargs="?",type=int,help="Minimum elevation for analysis")
parser.add_argument("-max_elevation", "--max_elevation",nargs="?",type=int,help="Maximum elevation for analysis")

#These arguments require streamlining
parser.add_argument("-burn_raster_to_csv", "--burn_raster_to_csv",nargs="?",type=bool,default=False,help="")
parser.add_argument("-geology", "--geology", nargs="?", type = bool, default=False, help="")
parser.add_argument("-TRMM", "--TRMM", nargs="?", type = bool, default=False, help="")
parser.add_argument("-use_precipitation_raster_for_chi", "--use_precipitation_raster_for_chi",nargs="?",type=bool,default=False,help="If true ")

inputs = parser.parse_args()
csv_name = inputs.csv_name
alos = inputs.alos
SRTM90 = inputs.SRTM90
mergeAllBasins = inputs.mergeAllBasins
junctions = inputs.junctions

#=============================================================================
# Key variables not yet controlled by arguments or input csv.
#=============================================================================

#Decimal degrees, controls size of tiles.
paddy_long = 0.25

#write path. Input csv must be in this directory.
path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/0_05_concavity/' 

#write name.
write = str(csv_name)+'_processed'

#=============================================================================
# Logic to control passing of boolean variables to subsequent scripts, clumsy.
#=============================================================================

if not inputs.burn_raster_to_csv:
  burn_raster_to_csv = 0
if inputs.burn_raster_to_csv:
  burn_raster_to_csv = 1

if not inputs.geology:
  geology = 0
if inputs.geology:
  geology = 1

if not inputs.TRMM:
  TRMM = 0
if inputs.TRMM:
  TRMM = 1

if not inputs.plotting:
  plotting = 0
if inputs.plotting:
  plotting = 1
  
if not inputs.use_precipitation_raster_for_chi:
  use_precipitation_raster_for_chi = 0
if inputs.use_precipitation_raster_for_chi:
  use_precipitation_raster_for_chi = 1

#setting min and max elevations for chi analysis
if inputs.min_elevation: 
  min_elevation = inputs.min_elevation
else:
  min_elevation = 0
  
if inputs.max_elevation:  
  max_elevation = inputs.max_elevation
else:
  max_elevation = 30000
 
 
#=============================================================================
# The following sections control tiling and preparation of csv files which drive the analysis.
# Manages directory structure in part. Key to analaysis.
#=============================================================================

with open(path+write+'.csv', 'wb') as csvfile:
   basinwriter = csv.writer(csvfile)
   basinwriter.writerow(('name','tile','lat', 'lon', 'iterations','min basin','basin_interval'))

with open(path+str(csv_name)+'.csv','r') as csvfile:
  csvReaderA = csv.reader(csvfile, delimiter = ',')
  next(csvReaderA)
  for row in csvReaderA:
    name = row[0]     
    name = name.replace('.','_')
    lat_1 = row[1]
    lon_1 = row[2]
    lat_2 = row[3]
    lon_2 = row[4]     
    lat_1 = float(lat_1)
    lat_2 = float(lat_2)
    lon_1 = float(lon_1)
    lon_2 = float(lon_2)
    iterations = row[5]
    min_basin = row[6]
    basin_interval = row[7]
    getLine(lat_1=lat_1, lon_1=lon_1, lat_2=lat_2, lon_2=lon_2, paddy=paddy_long, path=path, write=write, iterations=iterations, min_basin=min_basin, basin_interval=basin_interval, name=name)
  
    #generate summary directory
    summary_directory = path+name+'_summary/'
    os.mkdir(summary_directory, 0777)
    
    #generate main directory to allow use of -PARALLEL in visualisation. Doesn't work.
    main_directory = path+name
    os.mkdir(main_directory, 0777)
    
    #generating summary AllBasinsInfo.csv to control merging of MChiSegmented
    if mergeAllBasins:
      with open(summary_directory+'summary_AllBasinsInfo.csv', 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter = ',')
        csvWriter.writerow(('latitude','longitude','outlet_longitude','outlet_longitude','outlet_junction','basin_key','source_name','source_prefix'))

#=============================================================================
# Main driver of chi analysis. Beyond this, processes are sent to the background.
#=============================================================================  

with open(path+write+'.csv','r') as csvfile:
  csvReader = csv.reader(csvfile, delimiter = ',')
    
  next(csvReader)
  
  for row in csvReader:
     name = row[0]     
     name = name.replace('.','_')
     tile = row[1]
     lat = row[2]
     lon = row[3]
     iterations = row[4]
     min_basin = row[5]
     basin_interval = row[6]
              
     instanceSRTM = SRTM(name = name, tile = tile, lat = lat, lon = lon, alos=alos, SRTM90=SRTM90, mergeAllBasins=mergeAllBasins, junctions=junctions, path=path)
     
     extents = instanceSRTM.rasterFetcher(paddy_lat = 0.25, paddy_long = paddy_long) #returns extents in format xmin,ymin,xmax,ymax
     
     print 'SRTM90 is:...', SRTM90
     #if not SRTM90:
     if geology == 1:
        instanceSRTM.getGeologyRaster(SRTM90=SRTM90,extents=extents)
     if TRMM == 1:
        instanceSRTM.getTRMM(SRTM90=SRTM90,extents=extents)
     instanceSRTM.chiAnalysis(instanceSRTM, iterations = iterations,  min_basin = min_basin, interval_basin = basin_interval, print_litho_info=0, burn_raster_to_csv = burn_raster_to_csv,min_elevation=min_elevation, max_elevation=max_elevation, plotting = plotting, geology=geology, TRMM=TRMM, use_precipitation_raster_for_chi=use_precipitation_raster_for_chi)