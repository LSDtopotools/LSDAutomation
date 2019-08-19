#simplified raster burning
#20th July 2019

import os
import csv
import pandas as pd
import gdal
import osr
import subprocess as sub
import sys
import shutil
import utm
from srtm_alos import SRTM #remember to move this script up one directory level.
import glob


#####################
##  User Variables ##

delta_m_n = 0.1
start_m_n = 0.1
directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Andes/'

#geographic zone
andes = True
himalaya = False

#raster selector
geology = True
TRMM = True
exhumation = False
glaciated = False
cosmo = False
distance = False
distance_from = False
distance_along = False
strain = True
tectonics = False

## /User Variables ##
#####################

total_iterations = (1.0-start_m_n)/delta_m_n
#must be integer
total_iterations = float(total_iterations)

iteration_counter = 0

#plan: use processed csv to rasterize a new source raster, and run the raster burner hack of the chi_mapping_tool

### Data Sources ###
data_source_trmm = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/annual.tif'
data_source_exhumation = '/exports/csce/datastore/geos/users/s1134744/exhumation/0_2.tif'
data_source_glaciated = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/glims_ice/ice_100.bil'
data_source_cosmo = '/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/outputDS.tif'
data_source_distance = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/simplified_distance.tif'
data_source_distance_from = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/distance_km.tif'
data_source_distance_along = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/euc_allocation_6.tif'
data_source_strain_himalaya = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/second_invariant.tif'
data_source_strain_andes = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/andes_strain.bil
data_source_tectonics = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/fault_zones/digitized.bil'#source of digitized shapefile
data_source_GLiM_Himalaya = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/GLIM/himalaya/himalaya_full_key.shp'
data_soure_GLiM_Andes = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/GLIM/Andes/andes_glim_full.shp'
data_source_glims_glacier = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/glims_ice/clipped_exists.shp'
### /Data Sources ###

def utmExtents(summary_directory,fname,corner):
  if not os.path.exists(summary_directory+fname+corner+".txt"):
    findUTMextents(summary_directory,fname)
    
  with open (summary_directory+fname+corner+".txt", "r") as text:
    data = text.read().replace(',', '')
    data = data.replace('(','')
    data = data.replace(')','')
    data = data.split()
    coordinates = [data[2],data[3]]
    return coordinates

def findUTMextents(summary_directory,fname):
    #using grep to search for extent values in gdalinfo, I don't know how to directly asign to variable, so this uses an intermediatory text file
    dem = summary_directory+fname+'.bil'
    lower_left = "gdalinfo " + dem + " | grep 'Lower Left' >"+summary_directory+fname+"_lower_left.txt"
    upper_right = "gdalinfo " + dem + " | grep 'Upper Right' >"+summary_directory+fname+"_upper_right.txt"
    os.system(lower_left)
    os.system(upper_right)
    
def utmToLatLon(coordinate,proj4):
  zone = proj4.split(' ')
  zone = zone[1]
  zone = zone.replace('+zone=','')
  easting = float(coordinate[0])
  northing = float(coordinate[1])
  lat_lon_coordinate = utm.to_latlon(int(easting),int(northing),int(zone),northern = True)
  return lat_lon_coordinate
    
def getGlaciers(full_directory,summary_directory,fname,write_name,SRTM90=False):
  
  #these are in UTM, needs to be lat lon
  LL = utmExtents(summary_directory,fname,corner="_lower_left")
  UR = utmExtents(summary_directory,fname,corner="_upper_right")   
 
  ds = gdal.Open(summary_directory+fname+'.bil')
  #getting target srs from current DEM
  ds = ds.GetProjection()
  ds = osr.SpatialReference(ds)
  ds = ds.ExportToProj4()
  
  try:
    LL_lat_lon = utmToLatLon(LL,ds)
    UR_lat_lon = utmToLatLon(UR,ds)
  except:
    sys.exit()        
      
  #clipping                   
  try:
    print('ogr2ogr -f "ESRI Shapefile" %s.shp %s -clipsrc %s %s %s %s' %(summary_directory+fname+'_glaciers',data_source_glims_glacier,LL_lat_lon[0],LL_lat_lon[1],UR_lat_lon[0],UR_lat_lon[1]))                                                     
    sys.exit()
  except:
    sys.exit()
  os.system(('ogr2ogr -f "ESRI Shapefile" %s.shp %s -clipsrc %s %s %s %s') %(summary_directory+fname+'_glaciers',data_source_glims_glacier,LL_lat_lon[0],LL_lat_lon[1],UR_lat_lon[0],UR_lat_lon[1]))
  
  #transform crs and rasterize
  os.system('ogr2ogr -t_srs'+" '"+ds+"' "+summary_directory+fname+'_glaciers_utm'+'.shp '+summary_directory+fname+'_glaciers.shp')
  
  if os.path.isfile(full_directory+fname+'_glaciated.bil'):
    try:
      os.remove(full_directory+fname+'_glaciated.bil')  
      os.remove(full_directory+fname+'_glaciated.hdr')
    except:
      print("Error removing raster files. Forcing exit to prevent unseen errors")
      sys.exit()  
  
  if SRTM90:
    os.system('gdal_rasterize -of ENVI -a exists -a_nodata 0 -tr 90 90 -l '+fname+'_glaciers_utm'+' '+summary_directory+fname+'_glaciers_utm'+'.shp '+full_directory+write_name+'_glaciated'+'.bil')      
  else:
    os.system('gdal_rasterize -of ENVI -a exists -a_nodata 0 -tr 30 30 -l '+fname+'_glaciers_utm'+' '+summary_directory+fname+'_glaciers_utm'+'.shp '+full_directory+write_name+'_glaciated'+'.bil')


