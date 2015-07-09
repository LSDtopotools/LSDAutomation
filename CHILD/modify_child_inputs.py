## modify_child_inputs.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function takes the .in files used in CHILD runs and changes the value of 
## certain parameters to those specified in the function
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 07/07/2015
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import os
from glob import glob

def modify_child_inputs():
    
    ##########################
    #                        #
    #  PARAMETERS TO MODIFY  #
    #                        # 
    ##########################
    
    # value of nb in file    
    n = 2
        
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # det the directory and filename
    DataDirectory =  'Z:\\CHILD\\CHILD_Fiona\\Runs_n2_unchanged\\Error_bars\\' 
    
    for FileName in glob(DataDirectory+"*.in"): 
        
        print FileName
           
        f = open(FileName, 'r') # open file
        lines = f.readlines() # read in the data
        f.close()
        
        # modify the n value in the file
        lines[123] = str(n)+'\n'
        
        f = open(FileName, 'w')
        f.writelines(lines)
        f.close()
                    
if __name__ == "__main__":
    modify_child_inputs()
    