import os
import sys
import subprocess as sub
import csv
import shutil
import pandas
import gdal
import osr

#LSDTopoTools specific imports
#Loading the LSDTT setup configuration
setup_file = open('./chi_automation.config','r')
LSDMT_PT = setup_file.readline().rstrip()
LSDMT_MF = setup_file.readline().rstrip()
Iguanodon = setup_file.readline().rstrip() 
setup_file.close()

sys.path.append(LSDMT_PT)
sys.path.append(LSDMT_MF)
sys.path.append(Iguanodon)

import Iguanodon31 as Ig

class SRTM:

  def __init__(self, name, tile = 0, lat = 0, lon = 0,alos=False,path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/',SRTM90=False,mergeAllBasins=False,junctions=False):
  
    self.fname = name+'_'+str(tile)
    self.tile = tile
    self.static_path = path
    self.lat = lat
    self.lon = lon
    self.alos = alos
    self.SRTM90 = SRTM90
    self.mergeAllBasins = mergeAllBasins
    self.junctions = junctions
    #creates summary directory
    self.summary_directory = self.static_path+name+'_summary/'
    self.static_path = self.static_path+name+'/' #turn on if not directing to a single directory as part of parallel    
    #rounds lat and long to 2 decimal places to make file naming neater
    lat_2dp = "%.2f" %float(self.lat)
    lon_2dp = "%.2f" %float(self.lon)
    self.path = self.static_path+str(lat_2dp)+'_'+str(lon_2dp)+'_'+self.fname+'/'
    
    #directing to single directory for use of -PARALLEL in visualisation
    #self.path = self.static_path+name
    if not os.path.exists(self.path):
      os.mkdir(self.path, 0777)

 
  def parameterWriter (self, input):
    
    fname_to_write = self.path+self.fname+"_inputcoordinates.param"
    with open(fname_to_write, 'a') as param:
      write_param = param.write(input+'\n')
  
  
  
  def rasterFetcher (self, paddy_lat = 0.2, paddy_long = 0.8):
  
    #if float(self.lat) >= 60.0 or float(self.lat) <= -60.0: #declared float as part of debug
    #if alos:
    #  Ig_alos.get_ALOS30_from_point(self.path, self.fname, lat=float(self.lat), lon=float(self.lon), paddy_lat = float(paddy_lat), paddy_long = float(paddy_long), get_main_basin = False)
    #  extents = 0
    #else: 
    extents = Ig.get_SRTM30_from_point(self.summary_directory, self.fname, lat=float(self.lat), lon=float(self.lon), paddy_lat = float(paddy_lat), paddy_long = float(paddy_long), get_main_basin = False, return_extents=True, alos = self.alos, SRTM90 = self.SRTM90)
    
    print('Building the parameter file')
    self.parameterWriter('This is the write path: '+self.path)
    self.parameterWriter('This is the name: '+self.fname)
    self.parameterWriter('This is the lattitude: '+str(self.lat))
    self.parameterWriter('This is the write longitude: '+str(self.lon))
    self.parameterWriter('This is the paddy_lat: '+str(paddy_lat))
    self.parameterWriter('This is the paddy_lon: '+str(paddy_long))
    self.parameterWriter('ALOS raster used: '+str(self.alos))
    self.parameterWriter('90 metre SRTM used: '+str(self.SRTM90))
    return extents 
                                                                                           
  #def csvEditor(path,name):         #function part of 1 to 1.0 bug fix
  #  file = pandas.read_csv(path+name+'.csv')
  #  file.rename(columns={'m_over_n = 1':'m_over_n = 1.0'}, inplace=True)
  #  os.remove(path+name+'.csv')
  #  file.to_csv(path+name+'.csv', index=False)
  #  del file
  
  def getGeologyRaster(self,extents = [],): #clips and rasterizes GLIM extents for current DEM. Saves to summary_directory
    geology = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/GLIM/himalaya/himalaya.shp' #source of the glim shapefile clipped to cover the himalaya and in geographic coordinate system
    geology_key = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/GLIM/glim_lithokey.csv'
    ds = gdal.Open(self.summary_directory+self.fname+'.bil')
    #getting target srs from current DEM
    ds = ds.GetProjection()
    ds = osr.SpatialReference(ds)
    ds = ds.ExportToProj4()
    #clipping
    os.system(('ogr2ogr -f "ESRI Shapefile" %s.shp %s -clipsrc %s %s %s %s') %(self.summary_directory+self.fname,geology,extents[0],extents[1],extents[2],extents[3])) #This takes a lot of time as it's a big shapefile
    #transform crs and rasterize
    os.system('ogr2ogr -t_srs'+" '"+ds+"' "+self.summary_directory+self.fname+'_utm'+'.shp '+self.summary_directory+self.fname+'.shp')
    os.system('gdal_rasterize -of ENVI -a glim_key_I -a_nodata 0 -tr 30 30 -l '+self.fname+'_utm'+' '+self.summary_directory+self.fname+'_utm'+'.shp '+self.summary_directory+self.fname+'_LITHRAST'+'.bil')
        
  

  def chiAnalysis (self, chi_stats_only=False, print_litho_info=False, burn_raster_to_csv=False, n_movern = 9, start_movern = 0.1, delta_movern = 0.1, min_basin = 10000, interval_basin = 10000, contributing_pixels = 1000, iterations = 1, min_elevation=0, max_elevation=30000, plotting = 0):
    
    #if chi_stats_only:  
      
      #setting write directory
      #current_path = self.path+'/'+str(self.tile)+'/'
      #if not os.path.exists(current_path):
      #  os.makedirs(current_path)
      
      #getting required dems from summary directory 
      #shutil.copy2(self.summary_directory+self.fname+'.bil', current_path)
      #shutil.copy2(self.summary_directory+self.fname+'.hdr', current_path)
      #writing_prefix = self.fname

      #chi = Ig.Iguanodon31(current_path, self.fname, writing_path = current_path, writing_prefix = writing_prefix, data_source = 'ready', preprocessing_raster = False, UTM_zone = '', south = False)
      #Ig.Iguanodon31.chi_stats_only(chi)
      
      #return
    
    for x_i in range (0,int(iterations)):
      print('NOT CHI STATS ONLY')
      current_min = int(min_basin) + (int(interval_basin)*x_i)
      current_max = int(current_min) + (int(interval_basin)/2) #division added to create gap between iterations
      current_path = self.path+'/'+str(current_min)+'/'
      writing_prefix = str(self.tile)+str(current_min)+"_"+str(current_max)
  
      #os.mkdir(current_path,0777) FOR purposes of parallel visualisation the directories can only be made once 
      if not os.path.exists(current_path):
        os.makedirs(current_path)
      
      #putting key into current directory
      if print_litho_info or burn_raster_to_csv:
        geology_key = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/GLIM/glim_lithokey.csv'
        shutil.copy2(geology_key,current_path)
        shutil.copy2(self.summary_directory+self.fname+'_LITHRAST.bil',current_path+'geology_'+self.fname+'.bil')
        shutil.copy2(self.summary_directory+self.fname+'_LITHRAST.hdr',current_path+'geology_'+self.fname+'.hdr')
      
      shutil.copy2(self.summary_directory+self.fname+'.bil', current_path)
      shutil.copy2(self.summary_directory+self.fname+'.hdr', current_path)
      name = self.fname
      #here a command line call needs to be made with the nice &
        
      #chi = Ig.Iguanodon31(current_path, name, writing_path = current_path, writing_prefix = writing_prefix, data_source = 'ready', preprocessing_raster = False, UTM_zone = '', south = False)
      #Ig.Iguanodon31.movern_calculation(chi, n_movern, start_movern, delta_movern, print_basin_raster = True, minimum_basin_size_pixels = current_min, maximum_basin_size_pixels = current_max, threshold_contributing_pixels = contributing_pixels, only_take_largest_basin = False, write_hillshade = True, plot = False)
      
      location = os.getcwd()
      
      chi_plotMoverN_driver = "nohup nice python chi_plotMoverN_driver.py %s %s %s %s %s %s %s %s %s %s %s %s %s&" %(current_path,name,writing_prefix,current_min,current_max,self.summary_directory,print_litho_info,burn_raster_to_csv,self.mergeAllBasins,self.junctions, min_elevation, max_elevation, plotting)
      sub.call(chi_plotMoverN_driver, shell = True)
      
      
      
      
      
      ####begin 1 to 1.0 debug
      #os.rename(str(current_path)+str(current_min)+'_'+str(current_max)+'_movernstats_1_fullstats.csv',str(current_path)+str(current_min)+'_'+str(current_max)+'_movernstats_1.0_fullstats.csv') #debug for movern_fullstats naming as 1 not 1.0   
      #os.rename(str(current_path)+str(current_min)+'_'+str(current_max)+'_MCpoint_1_pointsMC.csv',str(current_path)+str(current_min)+'_'+str(current_max)+'_MCpoint_1.0_pointsMC.csv')
      
      #csv_editor.csvEditor(path = current_path,name = str(current_min)+"_"+str(current_max)+'_residual_movernstats_movern_residuals_Q3')
      #csv_editor.csvEditor(path = current_path,name = str(current_min)+"_"+str(current_max)+'_residual_movernstats_movern_residuals_Q1')
      #csv_editor.csvEditor(path = current_path,name = str(current_min)+"_"+str(current_max)+'_residual_movernstats_movern_residuals_median')
      #csv_editor.csvEditor(path = current_path,name = str(current_min)+"_"+str(current_max)+'_movernstats_basinstats')
      #csv_editor.csvEditor(path = current_path,name = str(current_min)+"_"+str(current_max)+'_MCpoint_points_MC_basinstats')      
      #csv_editor.csvEditor(path = current_path,name = str(current_min)+"_"+str(current_max)+'_movern')            
      
      #plotting_command = "python /exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Git_projects/LSDMappingTools/PlotKnickpointAnalysis.py -dir "+current_path+" -fname "+str(current_min)+"_"+str(current_max)+" -mcstd True -mcbk True"
      #plotting_command = "python %sPlotMOverNAnalysis.py -dir %s -fname %s -ALL True" %(chi.LSDMT_path,chi.wpath,chi.wprefix)
      #sub.call(plotting_command, shell = True) #PlotMOverNAnalysis moved forward to this script to allow debug
      ####end 1 to 1.0 debug
            
      #os.remove(current_path+self.fname+'.bil')
      #os.remove(current_path+self.fname+'.hdr')

      print "printing iteration number "+str(x_i)+".....\n\n"
   
  
      #iteration controller     
      x_i += 1




    


  


    
    
    