def getGeologyRaster(full_directory,summary_directory,fname,lat,lon,SRTM90=False,paddy=0.25,raster_name='Null',glaciation=False): 
    #clips and rasterizes GLIM extents for current DEM. Saves to summary_directory
    ##ADAPTED FROM STRM CLASS##
    #before rasterising, check if raster is already present in directory, remove if it is
    if os.path.isfile(full_directory+fname+raster_name+'.bil'):
      try:
        os.remove(full_directory+fname+'_'+raster_name+'.bil')
        os.remove(full_directory+fname+'_'+raster_name+'.hdr')
      except:
        print("Error removing raster files. Forcing exit to prevent unseen errors")
        sys.exit()
    
    xmin=lon-paddy
    ymin=lat-paddy
    xmax=lon+paddy
    ymax=lat+paddy
    
    geology_key = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/GLIM/glim_lithokey.csv'
    
    print(summary_directory+fname+'.bil')
    ds = gdal.Open(summary_directory+fname+'.bil')
    #getting target srs from current DEM
    ds = ds.GetProjection()
    ds = osr.SpatialReference(ds)
    ds = ds.ExportToProj4()
   
    if not glaciation:
        #shapefile_target = geology
        #for Andes
        if andes:
            shapefile_target = data_soure_GLiM_Andes
            shapefile_attribute = 'glim_litho'
        if himalaya:
            shapefile_target = data_soure_GLiM_Himalaya
            shapefile_attribute = 'litho_keys'
        
    if glaciation:
        shapefile_target = data_source_glims_glacier
        shapefile_attribute = 'exists'
    
    #removing shapefiles  
    try:
        to_remove = glob.glob(summary_directory+fname+raster_name+'*')
    except:
        print("Directory error")
        print("Exiting to prevent abormal activity at - ",summary_directory,fname,raster_name)
        sys.exit()
    
    if not to_remove:
        print("Nothing to remove.")
        
    for path in to_remove:
        try:
            os.remove(path)
        except:
            print("Error removing - ",path)
    
    #This takes a lot of time as it's a big shapefile    
    #clipping
    clip_command = 'ogr2ogr -f "ESRI Shapefile" %s.shp %s -clipsrc %s %s %s %s'%(summary_directory+fname+raster_name,shapefile_target,xmin,ymin,xmax,ymax)  
    print(clip_command)
    os.system(clip_command)        
                            
    #transforming crs  
    transform_command = 'ogr2ogr -t_srs'+" '"+ds+"' "+summary_directory+fname+raster_name+'_utm'+'.shp '+summary_directory+fname+raster_name+'.shp'
    os.system(transform_command)
    
    #rasterising    
    if SRTM90:
        os.system('gdal_rasterize -of ENVI -a '+shapefile_attribute+' -a_nodata -9999 -tr 90 90 -l '+fname+raster_name+'_utm'+' '+summary_directory+fname+raster_name+'_utm'+'.shp '+full_directory+fname+'_'+raster_name+'.bil')      
    else:
        os.system('gdal_rasterize -of ENVI -a '+shapefile_attribute+' -a_nodata -9999 -tr 30 30 -l '+fname+raster_name+'_utm'+' '+summary_directory+fname+raster_name+'_utm'+'.shp '+full_directory+fname+'_'+raster_name+'.bil')

