#encaser for chi_mapping_tool and PlotMoverN.py when using nohup nice &
import argparse
import subprocess as sub      
import shutil
import os
import geopandas as gpd
import pandas as pd
from time import sleep
import csv
import sys

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

from LSDPlottingTools import LSDMap_MOverNPlotting as MN
from LSDMapFigure import PlottingHelpers as Helper
import Iguanodon31 as Ig

#parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("current_path",nargs='?',default="none")
parser.add_argument("fname",nargs='?',default="none")
parser.add_argument("writing_prefix",nargs='?',default="none")
parser.add_argument("current_min",nargs='?',default="none")
parser.add_argument("current_max",nargs='?',default="none")
parser.add_argument("summary_directory",nargs='?',default="none")
parser.add_argument("print_litho_info",nargs='?',default="none")
parser.add_argument("burn_raster_to_csv",nargs='?',default="none")
parser.add_argument("geology",nargs='?',default="none")
parser.add_argument("TRMM",nargs='?',default="none")
parser.add_argument("mergeAllBasins",nargs='?',default="none")
parser.add_argument("junctions",nargs='?',default="none")
parser.add_argument("min_elevation",nargs='?',default="none")
parser.add_argument("max_elevation",nargs='?',default="none")
parser.add_argument("plotting",nargs='?',default="none")

inputs = parser.parse_args()

current_path = inputs.current_path
fname = inputs.fname
writing_prefix = inputs.writing_prefix
current_min = inputs.current_min
current_max = inputs.current_max
summary_directory = inputs.summary_directory
print_litho_info = inputs.print_litho_info
burn_raster_to_csv = inputs.burn_raster_to_csv   
geology = inputs.geology
TRMM = inputs.TRMM
mergeAllBasins = inputs.mergeAllBasins 
print_junctions_to_csv = inputs.junctions
min_elevation = inputs.min_elevation
max_elevation = inputs.max_elevation


#debugging passing of bool
inputs.plotting = int(inputs.plotting)
#plotting = False 

if inputs.plotting == 0:
  plotting = False
if inputs.plotting == 1:
  plotting = True

  


def parameterWriter(parameter):
  fname_to_write = current_path+fname+"_input_chi_plotMoverN_driver.param"
  with open(fname_to_write, 'a') as param:
    write_param = param.write(parameter+'\n')

#writing inputs to parameter file
parameterWriter("current_path: "+current_path)
parameterWriter("fname: "+fname)
parameterWriter("writing_prefix: "+writing_prefix)
parameterWriter("current_min: "+current_min)
parameterWriter("current_max: "+current_max)
parameterWriter("summary_directory: "+summary_directory)
parameterWriter("print_litho_info: "+print_litho_info)
parameterWriter("burn_raster_to_csv: "+burn_raster_to_csv)
parameterWriter("mergeAllBasins: "+mergeAllBasins)
parameterWriter("junctions: "+print_junctions_to_csv)
parameterWriter("min_elevation: "+min_elevation)
parameterWriter("max_elevation: "+max_elevation)
parameterWriter("plotting: "+str(plotting))
parameterWriter("geology: "+str(geology))
parameterWriter("TRMM: "+str(TRMM))




if not summary_directory:
  summary_directory = current_path
  print summary_directory

if print_litho_info: #chi_lith analysis doesn't appear to work. Just burn raster info.
  litho_raster = 'geology_'+fname
else:
  litho_raster = 'NULL'

if burn_raster_to_csv:
  burn_raster_prefix = 'geology_'+fname
else:
  burn_raster_prefix = 'NULL'

#chi_analysis
chi = Ig.Iguanodon31(current_path, fname, writing_path = current_path, writing_prefix = writing_prefix, data_source = 'ready', preprocessing_raster = False, UTM_zone = '', south = False)
Ig.Iguanodon31.movern_calculation(chi, burn_raster_to_csv, burn_raster_prefix, print_litho_info, litho_raster, print_junctions_to_csv, n_movern=9, start_movern=0.1, delta_movern=0.1, print_simple_chi_map_with_basins_to_csv =False, print_segmented_M_chi_map_to_csv =True, print_chi_data_maps = False, print_basin_raster = True, minimum_basin_size_pixels = current_min, maximum_basin_size_pixels = current_max, threshold_contributing_pixels = 1000, only_take_largest_basin = False, write_hillshade = True, plot = False, minimum_elevation = min_elevation, maximum_elevation = max_elevation)

