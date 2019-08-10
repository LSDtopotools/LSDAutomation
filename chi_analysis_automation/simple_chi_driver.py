#encaser for chi_mapping_tool and PlotMoverN.py when using nohup nice &
#simplified from chi_plotMoverN_driver.py 19th July 2019
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

import LSDPlottingTools as LSDPT
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
parser.add_argument("min_elevation",nargs='?',default="none")
parser.add_argument("max_elevation",nargs='?',default="none")
parser.add_argument("start_m_n",nargs='?',default="none")
parser.add_argument("delta_m_n",nargs='?',default="none")
parser.add_argument("total_iterations",nargs='?',default="none")

inputs = parser.parse_args()

current_path = inputs.current_path
fname = inputs.fname
writing_prefix = inputs.writing_prefix
current_min = inputs.current_min
current_max = inputs.current_max
summary_directory = inputs.summary_directory
min_elevation = inputs.min_elevation
max_elevation = inputs.max_elevation
start_m_n = inputs.start_m_n
delta_m_n = inputs.delta_m_n
total_iterations = inputs.total_iterations

#ensuring correct variable type
start_m_n = float(start_m_n)
delta_m_n = float(delta_m_n)
total_iterations = float(total_iterations)

def parameterWriter(parameter):
  fname_to_write = current_path+fname+"_input_chi_plotMoverN_driver.param"
  with open(fname_to_write, 'a') as param:
    write_param = param.write(parameter+'\n')

if not summary_directory:
  summary_directory = current_path
  print summary_directory

parameterWriter("current_path: "+str(current_path))
parameterWriter("fname: "+str(fname))
parameterWriter("writing_prefix: "+str(writing_prefix))
parameterWriter("current_min: "+str(current_min))
parameterWriter("current_max: "+str(current_max))
parameterWriter("summary_directory: "+str(summary_directory))
parameterWriter("min_elevation: "+str(min_elevation))
parameterWriter("max_elevation: "+str(max_elevation))

chi = Ig.Iguanodon31(current_path, fname, writing_path = current_path, writing_prefix = writing_prefix, 
                     data_source = 'ready', preprocessing_raster = False, UTM_zone = '', south = False)
                     
#initial m_n doesn't really matter. Removing variable.
Ig.Iguanodon31.movern_calculation(chi,print_litho_info=False, litho_raster='Null', print_junctions_to_csv=True,
                                  n_movern=total_iterations, start_movern=start_m_n, delta_movern=delta_m_n,
                                  print_simple_chi_map_with_basins_to_csv =False,
                                  print_segmented_M_chi_map_to_csv =True, print_chi_data_maps = False, 
                                  print_basin_raster = True, minimum_basin_size_pixels = current_min, 
                                  maximum_basin_size_pixels = current_max, threshold_contributing_pixels = 1000,
                                  only_take_largest_basin = False, write_hillshade = True, plot = False, 
                                  minimum_elevation = min_elevation, maximum_elevation = max_elevation)
                                                                
def renameOutputs(in_name,out_name):
  try:
    shutil.move(current_path+writing_prefix+in_name+'.csv',current_path+writing_prefix+out_name+'.csv')  
  except:
    print 'Error in '+in_name+' to '+out_name+' conversion!'
    
                              
#moving data to summary directory
#shutil.copy2(current_path+writing_prefix+'_hs.bil', summary_directory+writing_prefix+'_hs.bil')
#shutil.copy2(current_path+writing_prefix+'_hs.hdr', summary_directory+writing_prefix+'_hs.hdr')

# Logic to iterate through possible m/n ratios. #
# Purpose is to produce KSN values recalculated for each m/n value. #
# Based on concavity corrector. #

#range has to be integer#
for x in range(int(start_m_n*100),100,int(delta_m_n*100)):
  #recasting to float
  m_over_n = float(x)/100
  
  if m_over_n >= 1:
    print('error in m_over_n number')
  
  print m_over_n
  mn_for_name = str(m_over_n)
  mn_for_name = mn_for_name.replace('.','_')
  chi = Ig.Iguanodon31(current_path, fname, writing_path = current_path,
                       writing_prefix = fname+str(mn_for_name), data_source = 'ready', 
                       preprocessing_raster = False, UTM_zone = '', south = False)
                     
  Ig.Iguanodon31.mchi_only(chi,minimum_basin_size_pixels = current_min, maximum_basin_size_pixels = current_max, 
                           m_over_n = m_over_n, threshold_contributing_pixels = 1000,
                           minimum_elevation = min_elevation, maximum_elevation= max_elevation)
  