def getRaster(full_directory,summary_directory,write_name,fname,raster_source,raster_name='to_burn',SRTM90=False): 
  LL = utmExtents(summary_directory,fname,corner="_lower_left")
  UR = utmExtents(summary_directory,fname,corner="_upper_right")    
  
  #getting target srs from current DEM  
  try:
    print full_directory+fname+'.bil'
    ds = gdal.Open(full_directory+fname+'.bil')
    ds = ds.GetProjection()
    ds = osr.SpatialReference(ds)
    ds = ds.ExportToProj4()
  except:
    print("error getting burn raster, skipping...")
    return
  
         
  #clipping raster, reprojecting, and setting resolution 
  #setting nodata values to ensure preservation
  #changing from filename to writename
  res_90 = "gdalwarp -ot Float64 -of ENVI -tr 90 90 -srcnodata '-9999' -dstnodata '-9999' -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te %s %s %s %s %s %s%s_%s.bil" %(LL[0],LL[1],UR[0],UR[1],raster_source,full_directory,fname,raster_name)
  res_30 = "gdalwarp -ot Float64 -of ENVI -tr 30 30 -srcnodata '-9999' -dstnodata '-9999' -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te %s %s %s %s %s %s%s_%s.bil" %(LL[0],LL[1],UR[0],UR[1],raster_source,full_directory,fname,raster_name)    
  
  #before rasterising, check if raster is already present in directory, remove if it is
  if os.path.isfile(full_directory+fname+'_'+raster_name+'.bil'):
    try:
      os.remove(full_directory+fname+'_'+raster_name+'.bil')
      os.remove(full_directory+fname+'_'+raster_name+'.hdr')
    except:
      print("Error removing raster files. Forcing exit to prevent unseen errors")
      sys.exit()
      
  print 'srtm 90  is ...s...', SRTM90
  if SRTM90:
    os.system(res_90)
    print res_90
  else:
    os.system(res_30) 
    print res_30       

def mainAnalysis(full_target,summary_directory,write_name,fname,raster_source,header,lat=0.0,lon=0.0,geology_required=False,glaciation=False):
    # function to get rasters once, then iterate through the m/n range adding burned data
    #iteration counter for debugging
        
    if not geology_required:
        getRaster(full_target,summary_directory,write_name,fname,raster_source,raster_name = header)
    
    if geology_required:        
        if glaciation:
            getGeologyRaster(full_target,summary_directory,fname,lat,lon,raster_name = header,glaciation=True)
        
        getGeologyRaster(full_target,summary_directory,fname,lat,lon,raster_name = header)          

    #begining iterations through m/n values, rasters should already have been calculated
    
    for x in range(int(start_m_n*100),100,int(delta_m_n*100)):
        x = float(x)/100
        x = str(x)
        x = x.replace('.','_')
        
        #DEM presence is required
        try:
            os.rename(full_target+fname+'.bil',full_target+fname+x+'.bil')
            os.rename(full_target+fname+'.hdr',full_target+fname+x+'.hdr')
    
        except(OSError):
            print("ERROR! Probably a missing tile. Location: %s%s"%(full_target,fname)) 
        
        #adding burned suffix to ensure raster burner will function as expected
        if not os.path.isfile(full_target+fname+x+'_MChiSegmented_burned.csv'):
            try:
                shutil.copy2(full_target+fname+x+'_MChiSegmented.csv',full_target+fname+x+'_MChiSegmented_burned.csv')
            except:
                print("MChiSegmented file does not exist for iteration %s"%(x))
                #cannot use sys.exit() as not all tiles are successful
                #Try and think of a better method for error control
    
        #removing driver file to aid debugging
        if os.path.isfile(full_target+fname+"_Chiculations.param"):
            os.remove(full_target+fname+"_Chiculations.param")
        
        with open(full_target+fname+"_Chiculations.param",'wb') as file:
            file.write('# This is a parameter file for the chi_mapping_tool \n')
            file.write('# One day there will be documentation. \n')
            file.write(" \n")
            file.write('# These are parameters for the file i/o \n')
            file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
            file.write('read path: %s \n'%(full_target))
            file.write('write path: %s \n'%(full_target))
      
            file.write('read fname: %s \n'%(fname+x))
            file.write('write fname: %s \n'%(fname+x))
      
            file.write("\n")
            file.write('burn_raster_to_csv: True \n')
            file.write('burn_raster_prefix: %s \n'%(fname+'_'+header))
            file.write('burn_data_csv_column_header: %s \n'%(header))
            file.write("\n")
            file.write('secondary_burn_raster_to_csv: False \n')
            file.write('secondary_burn_raster_prefix: Null \n')
            file.write('secondary_burn_data_csv_column_header: Null \n')
            file.close()

        raster_burner_command = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Git_projects/LSDTT_Development/driver_functions_MuddChi2014/raster_burner.exe %s %s" %(full_target,fname+"_Chiculations.param")
        try:
            sub.call(raster_burner_command, shell = True)
        except:
            print("could not burn to csv!!!")
                    
        #undoing rename to allow renaming in next step
        try:
            os.rename(full_target+fname+x+'.bil',full_target+fname+'.bil')
            os.rename(full_target+fname+x+'.hdr',full_target+fname+'.hdr')
        except:
            print("error fixing rename")
    try:
        os.remove(full_target+fname+'_'+header+'.bil')
        os.remove(full_target+fname+'_'+header+'.hdr')
        #print("raster removal turned off")
    except:
        print("failed removing rasters after analyses")