print "????",current_path,writing_prefix

if plotting:
  #chi_plotting
  plotting_command = "python %sPlotMOverNAnalysis.py -dir %s -fname %s -ALL True" %(chi.LSDMT_path,current_path,writing_prefix)
  sub.call(plotting_command, shell = True)   

  ##### Imports and merges M/N data to shapefiles for use in QGIS

  #source data
  #path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/27.19_91.13_pankhabar-north_lakhiumpur_8/30000/'
  #fname = '830000_40000'
  #read into dataframes

  df = gpd.read_file(current_path+writing_prefix+'_AllBasins.shp')
  df2 = pd.read_csv(current_path+writing_prefix+'_AllBasinsInfo.csv')
  
  #renaming column to allow merging with shapefile
  df2.rename(columns={'outlet_junction':'ID'}, inplace=True)

  #merging data by outlet_junction
  new_df = df.merge(df2, on='ID')

  #getting MonteCarlo M/N data for this directory
  BasinDF = Helper.ReadMCPointsCSV(current_path,writing_prefix)
  PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=0.1,d_movern=0.1,n_movern=9)

  #merging MonteCarlo M/N data by basin_key
  new_df = new_df.merge(PointsDF, on='basin_key')

  #exporting to shapefile
  new_df.to_file(summary_directory+writing_prefix)
  

#moving data to summary directory
shutil.copy2(current_path+writing_prefix+'_hs.bil', summary_directory+writing_prefix+'_hs.bil')
print "did this start????"
shutil.copy2(current_path+writing_prefix+'_hs.hdr', summary_directory+writing_prefix+'_hs.hdr')

#shutil.move(current_path+writing_prefix+'.csv',summary_directory)

#shutil.copy2(current_path+writing_prefix+'_AllBasins.cpg', summary_directory+writing_prefix+'_AllBasins.cpg')
#shutil.copy2(current_path+writing_prefix+'_AllBasins.dbf', summary_directory+writing_prefix+'_AllBasins.dbf')
#shutil.copy2(current_path+writing_prefix+'_AllBasins.prj', summary_directory+writing_prefix+'_AllBasins.prj')
#shutil.copy2(current_path+writing_prefix+'_AllBasins.shp', summary_directory+writing_prefix+'_AllBasins.shp')
#shutil.copy2(current_path+writing_prefix+'_AllBasins.shx', summary_directory+writing_prefix+'_AllBasins.shx')

if plotting:
  shutil.copy2(current_path+'chi_plots/MLE_profiles.mp4', summary_directory+writing_prefix+'MLE_profiles.mp4')

  shutil.copy2(current_path+'summary_plots/'+writing_prefix+'_movern_chi_points.png', summary_directory+writing_prefix+'_movern_chi_points.png')
  shutil.copy2(current_path+'raster_plots/'+writing_prefix+'_basins_movern_chi_full.png', summary_directory+writing_prefix+'_basins_movern_chi_full.png')
  shutil.copy2(current_path+'raster_plots/'+writing_prefix+'_basins_movern_chi_points.png', summary_directory+writing_prefix+'_basins_movern_chi_points.png')
  shutil.copy2(current_path+'raster_plots/'+writing_prefix+'_basins_movern_SA.png', summary_directory+writing_prefix+'_basins_movern_SA.png')

#moving MChiSegmented to summary directory. Appending summary AllBasinsInfo.csv
if mergeAllBasins:
  shutil.copy2(current_path+writing_prefix+'_MChiSegmented.csv', summary_directory+writing_prefix+'_MChiSegmented.csv')
  with open(current_path+writing_prefix+'_AllBasinsInfo.csv', 'r') as csvfile:
    csvReader = csv.reader(csvfile, delimiter =',')
    next(csvReader)
    for row in csvReader:
      a = row[0]
      b = row[1]
      c = row[2]
      d = row[3]
      e = row[4]
      f = row[5]
      #removing the "_currentmax" part from string, part of debugging sorting basins for consistency.
      to_replace = "_"+str(current_max) 
      g = writing_prefix.replace(to_replace,"")
  
      #error management, hopefully will reduce/eliminate IOErrors
      try:
        with open(summary_directory+'summary_AllBasinsInfo.csv', 'a') as csvfile_B:
          csvWriter = csv.writer(csvfile_B, delimiter = ',')
          csvWriter.writerow((a,b,c,d,e,f,g))
      except IOError:
        sleep(5)
        with open(summary_directory+'summary_AllBasinsInfo.csv', 'a') as csvfile_B:
          csvWriter = csv.writer(csvfile_B, delimiter = ',')
          csvWriter.writerow((a,b,c,d,e,f,g))        

