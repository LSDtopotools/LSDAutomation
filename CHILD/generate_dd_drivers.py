##generate_dd_drivers.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function takes one driver file for the channel network extraction algorithm
## and the drainage density analysis and generates many driver files with different 
## seed numbers for different CHILD runs.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 08/07/2015
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def generate_dd_drivers():
    
    # number of seed values you want to generate drivers for
    n_seed = 4
    
    # starting seed value (will increment by 1 for n_seed)
    starting_seed = 1
    
    # uplift rate of CHILD runs
    uprate = "Up030"
    
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # det the directory and filename
    DataDirectory =  'Z:\\CHILD\\CHILD_Fiona\\Runs_n1\\Error_bars\\drivers_for_analysis\\' 
    ChannelHeadsDriverFile = 'channel_heads_child.driver'
    DrainageDensityDriverFile = 'drainage_density_child.driver'
  
    # combine these
    ChannelHeadsFileName = DataDirectory+ChannelHeadsDriverFile
    DrainageDensityFileName = DataDirectory+DrainageDensityDriverFile
    
    print "Channel heads driver is "+ChannelHeadsFileName
    print "Drainage density driver is "+DrainageDensityFileName
  
  
    # get the prefix of the channel heads file
    split_fname = ChannelHeadsDriverFile.split('.')
    no_tree_levs = len(split_fname) 
    fname_prefix  = split_fname[0]  
    if (no_tree_levs > 2):
        for i in range (1,no_tree_levs-1):
            fname_prefix+= "."+split_fname[i]
    
    print "The channel heads file prefix is: " + fname_prefix
    
    # get the prefix of the drainage density file

    split_fname2 = DrainageDensityDriverFile.split('.')
    no_tree_levs2 = len(split_fname2) 
    fname_prefix2  = split_fname2[0]  
    if (no_tree_levs2 > 2):
        for i in range (1,no_tree_levs2-1):
            fname_prefix2+= "."+split_fname2[i]
    
    print "The drainage density file prefix is: " + fname_prefix2

    # get the data from the channel heads driver   
    f = open(ChannelHeadsFileName,'r')  # open file
    lines = f.readlines()   # read in the data
    f.close()
    
    # overwrite the channel head driver lines to read in the correct float file
    counter = 0
    for seed in range(0,n_seed):
        counter+=1
        starting_seed = starting_seed+1            
        
        print "seed value = " +str(starting_seed)            

        lines[0] = 'LowRes_'+uprate+'_kb00001_s' +str(starting_seed)+'_ts6_xyz\n'            
                    
        print lines
                    
        this_fname = fname_prefix+"."+str(counter)+".driver"
        f = open(DataDirectory + this_fname,'w')  # open file
        f.writelines(lines)
        f.close()
        
    # get the data from the drainage_density driver   
    f = open(DrainageDensityFileName,'r')  # open file
    lines = f.readlines()   # read in the data
    f.close()
    
    starting_seed = 1
    # overwrite the drainage density driver lines to read in the correct float file
    counter = 0
    for seed in range(0,n_seed):
        counter+=1
        starting_seed = starting_seed+1            
        
        print "seed value = " +str(starting_seed)            

        lines[0] = 'LowRes_'+uprate+'_kb00001_s' +str(starting_seed)+'_ts6_xyz\n'
        lines[1] = 'LowRes_'+uprate+'_kb00001_s' +str(starting_seed)+'_ts6_xyz_CH'+'\n'            
                    
        print lines
                    
        this_fname = fname_prefix2+"."+str(counter)+".driver"
        f = open(DataDirectory + this_fname,'w')  # open file
        f.writelines(lines)
        f.close()
                    
if __name__ == "__main__":
    generate_dd_drivers()
    