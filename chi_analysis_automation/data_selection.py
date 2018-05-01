# script to select basins from MChiSegmented.csv
# uses an AllBasins.csv file with source_name added to source data
# all csv files must be in the same directory
import csv
import os
import argparse
import pandas as pd



# defined by argparse from terminal line

parser = argparse.ArgumentParser()
parser.add_argument("-dir", "--base_directory", type=str, help="The base directory with the m/n analysis. If this isn't defined I'll assume it's the same as the current directory.")
parser.add_argument("name",nargs='?')
parser.add_argument("-no_summary", "--no_summary", type=bool, default = False, help="use if all AllBasin and MChiSegmented csvs are in same directory and no summary_AllBasins.csv is present.")
inputs = parser.parse_args()

if inputs.name:
  name = inputs.name
else:
  name = ""

path = inputs.base_directory

#checking directory
if not path:
  path = os.getcwd()
  


#basin tracker
x_i = 0

#define function to select MChiSegmented data. Takes a pandas dataframe

#generating MChiSegmented csvfile to append data ### doesn't appear to actually be necessary
with open(path+name+'_output_MChiSegmented.csv', 'wb') as csvfile_A:
  csvReader_A = csv.writer(csvfile_A, delimiter = ',')
  #put relvant MChiSegmented column names here
  csvReader_A.writerow(("node",	"row", "col", "latitude", "longitude", "chi", "elevation", "flow_distance", "drainage_area", "m_chi", "b_chi", "source_key","basin_key", "segmented_elevation"))
  
#generating AllBasins csvfile to write corrected basin_key
with open(path+str(name)+'_output_AllBasinsInfo.csv', 'wb') as csvfile_B:
  csvReader_B = csv.writer(csvfile_B, delimiter = ',')
  #put relvant MChiSegmented column names here
  csvReader_B.writerow(('latitude','longitude','outlet_longitude','outlet_longitude','outlet_junction','basin_key'))

#allows merging of csv files output by multiple runs of this script when a summary csv file is not present.
#this creates a summary file following the same format.
if inputs.no_summary:
  with open(path+str(name)+'summary_AllBasins.csv','wb') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter = ',')
    csvWriter.writerow(('latitude','longitude','outlet_longitude','outlet_longitude','outlet_junction','basin_key','source_name'))
  for file in os.listdir(path):
    if file.endswith("AllBasinsInfo.csv"):
      print file
      with open(path+file, 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter = ',')
        
        next(csvReader)
        #stripping file string
        file = file.replace('_AllBasinsInfo.csv','')
        print file
        
        for row in csvReader:
          row.append(file)
          with open(path+str(name)+'summary_AllBasins.csv','a') as csvfile:
            csvWriter = csv.writer(csvfile,delimiter = ',')
            csvWriter.writerow((row))
        
    
    
  
      


#sorting summary_AllBasinsInfo csv by source name to maintain consistency in basin_key assigniment
with open(path+str(name)+'summary_AllBasins.csv','r') as csvfile:
  pandasDF = pd.read_csv(csvfile,delimiter=',')
  outputDF = pandasDF.sort_values(by=["source_name","basin_key"])
  outputDF.to_csv(path+name+"summary_sorted_AllBasinsInfo.csv", mode="w",header=True,index=False)

#generating an output litho_elevation.csv file
with open(path+str(name)+'_output_litho_elevation.csv','wb') as csvfile:
  csvWriter = csv.writer(csvfile,delimiter=',')
  csvWriter.writerow(("Evaporites","Ice and Glaciers","Metamorphics","No Data","Acid plutonic rocks","Basic plutonic rocks","Intermediate plutonic rocks","Pyroclastics","Carbonate sedimentary rocks",
  "Mixed sedimentary rocks","Siliciclastic sedimentary rocks","Unconsolidated sediments","Acid volcanic rocks","Basic volcanic rocks","Intermediate volcanic rocks","Water Bodies","Precambrian rocks",
  "Complex lithology","outlet_elevation","basin_key", "Median_MOv",	"FirstQ_thr",	"Min_MOverN",	"Max_MOverN"))

  

#opening AllBasins.csv to generate matching MChiSegmented 
with open(path+str(name)+'summary_sorted_AllBasinsInfo.csv', 'r') as csvfile_C:
  csvReader_C = csv.reader(csvfile_C, delimiter = ',')
  next(csvReader_C)
  for row in csvReader_C:                                           
  # use row[6] to open MChiSegmented  
    latitude = row[0]
    longitude = row[1]
    outlet_latitude = row[2]
    outlet_longitude = row[3]
    outlet_junction = row[4]
    basin_key = row[5]
    basin_key = int(basin_key)
    source_name = row[6]
    
    #read into pandas dataframe to allow easy selection using column value
    with open(path+source_name+'_MChiSegmented.csv', 'r') as csvfile_D:
      pandasDF = pd.read_csv(csvfile_D, delimiter = ',')
      selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
      #reassigning basin_key
      selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
      #append to MChiSegemnted.csv
      #print selected_DF
      selected_DF.to_csv(path+name+'_output_MChiSegmented.csv',mode='a',header=False,index=False)     
    
    #write corrected output_AllBasins.csv
    with open(path+name+'_output_AllBasinsInfo.csv', 'a') as csvfile_E:
      csvReader_D = csv.writer(csvfile_E, delimiter = ',')
      csvReader_D.writerow((latitude,longitude,outlet_latitude,outlet_longitude,outlet_junction,x_i))
      
    #writing litho_elevation.csv
    
    with open(path+source_name+'_litho_elevation.csv','r') as csvfile:
      pandasDF = pd.read_csv(csvfile,delimiter=',')
      selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
      #reassigning basin_key
      selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
      selected_DF.to_csv(path+name+'_output_litho_elevation.csv',mode='a',header=False,index=False)     
      
      #csvReader = csv.reader(csvfile,delimiter = ',')
      #next(csvReader)
      #for row in csvReader:
        #removing old basin_key
      #  data = row[:-1]
      #  data.append(x_i)
        #writing output data
      #  with open(path+str(name)+'_output_litho_elevation.csv','a') as csvfile:
      #    csvWriter = csv.writer(csvfile,delimiter = ',')
      #    csvWriter.writerow(data)
          
      
          
    #maintains correct basin labelling  
    print x_i
    x_i += 1
    
       
      