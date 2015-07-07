## chi_multidriver_gen_qsub_ver.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
'''
This function generates a series of driver files for different basins (junc indexes)
The user can modify the script to change the required parameters in the driver
files. 

This version reads from a separate file containing the basin name, junction index
(the first two columns).

This version produces driver files with a naming convention suitable for use 
with a job-queueing utility such as qsub or pbs or xjobs. i.e. the driver files'
names increase monotonically from 1 to n. wasatch_1.driver, wasatch_2.driver etc...

INPUTS
'base' driver file
junction index list file  #IMPORTANT: make sure this does not have a blank line
at the end of the file. (I.e. no newline characters on the last item)

OUTPUTS
n number of .driver files, where n is the number of basins listed in the junction
index list file.
'''
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DAV May-2014
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import numpy as np

def multinbasin_driver_gen():
    
    driver_file = 'wasatch_standard_params.driver'   # the file you are going to use as your 'standard'
    junction_file = 'catchment_list_wasatch_frontonly_10mNED.streams' # the file with a list of your basin JIs

    ##################################
    #                                #
    #   READ IN THE JUNCTION FILE    #
    #                                #
    ##################################

    # fixed values in the driver files that you want to set
    forced_mn_value = 0.475
    area_thin_fraction = 0.005
    
    with open(junction_file,'r') as f:
        junc_lines = f.readlines()
    
    with open(junction_file) as jf:
        for i, l in enumerate(jf):
            pass        # Can't have an empty 'for' block; 'pass' is placeholer
    file_len = i + 1 
    #print file_len

    ################################
    ### GET THE JUNCTION NUMBERS ###
    ################################
    '''
    A (rather long-winded) way to take the list of junction indices from the 
    JI file and store them in a list. (Can they not be read directly into
    a list or array, e.g. using np.loadtxt??)  DAV
    '''

    JI_array = []

    for i, line in enumerate(junc_lines):
        JI = line.strip().split(" ")
        JI_array.append(JI[1:])
        
        print JI
								
    JI_ints = [map(int, x) for x in JI_array]    #Convert all the strings to integers   
    JI_list = [l[0] for l in JI_ints]      #Flatten the 'list of lists'
    print JI_list

    #########################
    #                       #
    #   READ IN THE DRIVER  #
    #                       #
    #########################
    
    with open(driver_file, 'r') as g:
        driver_lines = g.readlines()   # read all the lines in the driver file
    
    #with open(driver_file) as df:
    for JI_i in range(0,file_len):
        this_JI = JI_list[JI_i]
        
        driver_lines[3] = str(this_JI)+'\n'    
        # remember python starts counting at 0! Don't overwrite the wrong line!
        driver_lines[4] = str(area_thin_fraction)+'\n' 
        driver_lines[8] = str(forced_mn_value)+'\n'
        driver_lines[9] = str(0)+'\n' # Basically, this is a hack to produce only one value of m/n to test
        driver_lines[10] = str(1)+'\n'
     
    ################################ 
    ## SPAWN THE NEW DRIVER FILES ##
    ################################ 
        
        new_driver_name = "wasatch_" + str(JI_i + 1) + ".driver"   
        #note: JI_i is not the junction index, it is the junction-index index. 
        with open(new_driver_name, 'w') as h:  # open a new driver file 
            h.writelines(driver_lines)
        
        #print driver_lines[3]
        #print this_JI

if __name__ == "__main__":
    multinbasin_driver_gen()