#removing duplicate dem files - DO NOT REMOVE, needed for PlotChiAnalysis.py
#os.remove(current_path+writing_prefix+'_AllBasins.bil')
#os.remove(current_path+writing_prefix+'_AllBasins.hdr')


#=============================================================================
# This sections generates some basins lithology statistics using the burn_to_csv function. 
# Must have burn_to_csv flag as true!
#=============================================================================

if burn_raster_to_csv:
    #adding burned csv data to mchi_segmented. CAUTION!!!  rounding lat long to 4 d.p.
  if geology or TRMM:
    
    with open(current_path+writing_prefix+'_chi_data_map_burned.csv','r') as chi:
      pandasChi = pd.read_csv(chi, delimiter = ',')
      burned_data = pandasChi[["burned_data","latitude","longitude"]]
      burned_data[["latitude","longitude"]] = burned_data[["latitude","longitude"]].round(4)
      #print burned_data  
      with open(current_path+writing_prefix+'_MChiSegmented.csv','r') as mchi:
        pandasMChi = pd.read_csv(mchi, delimiter = ',')
        pandasMChi[["latitude","longitude"]] = pandasMChi[["latitude","longitude"]].round(4)
        burned_data = burned_data.merge(pandasMChi,on=["latitude","longitude"])
        #print pandasMChi
        #print burned_data
        burned_data.to_csv(current_path+writing_prefix+'_MChiSegmented_burn.csv', mode = "w", header = True, index = False)  
    
    shutil.copy(current_path+writing_prefix+'_MChiSegmented_burn.csv', summary_directory+writing_prefix+'_MChiSegmented_burn.csv')
  
  
  
  if geology:
    #generating write file
    with open(current_path+writing_prefix+'_basin_lithology.csv', 'wb') as csvfile:
      csvWriter = csv.writer(csvfile,delimiter=',')
      csvWriter.writerow(("basin","Evaporites","Ice and Glaciers","Metamorphics","No Data","Acid plutonic rocks","Basic plutonic rocks","Intermediate plutonic rocks","Pyroclastics","Carbonate sedimentary rocks",
      "Mixed sedimentary rocks","Siliciclastic sedimentary rocks","Unconsolidated sediments","Acid volcanic rocks","Basic volcanic rocks","Intermediate volcanic rocks","Water Bodies","Precambrian rocks","Complex lithology"))  
  
    def lithCounter(basin_number,pandas_list):
      list = [basin_number]
      with open(current_path+"glim_lithokey.csv",'r') as csvfile:
        csvReader = csv.reader(csvfile,delimiter=',')
        next(csvReader)
        for row in csvReader:
          key = int(row[1])
          list.append(pandas_list.count(key)) 
      return list
    
    burned_DF = open(current_path+writing_prefix+'_chi_data_map_burned.csv','r')
    #reading chi data map with basins and burned glim lithology data to pandas dataframe
    pandasDF = pd.read_csv(burned_DF, delimiter = ',')

    with open(current_path+writing_prefix+'_AllBasinsInfo.csv','r') as csvfile:
      csvReader = csv.reader(csvfile,delimiter=',')
      next(csvReader)
      for row in csvReader:
        basin_number = int(row[5])
        selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_number]
        pandas_list = selected_DF['burned_data'].tolist()
        #print pandas_list
        count = lithCounter(basin_number,pandas_list)
        print "printing basin number", basin_number
        print count
        with open(current_path+writing_prefix+'_basin_lithology.csv', 'a') as csvfile:
          csvWriter = csv.writer(csvfile,delimiter=',')
          csvWriter.writerow(count)
    burned_DF.close()