#opening processed source file to access directory structure

if himalaya:
    name_list = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']

if andes:
    name_list = ['Andes_test_processed']

for name in name_list:

    with open(directory+name+'.csv','r') as csvfile:
        csvReader = csv.reader(csvfile,delimiter=',')
        next(csvReader)
        for row in csvReader:
            
            #iteration counting for debug only
            #iteration_counter += 1
            
            #if iteration_counter == 2:
            #    print(iteration_counter)
            #    sys.exit()
            
            #print(row)
            #generating target path
            #for writing output, will make it easier in handling the generated files with existing scripts
            part_1 = str(row[0])
            part_1 = part_1.replace('.','_')
            part_2 = str(("%.2f" %float(row[2])))+'_'+str(("%.2f" %float(row[3])))
            part_2 = part_2.replace('.','_')
            lat=float(row[2])
            lon=float(row[3])
        
            full_target = os.path.join(directory+part_1,part_2+'_'+part_1+'_'+str(row[1]),str(row[5])+'/')            
            #summary directory. This is where the extent.txt files are preserved from the original analysis
            summary_target = directory+part_1+'_summary/'      
            fname = part_1+'_'+str(row[1])
            max_basin = (int(row[6])/2)+int(row[5])      
            write_name = str(row[1])+str(row[5])+'_'+str(max_basin)       

            #logic to rename source DEM files/make sure they exist            
            if not os.path.isfile(full_target+fname+'.bil'):                     
                try:
                    os.rename(full_target+write_name+'.bil',full_target+fname+'.bil')
                    os.rename(full_target+write_name+'.hdr',full_target+fname+'.hdr')
                except:
                    
                    try:
                        shutil.copy2(summary_target+fname+'.bil',full_target+fname+'.bil')
                        shutil.copy2(summary_target+fname+'.hdr',full_target+fname+'.hdr')                        
                    except:
                        print("cannot find the dem for %s"%(fname))
                        #Using sys.exit() at this point might cause unexpected behaviour mid-process. 
                        #Write tiles missing DEMs on the 
            
            if geology:
                mainAnalysis(full_target, summary_target, write_name, fname, data_source_trmm, 'GLiM_Unit', lat = lat, lon = lon, geology_required = True)

        
            if TRMM:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_trmm, lat = lat, lon = lon, header = 'Precipiation_mm_yr')

                             
            if exhumation:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_exhumation, lat = lat, lon = lon, header = 'Exhumation')
                                         
            if glaciated:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_glaciated, lat = lat, lon = lon, header = 'Glaciated',geology_required = False,glaciation=False)
                                         
            if cosmo:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_cosmo, lat = lat, lon = lon, header = 'Cosmo_EBE_mm_kyr')
                                         
            if distance:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_distance, lat = lat, lon = lon, header = 'Distance')
                                         
            if distance_from:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_distance_from, lat = lat, lon = lon, header = 'Distance_From_KM')
                                         
            if distance_along:
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_distance_along, lat = lat, lon = lon, header = 'Distance_Along_KM')
                                         
            if strain: 
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_strain, lat = lat, lon = lon, header = 'Strain_10^-9_year^-1')                             

            if tectonics: 
                mainAnalysis(full_target, summary_target, write_name, fname,
                             raster_source = data_source_tectonics, lat = lat, lon = lon, header = 'Tectonic_Zone')                                                          
