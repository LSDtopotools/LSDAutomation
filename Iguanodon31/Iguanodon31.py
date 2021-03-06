# Iguanodon is an automation class for LSDTopoTools because I am Lazy.
# SMM: I am attempting to go through this and document it as best I can. 
# The purpose of this package is to manage the downloading and processing 
# of topographic data. 
# 
# There are a series of routines for fetching data from opentopography
# and then additional functions that run LSDTopoTools analyses. 
# These are done using subprocess calls.
#
# Documentation started 26/06/2018 somewhere in the air near Paris. 

import utm
import os
import subprocess as sub

class Iguanodon31:

	def __init__(self,reading_path, reading_prefix, writing_path = "", writing_prefix = "", data_source = 'ready', preprocessing_raster = False, UTM_zone = '', south = False):
		"""
    The Iguanodon31 object automates running analyses and plotting results.
    The data members are mostly paths to where data is located and where plotting scripts are located.
    
    reading_path (str): The directory of the data
    reading_prefix (str): The prefix of the data (e.g., SuperPlace.bil will have a prefix of SuperPlace)
    writing_path (str): Directory to which the code writes. If an empty string it will write to the reading_path.
    writing_prefix (str): Prefix of writing rasters. If empty string defaults to reading_prefix.
    data_source (str): If this is OT_SRTM30, the program will run assuming the data is the SRTM30 data
    from OpenTopography.org. Otherwise it will assume data is ready for processing.
    In the future more options will be added here. 
    preprocessing_raster (bool): If true, run some preprocessing routines to convert to correct coordinate system, format, clean up nodata, etc. Needed if you are directly grabbing SRTM tiles.
    UTM_zone (int): Sets the UTM zone
    south (bool): If true, sets the UTM zone to south. Otherwise the UTM zone will be north.
    
    Author: BG
    
    """
		
		# Setting the reading parameters
		self.rpath = reading_path
		if(self.rpath[-1] != '/'):
			self.rpath += '/'
		self.rprefix = reading_prefix
		# setting the writting parameters
		if(writing_prefix != '' and 1==0):
			self.wpath = writing_path
			if(self.wpath[-1] != '/'):
				self.wpath += '/'
		
		else:
			print("I am sorry, for buggy reasons at the moments, I am forcing your writing path to be the same as your reading path. Apologies.")
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
		else:
			print("You didn't tell me the data source so I will assume you have prepared rasters.")

		# Loading the LSDTT setup configuration
		setup_file = open('config.config','r')
		self.LSDTT_path = setup_file.readline().rstrip()
		self.LSDMT_path = setup_file.readline().rstrip()
		setup_file.close()

		###### TODO CONVERSION #######

		# Before doing anything else, let's preprocess the file if needed note that I will erase your original file
		if(preprocessing_raster):
			self.preprocess_raster(self, replace = True)

	def preprocess_raster(self, replace = False):
		"""
    This function preprocess the raster, it sorts some nodata issues and recast the data into float
      if replace is activated, it replace the original file.
       
        Args:
          replace (bool): If true, this replaces the current raster with a raster with "remove seas".
          WARNING: You lose the original DEM so do this with caution!
          
    Author: BG
    
    
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
		file.write('# Documentation at: http://lsdtopotools.github.io/Documentation/ \n')
		file.write(' \n')
		file.write('# These are parameters for the file i/o \n')
		file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
		file.write('read path: %s \n'%(self.rpath))
		file.write('write path: %s \n'%(self.wpath))
		file.write('read fname: %s \n'%(self.rprefix))
		file.write('write fname: %s \n'%(self.wprefix))
		file.close()
		# done with writing

		# let's run the analysis with a subprocess call
		lsdtt_pp = sub.call(self.LSDTT_path+'Analysis_driver/DEM_preprocessing.exe '+self.wpath + ' ' +self.wprefix + '_PreProcessing.param',shell = True)

		print("Done with the preprocessing")


	def basics_metric(self,topo = True,slope = True, curvature = True, plot = True):
		"""
    This function simply produces and plots a topographic map and a slope map.
    
      Args:
        topo (bool): If true, plot the topography
        slope (bool): If true calculate and plot a slope map
        curvature (bool): I true calculate and plot a curvature map
        plot (bool): If true make the call to the python plotting routine
        
        Author: BG
        
    """
		# writing the file
		# Writing the file
		param_name = self.wpath+self.wprefix+"_basic_analysis.param"
		file = open(param_name, 'w')
		file.write('# This is a parameter file for the chi_mapping_tool \n')
		file.write('# Documentation is here: https://lsdtopotools.github.io/LSDTT_documentation/LSDTT_chi_analysis.html \n')
		file.write(" \n")
		file.write('# These are parameters for the file i/o \n')
		file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
		file.write('read path: %s \n'%(self.rpath))
		file.write('write path: %s \n'%(self.wpath))
		file.write('read fname: %s \n'%(self.rprefix))
		file.write('write fname: %s \n'%(self.wprefix))
		file.write(" \n")
		file.write('write hillshade: %s \n'%(topo))#
		file.write('write slope: %s \n'%(slope))
		file.write('write curvature: %s \n'%(curvature))
		file.write(" \n")
		file.close()
		# done with writing the parameter file

		#analysis command
		Analysis_command = "%sAnalysis_driver/LSDTT_analysis_from_paramfile.out %s %s" %(self.LSDTT_path, param_name, self.wprefix)
				# Now call the subprocess
		sub.call(Analysis_command, shell = True)

				# Use the raster plotting python routine to plot the results. 
		if (plot):
			plotting_command = "python %sPlotBasicRaster.py -dir %s -fname %s -t %s -S %s -C %s" %(self.LSDMT_path,self.wpath,self.wprefix, topo, slope, curvature)
			sub.call(plotting_command, shell = True)



	def chi_mapping_tool_full(self,print_litho_info=False,litho_raster='NULL',minimum_elevation = 0, maximum_elevation = 30000, min_slope_for_fill = 0.0001, 
                              raster_is_filled = False, remove_seas = True ,only_check_parameters = False,print_raster_without_seas= False, 
                              CHeads_file = 'NULL', threshold_contributing_pixels = 200,minimum_basin_size_pixels = 5000, 
                              maximum_basin_size_pixels = 8000, test_drainage_boundaries = True, only_take_largest_basin = False, 
                              BaselevelJunctions_file = "NULL", extend_channel_to_node_before_receiver_junction = True,find_complete_basins_in_window = True, 
                              find_largest_complete_basins = False, print_basin_raster  = False, convert_csv_to_geojson = False,
                              print_stream_order_raster = False,print_channels_to_csv = False, print_junction_index_raster= False,
                              print_junctions_to_csv =False,print_fill_raster = False,print_DrainageArea_raster = False, 
                              write_hillshade = True,print_basic_M_chi_map_to_csv = False, ksn_knickpoint_analysis = False, A_0 = 1,m_over_n = 0.5,threshold_pixels_for_chi = 0, basic_Mchi_regression_nodes = 11,burn_raster_to_csv = False,burn_raster_prefix = 'NULL',
                              burn_data_csv_column_header = 'burned_data',secondary_burn_raster_to_csv = False,
                              secondary_burn_raster_prefix = 'NULL',secondary_burn_data_csv_column_header = 'secondary_burned_data', 
                              n_movern = 8, start_movern = 0.1, delta_movern = 0.1, only_use_mainstem_as_reference = True,calculate_MLE_collinearity = False,
                              collinearity_MLE_sigma = 1000, print_profiles_fxn_movern_csv = False, calculate_MLE_collinearity_with_points = False, 
                              calculate_MLE_collinearity_with_points_MC = False, MC_point_fractions = 5, MC_point_iterations = 1000,
                              max_MC_point_fraction = 0.5, movern_residuals_test = False, MCMC_movern_analysis = False, 
                              MCMC_movern_minimum = 0.05, MCMC_movern_maximum = 1.5, MCMC_chain_links = 5000, estimate_best_fit_movern = True,
                              SA_vertical_interval = 20,log_A_bin_width = 0.1,print_slope_area_data = False, segment_slope_area_data = False, 
                              slope_area_minimum_segment_length = 3, bootstrap_SA_data =False, N_SA_bootstrap_iterations = 1000,
                              SA_bootstrap_retain_node_prbability = 0.5,n_iterations = 20,minimum_segment_length = 10, maximum_segment_length = 100000, n_nodes_to_visit = 10, target_nodes = 80,skip = 2, sigma = 20,print_chi_coordinate_raster = False, print_simple_chi_map_to_csv = True, 
                              print_chi_data_maps = True, print_simple_chi_map_with_basins_to_csv = True,
                              print_segmented_M_chi_map_to_csv =True, print_source_keys = True, print_sources_to_csv = False, 
                              print_sources_to_raster =False, print_baselevel_keys = False, use_precipitation_raster_for_chi = False,  
                              print_discharge_raster = False,print_chi_no_discharge = False,check_chi_maps = False,
                              precipitation_fname = "NULL", print_segments = False, print_segments_raster = False):
		"""
    This function will manipulate the chi_mapping_tool.exe. I recommend creating intermediate functions to control this 
        massive function for specific purposes ex MuddChi_2014, Mudd_movern_2018, 
        
        SMM 26/06/2018: This takes every possible input to a chi mapping tool call and passes these as
        arguments. The defaults are set to the default values of the chi mapping tool
        See https://lsdtopotools.github.io/LSDTT_documentation/LSDTT_chi_analysis.html for documentation
        
    """
		# writing the file

		param_name = self.wpath+self.wprefix+"_Chiculations.param"
		file = open(param_name, 'w')
		file.write('# This is a parameter file for the chi_mapping_tool \n')
		file.write('# Documentation is here: https://lsdtopotools.github.io/LSDTT_documentation/LSDTT_chi_analysis.html \n')
		file.write(" \n")
		file.write('# These are parameters for the file i/o \n')
		file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
		file.write('read path: %s \n'%(self.rpath))
		file.write('write path: %s \n'%(self.wpath))
		file.write('read fname: %s \n'%(self.rprefix))
		file.write('write fname: %s \n'%(self.wprefix))
		file.write(" \n")
		file.write('minimum_elevation: %s \n'%(minimum_elevation))
		file.write('maximum_elevation: %s \n'%(maximum_elevation))
		file.write('min_slope_for_fill: %s \n'%(min_slope_for_fill))
		file.write('raster_is_filled: %s \n'%(to_cpp(raster_is_filled)))
		file.write('remove_seas: %s \n'%(to_cpp(remove_seas)))
		file.write('only_check_parameters: %s \n'%(to_cpp(only_check_parameters)))
		file.write('CHeads_file: %s \n'%(CHeads_file))
		file.write('start_movern: %s \n'%(to_cpp(start_movern)))
		file.write('delta_movern: %s \n'%(to_cpp(delta_movern)))
		file.write('only_use_mainstem_as_reference: %s \n'%(to_cpp(only_use_mainstem_as_reference)))
		file.write('calculate_MLE_collinearity: %s \n'%(to_cpp(calculate_MLE_collinearity)))
		file.write('collinearity_MLE_sigma: %s \n'%(to_cpp(collinearity_MLE_sigma)))
		file.write('print_profiles_fxn_movern_csv: %s \n'%(to_cpp(print_profiles_fxn_movern_csv)))
		file.write('calculate_MLE_collinearity_with_points: %s \n'%(to_cpp(calculate_MLE_collinearity_with_points)))
		file.write('calculate_MLE_collinearity_with_points_MC: %s \n'%(to_cpp(calculate_MLE_collinearity_with_points_MC)))
		file.write('MC_point_fractions: %s \n'%(to_cpp(MC_point_fractions)))
		file.write('print_chi_coordinate_raster: %s \n'%(to_cpp(print_chi_coordinate_raster)))
		file.write('print_chi_data_maps: %s \n'%(to_cpp(print_chi_data_maps)))
		file.write('print_simple_chi_map_to_csv: %s \n'%(to_cpp(print_simple_chi_map_to_csv)))
		file.write('print_simple_chi_map_with_basins_to_csv: %s \n'%(to_cpp(print_simple_chi_map_with_basins_to_csv)))
		file.write('print_segmented_M_chi_map_to_csv: %s \n'%(to_cpp(print_segmented_M_chi_map_to_csv)))
		file.write('print_basic_M_chi_map_to_csv: %s \n'%(to_cpp(print_basic_M_chi_map_to_csv)))
		file.write('print_source_keys: %s \n'%(to_cpp(print_source_keys)))
		file.write('print_sources_to_csv: %s \n'%(to_cpp(print_sources_to_csv)))
		file.write('print_sources_to_raster: %s \n'%(to_cpp(print_sources_to_raster)))
		file.write('print_baselevel_keys: %s \n'%(to_cpp(print_baselevel_keys)))
		file.write('use_precipitation_raster_for_chi: %s \n'%(to_cpp(use_precipitation_raster_for_chi)))
		file.write('print_discharge_raster: %s \n'%(to_cpp(print_discharge_raster)))
		file.write('print_chi_no_discharge: %s \n'%(to_cpp(print_chi_no_discharge)))
		file.write('check_chi_maps: %s \n'%(to_cpp(check_chi_maps)))
		file.write('precipitation_fname: %s \n'%(to_cpp(precipitation_fname)))
		file.write('print_segments: %s \n'%(to_cpp(print_segments)))
		file.write('print_segments_raster: %s \n'%(to_cpp(print_segments_raster)))
		file.write('print_litho_info: %s \n'%(to_cpp(print_litho_info)))
		file.write('litho_raster: %s \n'%(to_cpp(litho_raster)))
		file.write('estimate_best_fit_movern: %s \n'%(to_cpp(estimate_best_fit_movern)))
		file.write('SA_vertical_interval: %s \n'%(to_cpp(SA_vertical_interval)))
		file.write('log_A_bin_width: %s \n'%(to_cpp(log_A_bin_width)))
		file.write('print_slope_area_data: %s \n'%(to_cpp(print_slope_area_data)))
		file.write('segment_slope_area_data: %s \n'%(to_cpp(segment_slope_area_data)))
		file.write('slope_area_minimum_segment_length: %s \n'%(to_cpp(slope_area_minimum_segment_length)))
		file.write('bootstrap_SA_data: %s \n'%(to_cpp(bootstrap_SA_data)))
		file.write('N_SA_bootstrap_iterations: %s \n'%(to_cpp(N_SA_bootstrap_iterations)))
		file.write('SA_bootstrap_retain_node_prbability: %s \n'%(to_cpp(SA_bootstrap_retain_node_prbability)))
		file.write('n_iterations: %s \n'%(to_cpp(n_iterations)))
		file.write('minimum_segment_length: %s \n'%(to_cpp(minimum_segment_length)))
		file.write('maximum_segment_length: %s \n'%(to_cpp(maximum_segment_length)))
		file.write('n_nodes_to_visit: %s \n'%(to_cpp(n_nodes_to_visit)))
		file.write('target_nodes: %s \n'%(to_cpp(target_nodes)))
		file.write('skip: %s \n'%(to_cpp(skip)))
		file.write('MC_point_iterations: %s \n'%(to_cpp(MC_point_iterations)))
		file.write('max_MC_point_fraction: %s \n'%(to_cpp(max_MC_point_fraction)))
		file.write('movern_residuals_test: %s \n'%(to_cpp(movern_residuals_test)))
		file.write('MCMC_movern_analysis: %s \n'%(to_cpp(MCMC_movern_analysis)))
		file.write('MCMC_movern_minimum: %s \n'%(to_cpp(MCMC_movern_minimum)))
		file.write('MCMC_movern_maximum: %s \n'%(to_cpp(MCMC_movern_maximum)))
		file.write('MCMC_chain_links: %s \n'%(to_cpp(MCMC_chain_links)))
		file.write('print_stream_order_raster: %s \n'%(to_cpp(print_stream_order_raster)))
		file.write('print_raster_without_seas: %s \n'%(to_cpp(print_raster_without_seas)))
		file.write('threshold_contributing_pixels: %s \n'%(threshold_contributing_pixels))
		file.write('minimum_basin_size_pixels: %s \n'%(minimum_basin_size_pixels))
		file.write('maximum_basin_size_pixels: %s \n'%(maximum_basin_size_pixels))
		file.write('test_drainage_boundaries: %s \n'%(to_cpp(test_drainage_boundaries)))
		file.write('only_take_largest_basin: %s \n'%(to_cpp(only_take_largest_basin)))
		file.write('BaselevelJunctions_file: %s \n'%(BaselevelJunctions_file))
		file.write('extend_channel_to_node_before_receiver_junction: %s \n'%(to_cpp(extend_channel_to_node_before_receiver_junction)))
		file.write('find_complete_basins_in_window: %s \n'%(to_cpp(find_complete_basins_in_window)))
		file.write('find_largest_complete_basins: %s \n'%(to_cpp(find_largest_complete_basins)))
		file.write('print_basin_raster: %s \n'%(to_cpp(print_basin_raster)))
		file.write('convert_csv_to_geojson: %s \n'%(to_cpp(convert_csv_to_geojson)))
		file.write('print_channels_to_csv: %s \n'%(to_cpp(print_channels_to_csv)))
		file.write('print_junction_index_raster: %s \n'%(to_cpp(print_junction_index_raster)))
		file.write('print_junctions_to_csv: %s \n'%(to_cpp(print_junctions_to_csv)))
		file.write('print_fill_raster: %s \n'%(to_cpp(print_fill_raster)))
		file.write('write_hillshade: %s \n'%(to_cpp(write_hillshade)))
		file.write('print_basic_M_chi_map_to_csv: %s \n'%(to_cpp(print_basic_M_chi_map_to_csv)))
		file.write('ksn_knickpoint_analysis: %s \n'%(to_cpp(ksn_knickpoint_analysis)))
		file.write('A_0: %s \n'%(to_cpp(A_0)))
		file.write('m_over_n: %s \n'%(to_cpp(m_over_n)))
		file.write('threshold_pixels_for_chi: %s \n'%(to_cpp(threshold_pixels_for_chi)))
		file.write('basic_Mchi_regression_nodes: %s \n'%(to_cpp(basic_Mchi_regression_nodes)))
		file.write('burn_raster_to_csv: %s \n'%(to_cpp(burn_raster_to_csv)))
		file.write('burn_raster_prefix: %s \n'%(to_cpp(burn_raster_prefix)))
		file.write('burn_data_csv_column_header: %s \n'%(to_cpp(burn_data_csv_column_header)))
		file.write('secondary_burn_raster_to_csv: %s \n'%(to_cpp(secondary_burn_raster_to_csv)))
		file.write('secondary_burn_raster_prefix: %s \n'%(to_cpp(secondary_burn_raster_prefix)))
		file.write('secondary_burn_data_csv_column_header: %s \n'%(to_cpp(secondary_burn_data_csv_column_header)))
		file.write('n_movern: %s \n'%(to_cpp(n_movern)))
		file.write('print_stream_order_raster: %s \n'%(to_cpp(print_stream_order_raster)))



		file.write(" \n")
		file.close()
		# done with writing the parameter file

		#analysis command

		chi_mapping_tool_command = "%sdriver_functions_MuddChi2014/chi_mapping_tool.exe %s %s" %(self.LSDTT_path, self.wpath, self.wprefix+"_Chiculations.param")
		sub.call(chi_mapping_tool_command, shell = True)

	def basin_extraction(self, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, print_basin_raster = True, remove_seas = False, threshold_contributing_pixels = 5000, estimate_best_fit_movern = False, print_channels_to_csv = True, write_hillshade = True):
		"""
    Provides a simple basin extraction tool.
    
            Args:
                minimum_basin_size_pixels (int): The minimum basin size in pixels. 
                maximum_basin_size_pixels (int): The maximum basin size in pixels. The default will result in
                a quite large basin (or basins).
                print_basin_raster (bool): If true, calls the python plotting script for the basin.
                remove_seas (true): If true, set the remove_seas flag to true in the chi analysis. The 
                minimum and maximum elevations are the defaults so basically all this will do is it will turn
                points on the raster at sea level or lower to nodata. 
                threshold_contributing_pixels (int): The accumulated prixels needed to begin a channel. 
                estimate_best_fit_movern (bool): If true this triggers the full concavity analysis.
                It takes a long time!
                print_channels_to_csv (bool): If true you get a csv with channels. 
                You can use this for plotting.
                write_hillshade (bool): If true, writes the hillshade. If you set this to false it will mess up your plotting unless you have previously calculated the hillshade. 
            
            Author: Calum Bradbury - 30/11/2017
            
            

		"""

        # This calls the full chi mapping tool but with specific defaults set. 
		self.chi_mapping_tool_full(print_litho_info=False,litho_raster='Null',minimum_basin_size_pixels = minimum_basin_size_pixels, print_basin_raster = print_basin_raster, maximum_basin_size_pixels = maximum_basin_size_pixels, remove_seas = remove_seas, threshold_contributing_pixels = threshold_contributing_pixels, estimate_best_fit_movern = estimate_best_fit_movern, print_channels_to_csv = print_channels_to_csv, write_hillshade = write_hillshade)
  
    
	def ksn_calculation(self,print_basin_raster = True, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, m_over_n = 0.45, threshold_contributing_pixels = 5000, write_hillshade = True, plot = True):
		"""
			Provide a first-order ksn calculation for the  a range of basin, a threshold for river detection and a fixed concavity index.
            
            Args:
                print_basin_raster (bool): True if you want to print the basin raster to file
                minimum_basin_size_pixels (int): Does what it says on the tin.
                maximum_basin_size_pixels (int): Does what it says on the tin.
                m_over_n (float): The concavity you want to use for the analysis (m/n is legacy terminology)
                threshold_contributing_pixels (int): The number of pixels you need to accumulate to get a channel.
                write_hillshade (bool): If true write the hillshade raster
                plot (bool): If true call the LSDMappingTools plotting routines. 
                
    Author: Boris Gailleton - 16/11/2017
    
    """

        # Run the analysis in a subprocess
		self.chi_mapping_tool_full(print_basin_raster = print_basin_raster,minimum_basin_size_pixels = minimum_basin_size_pixels, maximum_basin_size_pixels = maximum_basin_size_pixels, m_over_n =m_over_n,threshold_contributing_pixels = threshold_contributing_pixels,write_hillshade = write_hillshade)
		
        # Plot results if that is what you want
		if (plot):
			plotting_command = "python %sPlotKnickpointAnalysis.py -dir %s -fname %s -mcstd True -mcbk True" %(self.LSDMT_path,self.wpath,self.wprefix)
			sub.call(plotting_command, shell = True)

	def chi_stats_only(self, m_over_n = 0.5):
		""""
			Provides extraction of the landscape chi coordinate only
            
            Args:
                m_over_n (float): The concavity for the chi calculation (added by SMM 26/06/2018)
                
			Author: Calum Bradbury - 07/03/2018
		"""
		self.chi_mapping_tool_full(threshold_contributing_pixels = 1000, m_over_n = m_over_n, print_chi_coordinate_raster = True,print_simple_chi_map_to_csv = True, print_chi_data_maps = True, test_drainage_boundaries = True,estimate_best_fit_movern = False,write_hillshade = False,threshold_pixels_for_chi = 0,only_use_mainstem_as_reference = True)

	def movern_calculation(self, print_litho_info, litho_raster, print_junctions_to_csv, n_movern =  18, start_movern = 0.1, delta_movern = 0.05, print_basin_raster = True, print_segmented_M_chi_map_to_csv =False, print_chi_data_maps = True, print_simple_chi_map_with_basins_to_csv =True, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, threshold_contributing_pixels = 5000, only_take_largest_basin = True, write_hillshade = True, plot = True,  minimum_elevation = 0, maximum_elevation= 30000,use_precipitation_raster_for_chi = False,precipitation_fname = "NULL",burn_raster_to_csv=False, burn_raster_prefix="NULL",secondary_burn_raster_to_csv=False,secondary_burn_raster_prefix="Null"):
		"""
    This runs the concavity analysis
            
            Args:
                print_litho_info (bool): If true prints the csv for lithology
                litho_raster (str): I (SMM) think this is the name of the lithology raster
                print_junctions_to_csv (bool): If true, print the locations of the junctions.
                Useful for later selecting specific basins.
                n_movern (int): The number of concavity index values you want to test
                start_movern (float): The starting concavity index
                delta_movern (float): The change in concavity index after each iteration
                print_basin_raster (bool): f true prints the basin raster. Used for plotting. 
                print_segmented_M_chi_map_to_csv (bool): If true prints the segmented channels. Uses default concavity (0.5).
                print_chi_data_maps (bool): If true pruint the data maps that are used for plotting.
                print_simple_chi_map_with_basins_to_csv (bool): This is superceded by the print_chi_data_maps but I (SMM) am leaving it in to avoid breaking Boris' code.
                minimum_basin_size_pixels (int): Does what it says on the tin.
                maximum_basin_size_pixels (int): Does what it says on the tin.
                m_over_n (float): The concavity you want to use for the analysis (m/n is legacy terminology)
                threshold_contributing_pixels (int): The number of pixels you need to accumulate to get a channel.
                write_hillshade (bool): If true write the hillshade raster
                plot (bool): If true call the LSDMappingTools plotting routines.
                
    Author: Boris Gailleton - 16/11/2017

    """
		self.chi_mapping_tool_full(burn_raster_to_csv=burn_raster_to_csv,burn_raster_prefix=burn_raster_prefix, secondary_burn_raster_to_csv=secondary_burn_raster_to_csv,secondary_burn_raster_prefix=secondary_burn_raster_prefix, print_litho_info=print_litho_info, litho_raster=litho_raster, print_junctions_to_csv=print_junctions_to_csv, n_movern = n_movern,start_movern = start_movern,delta_movern = delta_movern,estimate_best_fit_movern= True,print_basin_raster = print_basin_raster,minimum_basin_size_pixels = minimum_basin_size_pixels, maximum_basin_size_pixels = maximum_basin_size_pixels,threshold_contributing_pixels = threshold_contributing_pixels,only_take_largest_basin=only_take_largest_basin,write_hillshade = write_hillshade, minimum_elevation = minimum_elevation, maximum_elevation = maximum_elevation, use_precipitation_raster_for_chi = use_precipitation_raster_for_chi,precipitation_fname = precipitation_fname)
		if (plot):
			plotting_command = "python %sPlotMOverNAnalysis.py -dir %s -fname %s -ALL True" %(self.LSDMT_path,self.wpath,self.wprefix)
			sub.call(plotting_command, shell = True)    
    

	def knickpoint_calculation(self,print_basin_raster = True, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, m_over_n = 0.45, threshold_contributing_pixels = 5000, write_hillshade = True, plot = True):
		"""
    This runs the knickpoint detection routines
            
            Args:
                print_basin_raster (bool): If true, prints the basin raster. Needed for plotting.
                minimum_basin_size_pixels (int): Does what it says on the tin.
                maximum_basin_size_pixels (int): Does what it says on the tin.
                m_over_n (float): The concavity you want to use for the analysis (m/n is legacy terminology)
                threshold_contributing_pixels (int): The number of pixels you need to accumulate to get a channel.
                write_hillshade (bool): If true write the hillshade raster
                plot (bool): If true call the LSDMappingTools plotting routines.
                
    Author: Boris Gailleton - 16/11/2017
    
    """

		self.chi_mapping_tool_full(print_basin_raster = print_basin_raster,minimum_basin_size_pixels = minimum_basin_size_pixels, maximum_basin_size_pixels = maximum_basin_size_pixels, m_over_n =m_over_n,threshold_contributing_pixels = threshold_contributing_pixels,write_hillshade = write_hillshade, ksn_knickpoint_analysis = True)
		if (plot):
			plotting_command = "python %sPlotKnickpointAnalysis.py -dir %s -fname %s -ALL True" %(self.LSDMT_path,self.wpath,self.wprefix)
			sub.call(plotting_command, shell = True)
	
	def mchi_only(self,minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, m_over_n = 0.45, threshold_contributing_pixels = 5000, minimum_elevation = 0, maximum_elevation= 30000,burn_raster_to_csv=False, burn_raster_prefix="NULL",secondary_burn_raster_to_csv=False,secondary_burn_raster_prefix="Null"):
		
		"""
      Needed to recalculate mchi_segmented csvs for investigation of ksn values.
      Author: Calum Bradbury 03/07/2018
    """
		self.chi_mapping_tool_full(burn_raster_to_csv=burn_raster_to_csv,burn_raster_prefix=burn_raster_prefix,secondary_burn_raster_to_csv=secondary_burn_raster_to_csv,secondary_burn_raster_prefix=secondary_burn_raster_prefix, minimum_elevation = minimum_elevation, maximum_elevation= maximum_elevation,minimum_basin_size_pixels = minimum_basin_size_pixels,maximum_basin_size_pixels = maximum_basin_size_pixels, m_over_n =m_over_n,threshold_contributing_pixels = threshold_contributing_pixels, print_basin_raster = False,write_hillshade = False,estimate_best_fit_movern=False, print_simple_chi_map_to_csv = False,print_chi_data_maps = False, print_simple_chi_map_with_basins_to_csv = False,print_source_keys = False)

###### end of the class

def extract_file(fpath,fname,file_type = 'targz'):
	"""
    Extracts the targz file that you get from opentopography
                                                  
    Args: 
        fpath (str): The name of the path to which you will save the file
        fname (str): The name of the file (i.e., what you rename the file after downloading)
        file_type (str): You can also designate zip files if you want (the two types are targz and zip)
        
    Author: BG
    
  """
	
	if(file_type == 'targz'):
		extract_command = "tar xzvf %s"%(fpath+fname)
	elif(file_type == 'zip'):
		extract_command = "unzip %s"%(fpath+fname)
	else:
		extract_command = "tar xzvf %s"%(fpath+fname) 

	extract_popen = sub.call(extract_command, shell = True)


def OT_SRTM30_toLSDTT(fpath,fname, UTM_zone, out_full_name, reso = 30, south = False):
	"""
    This function takes a raster and converts it to one in UTM zone of your choice.
    It also resamples to a resolution of your choice using cubic sampling
    
    SMM Note: This should work for SRTM90 or any of the other opentopography data. Maybe rename this to be more general?
    
    Args: 
        fpath (str): The name of the path to which you will save the file
        fname (str): The name of the file (i.e., what you rename the file after downloading)
        UTM_zone (int): The UTM zone, duh
        out_full_name (str): The prefix of the outfile (I think you need .bil at the end)
        reso (float): The resolution in metres
        south (bool): If true in UTM south
        
    Author: BG
  """

	if(south):
		conversion_command = "gdalwarp -t_srs '+proj=utm +zone=%s +south +datum=WGS84' -of ENVI -r cubic -tr %s %s %s %s" %(UTM_zone,reso,reso,fpath+fname, fpath+out_full_name)

	else:
		conversion_command = "gdalwarp -t_srs '+proj=utm +zone=%s +datum=WGS84' -of ENVI -r cubic -tr %s %s %s %s" %(UTM_zone,reso,reso,fpath+fname, fpath+out_full_name)

	conversion_process = sub.call(conversion_command,shell = True)
	print("resolution is ",reso)

def get_SRTM30_from_point(fpath, fname, lat = 0, lon = 0, paddy_lat = 0.1, paddy_long = 0.2, get_main_basin = False, remove_old_files = True, return_iguanodon = False, return_extents = False, alos=False, SRTM90 = False):
	"""
    This function has a slightly misleading name since it gets rasters from a variety of data sources. 
    
    All the data come from OpenTopography but they host SRTM30, SRTM90 and ALOS 30data, all of which you can get. However the default is to get SRTM30 (or to be clearer, it will always get SRTM30 but
    you can get additional datasets)
    
    Args: 
        fpath (str): The name of the path to which you will save the file
        fname (str): The name of the file (i.e., what you rename the file after downloading)
        lat (float): The centre latitude
        long (float): The centre longitude
        paddy_lat (float): How far away from the centre, in each direction, the raster will extend in latitude.
        paddy_long (float): How far away from the centre, in each direction, the raster will extend in longitude.
        get_main_basin (bool): If true this then clips the raster to the biggest basin. It uses the basin spawner to do this so the resulting DEM is padded such that you can later use it for chi ananlysis.
        remove_old_files (bool): If true, deletes the old files (or overwrites them).
        return_iguanadon (bool): if true passes the Iguanodon31 object back so that it can be used for other things. 
        alos (bool): If true get ALOS data
        SRTM90 (bool): If true get SRTM90 data
        
    Author: CB?
  """

	# Calculation of the extents
	xmin = lon - paddy_long
	xmax = lon + paddy_long
	ymin = lat - paddy_lat
	ymax = lat + paddy_lat

	if(xmin>=xmax or ymin>= ymax):
		print("UNVALID PARAMETERS: the extend of the wanted raster are not valid. Check it.")
		print("This error is here because your xmax or ymax were less than your xmin or ymin")
	#allows use of ALOS raster
	if alos:
		wget_command = 'wget -O %s "http://opentopo.sdsc.edu/otr/getdem?demtype=AW3D30&west=%s&south=%s&east=%s&north=%s&outputFormat=GTiff"'%(fpath+fname,xmin,ymin,xmax,ymax)
	if SRTM90:
		wget_command = 'wget -O %s "http://opentopo.sdsc.edu/otr/getdem?demtype=SRTMGL3&west=%s&south=%s&east=%s&north=%s&outputFormat=GTiff"'%(fpath+fname,xmin,ymin,xmax,ymax)
	else:
		wget_command = 'wget -O %s "http://opentopo.sdsc.edu/otr/getdem?demtype=SRTMGL1&west=%s&south=%s&east=%s&north=%s&outputFormat=GTiff"'%(fpath+fname,xmin,ymin,xmax,ymax)
	wget_process =  sub.call(wget_command, shell = True)
	# Dealing with the conversion
	temp_info = utm.from_latlon(lat,lon)
	if(temp_info[3] in ['X','W','V','U','T','S','R','Q','P','N']):
		south = False
	else:
		south = True
	if SRTM90:
		reso = 90
	else:
		reso = 30


	OT_SRTM30_toLSDTT(fpath, fname,temp_info[2],fname+".bil",reso = reso, south = south)
	if(return_extents):
		return xmin,ymin,xmax,ymax
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
		file.write('# Documentation is here: https://lsdtopotools.github.io/LSDTT_documentation/LSDTT_chi_analysis.html \n')
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
		LSD_folder = setup_file.readline().rstrip()
		setup_file.close()


		lsdtt_pp = sub.call(LSD_folder+'Analysis_driver/basin_averager.out '+fpath + ' ' +fname + '_trimming.param',shell = True)
		print("Done with basin spawning")

		if(remove_old_files):
			os.remove(fpath+fname+'.bil') # Removing the bil file
			os.remove(fpath+fname+'.hdr') # Removing the header file
			os.rename(fpath+fname+"_Spawned_0.bil",fpath+fname+".bil") # Renaming the older file
			os.rename(fpath+fname+"_Spawned_0.hdr",fpath+fname+".hdr") # Renaming the older file

	if(return_iguanodon):
		IG = Iguanodon31(fpath, fname, writing_path = fpath, writing_prefix = fname, data_source = 'ready', preprocessing_raster = False, UTM_zone = temp_info[2], south = south)
		return IG
    
def get_ALOS30_from_point(fpath, fname, lat = 0, lon = 0, paddy_lat = 0.1, paddy_long = 0.2, get_main_basin = False, remove_old_files = True, return_iguanodon = False):
	"""
    This gets ALOS data from OpenTopography
    
    Args: 
        fpath (str): The name of the path to which you will save the file
        fname (str): The name of the file (i.e., what you rename the file after downloading)
        lat (float): The centre latitude
        long (float): The centre longitude
        paddy_lat (float): How far away from the centre, in each direction, the raster will extend in latitude.
        paddy_long (float): How far away from the centre, in each direction, the raster will extend in longitude.
        get_main_basin (bool): If true this then clips the raster to the biggest basin. It uses the basin spawner to do this so the resulting DEM is padded such that you can later use it for chi ananlysis.
        remove_old_files (bool): If true, deletes the old files (or overwrites them).
        return_iguanadon (bool): if true passes the Iguanodon31 object back so that it can be used for other things. 
    
    Author: BG
    
  """

	# Calculation of the extents
	xmin = lon - paddy_long
	xmax = lon + paddy_long
	ymin = lat - paddy_lat
	ymax = lat + paddy_lat

	if(xmin>=xmax or ymin>= ymax):
		print("UNVALID PARAMETERS: the extend of the wanted raster are not valid. Check it.")
	wget_command = 'wget -O %s "http://opentopo.sdsc.edu/otr/getdem?demtype=ALOS&west=%s&south=%s&east=%s&north=%s&outputFormat=GTiff"'%(fpath+fname,xmin,ymin,xmax,ymax)
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
		file.write('# Documentation is here: https://lsdtopotools.github.io/LSDTT_documentation/LSDTT_chi_analysis.html \n')
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
		LSD_folder = setup_file.readline().rstrip()
		setup_file.close()


		lsdtt_pp = sub.call(LSD_folder+'Analysis_driver/basin_averager.out '+fpath + ' ' +fname + '_trimming.param',shell = True)
		print("Done with basin spawning")

		if(remove_old_files):
			os.remove(fpath+fname+'.bil') # Removing the bil file
			os.remove(fpath+fname+'.hdr') # Removing the header file
			os.rename(fpath+fname+"_Spawned_0.bil",fpath+fname+".bil") # Renaming the older file
			os.rename(fpath+fname+"_Spawned_0.hdr",fpath+fname+".hdr") # Renaming the older file

	if(return_iguanodon):
		IG = Iguanodon31(fpath, fname, writing_path = fpath, writing_prefix = fname, data_source = 'ready', preprocessing_raster = False, UTM_zone = temp_info[2], south = south)
		return IG


def Analysis_from_multiple_lat_long(csv_path,csv_fname, get_raster = False, multiprocessing = 1):
	"""
  
    This function provides a full range of analysis for a list of basins from a csv_file.
    It will create one folder per file, the prefix and foldername will be in the csv file formatted as follow:
    prefix,longitude,latitude
    ex1,23.45,54.9
    ex2,11.23,78.87
    
    
      Args:
        csv_path (str): The directory of the path with the csv file that contains the lat-long
        csv_fname (str): The name of the csv file
        get_raster (bool): If true, fetch the raster from a data repository (at the moment SRTM30 from OpenTopography)
        multiprocessing (int): This isn't implemented at the moment but in the future will call multiple subprocesses. 

    Author: Boris Gailleton - 16/11/2017

  """
	list_of_files = []
	prefix_col = 0
	longitude_col = 0
	latitude_col = 0
	if (multiprocessing>1):
		print("I still need to code the multiprocessing sorry")
		multiprocessing = 1
	else:
		print("I didn't get your multiprocessing info, make sure it is an integer >= 1, I am recasting to 1")
		multiprocessing = 1

	if(get_raster):

		file = open(csv_path+csv_fname, "r")
		header = file.readline().rstrip().split(",")

		# getting the place of all the three column
		for i in range(len(header)):
			print(header[i])
			if(header[i].lower().rstrip() == "prefix"):
				prefix_col = i
			elif(header[i].lower().rstrip() in ["longitude","lon"]):
				longitude_col = i
			elif(header[i].lower().rstrip() in ["latitude","lat"]):
				latitude_col = i
		
		# print("longitude column is "+str(longitude_col))
		# print("latitude column is "+str(latitude_col))
		# print("prefix column is "+str(prefix_col))
		# quit()
		# getting the rest of the informations

        # This reads the list of files, creates an Iguanodon31 object for each one,
        # and then uses that object to grab data from OpenTopography.org 
		for line in file.readlines():
			temp = line.rstrip().split(",")
			this_dict = {}
			this_dict["path"] = csv_path+temp[prefix_col]+'/'
			this_dict["prefix"] = temp[prefix_col]
			this_dict["lat"] = temp[latitude_col]
			this_dict["lon"] = temp[longitude_col]

			if not os.path.isdir(this_dict["path"]):
				os.makedirs(this_dict["path"])

			thisIG = get_SRTM30_from_point(this_dict["path"], this_dict["prefix"], lat = float(this_dict["lat"]), lon = float(this_dict["lon"]), paddy_lat = 0.1, paddy_long = 0.2, get_main_basin = True, remove_old_files = True, return_iguanodon = True)
			list_of_files.append(thisIG)
		file.close()

	else:
		# If you just want to read your files already dowloaded with the same pattern
        # SMM: This skips the downloading part if you have already grabbed the rasters
		list_of_files = []
		file = open(csv_path+csv_fname, "r")
		header = file.readline().rstrip().split(",")
		for i in range(len(header)):
			if(header[i].lower() == "prefix"):
				prefix_col = i
			elif(header[i].lower() in ["longitude","lon"]):
				longitude_col = i
			elif(header[i].lower() in ["latitude","lat"]):
				latitude_col = i

		for line in file.readlines():
			temp = line.rstrip().split(",")
			this_IG = Iguanodon31(csv_path+'/'+temp[prefix_col]+"/", temp[prefix_col], data_source = 'ready', preprocessing_raster = False)
			list_of_files.append(this_IG)



	print("I am done with loading your files, let me proceed to the Analysis")
    # EThe previous steps have generated an Iguanodon31 object from the file list, 
    # and now we loop through those objects to run the analyses. 
	for Iguanodons in list_of_files:
		Iguanodons.ksn_calculation(print_basin_raster = True, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, m_over_n = 0.45, threshold_contributing_pixels = 5000, write_hillshade = True, plot = True)
		Iguanodons.movern_calculation(n_movern =  18, start_movern = 0.1, delta_movern = 0.05, print_basin_raster = True, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, threshold_contributing_pixels = 5000, write_hillshade = True, plot = True)
		Iguanodons.knickpoint_calculation(print_basin_raster = True, minimum_basin_size_pixels = 10000, maximum_basin_size_pixels = 90000000, m_over_n = 0.45, threshold_contributing_pixels = 5000, write_hillshade = True, plot = True)
		Iguanodons.basics_metric()
	print("I am done")





def bool_for_cpp(boo):
	"""
    This just converts a python boolean into a string that is readable by c++ code
    
    Args:
        boo (bool): A python boolean to be converted to a string. 
    
    Author: BG
  """
	stre = ''
	if(boo):
		stre = 'true'
	else:
		stre = 'false'
	return stre

def to_cpp(ar):
	"""
    SMM: Not sure what the point of this is. 
    
  """
	if(isinstance(ar,bool)):
		ar = bool_for_cpp(ar)
	return ar