#=============================================================================
# This section caculates lithology as a percentage. 
# Also adds the outlet elevation.
# Must have burn_to_csv flag as true!
#=============================================================================



    def mChiSegmented_elevation(node):
      with open(current_path+writing_prefix+"_MChiSegmented.csv",'r') as mChiSegmented:
        pandasDF = pd.read_csv(mChiSegmented, delimiter = ',')
        selected_DF = pandasDF.loc[pandasDF['node'] == node]
        return int(selected_DF['elevation'])

    #function to return node from junction
    def junction_node(junction):
      with open(current_path+writing_prefix+"_JN.csv",'r') as junction_node:
        pandasDF = pd.read_csv(junction_node, delimiter = ',')
        selected_DF = pandasDF.loc[pandasDF['junction'] == junction]
        return int(selected_DF['node'])

    #function to return outlet junction from basin_key
    def outlet_junction(basin_key):
      with open(current_path+writing_prefix+"_AllBasinsInfo.csv",'r') as outlet_junction:
        pandasDF = pd.read_csv(outlet_junction, delimiter = ',')
        selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
        return int(selected_DF['outlet_junction'])

    def statsWriter(current_path,writing_prefix):
      #generating output file
      with open(current_path+writing_prefix+"_litho_elevation.csv","wb") as stats_csv:
        csvWriter = csv.writer(stats_csv,delimiter=',')
        csvWriter.writerow(("Evaporites","Ice and Glaciers","Metamorphics","No Data","Acid plutonic rocks","Basic plutonic rocks","Intermediate plutonic rocks","Pyroclastics","Carbonate sedimentary rocks",
        "Mixed sedimentary rocks","Siliciclastic sedimentary rocks","Unconsolidated sediments","Acid volcanic rocks","Basic volcanic rocks","Intermediate volcanic rocks","Water Bodies","Precambrian rocks",
        "Complex lithology","outlet_elevation","basin_key"))

      #try and add MN data to litho_elevation.csv
      with open(current_path+writing_prefix+"_basin_lithology.csv",'r') as csvfile:
        csvReader = csv.reader(csvfile,delimiter=',')
        next(csvReader)
        for row in csvReader:
          #getting outlet elevation:
          basin_key = int(row[0])
          junction = outlet_junction(basin_key)
          node = junction_node(junction)
          elevation = mChiSegmented_elevation(node)
          #beginning work on the lithologies  
          list = []
          #recasting to an integar list
          for x in row:
            list.append(int(x))  
          #accounting for basin_number in list
          list = list[1:]
          total = sum(list)
          percentage = []
          for x in list:
            x = float(x)
            x = (x/total)*100
            x = "%.2f" %float(x)
            percentage.append(x)
          percentage.append(elevation)
          percentage.append(basin_key)
          print "did this run OK?"
          with open(current_path+writing_prefix+"_litho_elevation.csv","a") as stats_csv:
            csvWriter = csv.writer(stats_csv,delimiter=',')
            csvWriter.writerow((percentage))
            
    print "why is this evaluating as true?"
    statsWriter(current_path,writing_prefix)
  
   
  
    #adding MN data to litho_elevation.csv
  if geology:
    with open(current_path+writing_prefix+'_litho_elevation.csv','r') as file:
      BasinDF = Helper.ReadMCPointsCSV(current_path,writing_prefix)
      PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=0.1,d_movern=0.1,n_movern=9)
      pandasDF = pd.read_csv(file, delimiter = ',')
      pandasDF = pandasDF.merge(PointsDF, on='basin_key')
      pandasDF.to_csv(current_path+writing_prefix+'_litho_elevation_MN.csv', mode="w",header=True,index=False)
  
  
    try:
      shutil.copy(current_path+writing_prefix+"_litho_elevation_MN.csv", summary_directory+writing_prefix+"_litho_elevation.csv")
    except:
      print "failed moving litho_elevation to summary directory"



#removing files duplicated from summary directory
if burn_raster_to_csv:
  os.remove(current_path+'geology_'+fname+'.bil')
  os.remove(current_path+'geology_'+fname+'.hdr')
  
  
print "did this end????"

 
