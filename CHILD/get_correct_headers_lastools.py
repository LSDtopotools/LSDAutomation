##get_correct_headers.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function takes the header files generated through LASTools and changes 
## them to headers that can be read by LSDTopoTools.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 07/07/2015
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import os
from glob import glob

def get_correct_headers():
        
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # det the directory and filename
    DataDirectory =  'Z:\\CHILD\\CHILD_Fiona\\Runs_n1\\Error_bars\\' 
    
    for FileName in glob(DataDirectory+"*.hdr"): 
        
        print FileName
           
        f = open(FileName, 'r') # open file
        lines = f.readlines() # read in the data
        f.close()
        
        temp_lines = []
        
        temp_lines.append(lines[1])
        temp_lines.append(lines[2])
        temp_lines.append(lines[4])
        temp_lines.append(lines[5])
        temp_lines.append(lines[6])
        temp_lines.append(lines[3])
        temp_lines.append(lines[7])
        
        print temp_lines
        
        f = open(FileName, 'w') # open file to overwrite
        f.writelines(temp_lines)
        f.close()
                    
if __name__ == "__main__":
    get_correct_headers()
    