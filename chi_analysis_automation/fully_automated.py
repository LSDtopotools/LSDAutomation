##19th July 2019##
##Amalgamation of automate along line, iguanodon, and concavity corrector

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
import sys

#=============================================================================
# Welcome screen if no arguments.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("This script will automate chi analysis using tiles.")
    print("For help type:")
    print("   python fully_automated.py -h\n")
    print("=======================================================================\n\n ")

#====================
##  User Variables ##
#====================

delta_m_n = 0.1
start_m_n = 0.1
#write path. Input csv must be in this directory.
path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/0_1_5000m/'

#====================
## /User Variables ##
#====================
total_iterations = (1.0-start_m_n)/delta_m_n

total_iterations = float(total_iterations)

print delta_m_n,start_m_n,total_iterations




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
parser.add_argument("-min_elevation", "--min_elevation",nargs="?",type=int,help="Minimum elevation for analysis")
parser.add_argument("-max_elevation", "--max_elevation",nargs="?",type=int,help="Maximum elevation for analysis")

inputs = parser.parse_args()
csv_name = inputs.csv_name
alos = inputs.alos
SRTM90 = inputs.SRTM90

#=============================================================================
# Key variables not yet controlled by arguments or input csv.
#=============================================================================

#Decimal degrees, controls size of tiles.
paddy_long = 0.25



#write name.
write = str(csv_name)+'_processed'

#=============================================================================
# Setting min and max elevations for chi analysis.
#=============================================================================

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
        
#=============================================================================
# Main driver of chi analysis. Beyond this, processes are sent to the background.
#=============================================================================  

with open(path+write+'.csv','r') as csvfile:
  csvReader = csv.reader(csvfile, delimiter = ',')
    
  next(csvReader)
  
  # For each row in csv the tiling process is started. # 
  for row in csvReader:
     name = row[0]     
     name = name.replace('.','_')
     tile = row[1]
     lat = row[2]
     lon = row[3]
     iterations = row[4]
     minimum_basin = row[5]
     basin_interval = row[6]
              
     instanceSRTM = SRTM(name = name, tile = tile, lat = lat, lon = lon, alos=alos, SRTM90=SRTM90, path=path)
     #extents unused
     extents = instanceSRTM.rasterFetcher(paddy_lat = 0.25, paddy_long = paddy_long) #returns extents in format xmin,ymin,xmax,ymax
     instanceSRTM.simpleChiAnalysis(minimum_basin, basin_interval, min_elevation, max_elevation, start_m_n, delta_m_n, total_iterations)