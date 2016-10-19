# This is a python script for setting up LSDTopoTools on your computer
# It creates a directory structure, clones the appropriate repositories
# And makes the programs. 
# @author Simon M Mudd
# @date 16-10-2016

import os
import subprocess
import sys, getopt
import time

#=============================================================================
# This function gets the base directory
#=============================================================================
def GetBaseDirectory(WantHomeDirectory = True):
    
    # First, we need to find out if we are on vagrant
    home_dir = os.path.expanduser("~")
    this_dir = os.getcwd()
    
    print "\n\nI am first going to figure out where I will install the directory structures."
    print "Your home directory is: "+home_dir
    
    # Now we go through some logic that tests if we are in a vagrant machine
    vagrant_str = "vagrant"
    if vagrant_str in home_dir:
        print "You seem to be on a vagrant machine"
        vagrant_switch = True
        the_base_directory = "/"
    else:
        vagrant_switch = False
        print "You don't seem to be using vagrant."
        if WantHomeDirectory == True:
            print "I am going to install on your home directory, which is here:"
            print home_dir
            the_base_directory = home_dir+"/"
        else:
            print "You set the WantHomeDirectory to false, so I am going to install here:"
            print this_dir
            the_base_directory = this_dir+"/"
    
    print "\n\nThe location of your LSDTopoTools build is:"
    print the_base_directory
    return the_base_directory
#=============================================================================
    
    
#=============================================================================
# This function builds the directory trees
#=============================================================================
def BuildDirectoryTree(the_base_directory):
    
    print "I am now going to build the initial directory structure."
    print "Your base directory is: " 
    print the_base_directory
    
    # first find the LSDTopoTools directory
    path = the_base_directory+"LSDTopoTools/"
    if not os.access(path,os.F_OK):
        print "Making path: "
        os.mkdir(path)
        print path
    else:
        print "Path: " +path+" already exists."   
        
    # first find the Git_projects directory
    path = the_base_directory+"LSDTopoTools/Git_projects"
    if not os.access(path,os.F_OK):
        print "Making path: "
        os.mkdir(path)
        print path
    else:
        print "Path: " +path+" already exists."          
        
    # first find the Git_projects directory
    path = the_base_directory+"LSDTopoTools/Topographic_projects"
    if not os.access(path,os.F_OK):
        print "Making path: "
        os.mkdir(path)
        print path
    else:
        print "Path: " +path+" already exists."  
#=============================================================================
        
        
               
#=============================================================================
# This function clones both the test data and the workshop data from github
#=============================================================================
def CloneData(the_base_directory):
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
    
    print "I am going to check the test data files."
    file = the_base_directory+"/LSDTopoTools/Topographic_projects/Test_data/Mandakini.bil"
    if not os.path.isfile(file):
        print "There is no test data. Cloning in a subprocess"
        repo_address = "https://github.com/LSDtopotools/LSDTT_vagrant_datasets.git"
        target_directory = the_base_directory+"/LSDTopoTools/Topographic_projects/Test_data"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        git_worktree = "--work-tree="+the_base_directory+"LSDTopoTools/Topographic_projects/Test_data/"
        git_dir = "--git-dir="+the_base_directory+"LSDTopoTools/Topographic_projects/Test_data/.git"
        #print "I am calling a subprocess with the following entries:"
        #print git
        #print git_worktree
        #print git_dir      
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])
    
    print "\n\nI am going to check the workshop data files."
    file = the_base_directory+"/LSDTopoTools/Topographic_projects/LSDTT_workshop_data/WA.bil"
    if not os.path.isfile(file):
        print "There is no test data. Cloning in a subprocess"
        repo_address = "https://github.com/LSDtopotools/LSDTT_workshop_data.git"
        target_directory = the_base_directory+"LSDTopoTools/Topographic_projects/LSDTT_workshop_data"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        git_worktree = "--work-tree="+the_base_directory+"LSDTopoTools/Topographic_projects/LSDTT_workshop_data/"
        git_dir = "--git-dir="+the_base_directory+"LSDTopoTools/Topographic_projects/LSDTT_workshop_data/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])          
#=============================================================================



#=============================================================================
# This function clones and makes the analysis driver
#=============================================================================
def CloneMakeAnalysisDriver(the_base_directory):
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
    
    print "I am going to check if the repository exists."
    file = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/LSDRaster.cpp"
    if not os.path.isfile(file):
        print "I don't see the LSDraster.cpp. I am going to try cloning the LSDTopoTools_AnalysisDriver repo."
        repo_address = "https://github.com/LSDtopotools/LSDTopoTools_AnalysisDriver.git"
        target_directory = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        git_worktree = "--work-tree="+the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/"
        git_dir = "--git-dir="+the_base_directory+"/LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])    
        
    print "I've got the repository. Now I am going to make the program for you."
    make = "make"
    C_flag = "-C"
    LSDTTpath = "LSDTopoTools/Git_projects/"
    f_flag = "-f"
    target_path = the_base_directory+LSDTTpath+"LSDTopoTools_AnalysisDriver/Analysis_driver/"
    target_makefile = "Drive_analysis_from_paramfile.make"
    
    target = target_path+target_makefile
    print target
    
    #Let me just check to make sure the target makefile exists
    #if not os.access(target_path,os.F_OK):
        
    if not os.path.isfile(target):
        print "The makefile doesn't exist. Check your filenames and paths."
    else:
        print "Makefile is here, lets run make!"
        
    subprocess.call([make,C_flag,target_path,f_flag,target_makefile])
    print "You Analysis_driver is now ready to run!"
    #print "Note if make said it didn't have anything to do it means you already compiled the program."
#=============================================================================        


#=============================================================================
# This function clones and makes the Chi Tool
#=============================================================================
def CloneMakeChiTools(the_base_directory):
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
 
    # The below logic checks to see if the repo exist. If not it clones, if so it pulls, both using a 
    # subprocess call to git
    print "I am going to check if the repository exists."
    file = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/LSDRaster.cpp"
    if not os.path.isfile(file):
        print "I don't see the LSDraster.cpp. I am going to try cloning the LSDTopoTools_ChiMudd2014 repo."
        repo_address = "https://github.com/LSDtopotools/LSDTopoTools_ChiMudd2014.git"
        target_directory = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        git_worktree = "--work-tree="+the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/"
        git_dir = "--git-dir="+the_base_directory+"/LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])    
        
    print "I've got the repository. Now I am going to make the program for you."
    make = "make"
    C_flag = "-C"
    LSDTTpath = "LSDTopoTools/Git_projects/"
    f_flag = "-f"
    target_path = the_base_directory+LSDTTpath+"LSDTopoTools_ChiMudd2014/driver_functions_MuddChi2014/"
    target_makefile = "chi_mapping_tool.make"
    
    target = target_path+target_makefile
    print target
    
    #Let me just check to make sure the target makefile exists
    #if not os.access(target_path,os.F_OK):
        
    if not os.path.isfile(target):
        print "The makefile doesn't exist. Check your filenames and paths."
    else:
        print "Makefile is here, lets run make!"
        
    subprocess.call([make,C_flag,target_path,f_flag,target_makefile])
    print "You Chi tool is now ready to run!"
    #print "Note if make said it didn't have anything to do it means you already compiled the program."
#=============================================================================   

#=============================================================================
# This function clones the CRN repo and makes the CAIRN tool
#=============================================================================
def CloneMakeCRN_CAIRN(the_base_directory):
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
 
    # The below logic checks to see if the repo exist. If not it clones, if so it pulls, both using a 
    # subprocess call to git
    print "I am going to check if the repository exists."
    file = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_CRNBasinwide/LSDRaster.cpp"
    if not os.path.isfile(file):
        print "I don't see the LSDraster.cpp. I am going to try cloning the LSDTopoTools_CRNBasinwide repo."
        repo_address = "https://github.com/LSDtopotools/LSDTopoTools_CRNBasinwide.git"
        target_directory = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_CRNBasinwide"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        git_worktree = "--work-tree="+the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_CRNBasinwide/"
        git_dir = "--git-dir="+the_base_directory+"/LSDTopoTools/Git_projects/LSDTopoTools_CRNBasinwide/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])    
        
    print "I've got the repository. Now I am going to make the program for you."
    make = "make"
    C_flag = "-C"
    LSDTTpath = "LSDTopoTools/Git_projects/"
    f_flag = "-f"
    target_path = the_base_directory+LSDTTpath+"LSDTopoTools_CRNBasinwide/driver_functions_CRNBasinwide/"
    target_makefile = "Basinwide_CRN.make"
    
    # Get the list of makefiles
    makefile_list = []
    makefile_list.append("Basinwide_CRN.make")
    makefile_list.append("Soil_CRN.make")
    makefile_list.append("Nested_CRN.make")
    makefile_list.append("Check_CRN_basins.make")
    makefile_list.append("Shielding_for_CRN.make")
    makefile_list.append("SimpleSnowShield.make")
    makefile_list.append("Spawn_DEMs_for_CRN.make")
    
    # Loop through the makefile list, calling make as you go using a subprocess
    for target_makefile in makefile_list:
        
        print "I am making using the makefile: "+target_makefile
    
        target = target_path+target_makefile
        
        # Check to see if the makefile is here
        if not os.path.isfile(target):
            print "The makefile doesn't exist. Check your filenames and paths."
        else:
            print "Makefile is here, lets run make!"
        
        # Call make via subprocess
        subprocess.call([make,C_flag,target_path,f_flag,target_makefile])
        
    print "You CRN tools are now ready to run!"
    #print "Note if make said it didn't have anything to do it means you already compiled the program."
#=============================================================================   



#=============================================================================
# This function clones and makes the programs for the analysis in Mudd et al 2014 JGR-ES
#=============================================================================
def CloneMakeChiMudd(the_base_directory):
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
    
    # The below logic checks to see if the repo exist. If not it clones, if so it pulls, both using a 
    # subprocess call to git
    print "I am going to check if the repository exists."
    file = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/LSDRaster.cpp"
    if not os.path.isfile(file):
        print "I don't see the LSDraster.cpp. I am going to try cloning the LSDTopoTools_ChiMudd2014 repo."
        repo_address = "https://github.com/LSDtopotools/LSDTopoTools_ChiMudd2014.git"
        target_directory = the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        git_worktree = "--work-tree="+the_base_directory+"LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/"
        git_dir = "--git-dir="+the_base_directory+"/LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])    
        
    print "I've got the repository. Now I am going to make the program for you."
    make = "make"
    C_flag = "-C"
    LSDTTpath = "LSDTopoTools/Git_projects/"
    f_flag = "-f"
    target_path = the_base_directory+LSDTTpath+"LSDTopoTools_ChiMudd2014/driver_functions_MuddChi2014/"
    
    # Get the list of makefiles
    makefile_list = []
    makefile_list.append("chi_step1_write_junctions.make")
    makefile_list.append("chi_step2_write_channel_file.make")
    makefile_list.append("chi_get_profiles.make")
    makefile_list.append("chi_m_over_n_analysis.make")
    
    # Loop through the makefile list, calling make as you go using a subprocess
    for target_makefile in makefile_list:
        
        print "I am making using the makefile: "+target_makefile
    
        target = target_path+target_makefile
        
        # Check to see if the makefile is here
        if not os.path.isfile(target):
            print "The makefile doesn't exist. Check your filenames and paths."
        else:
            print "Makefile is here, lets run make!"
        
        # Call make via subprocess
        subprocess.call([make,C_flag,target_path,f_flag,target_makefile])
    
    print "I've compiled everything you need to run the Mudd et al 2014 JGR-ES analyses!"
    #print "Note if make said it didn't have anything to do it means you already compiled the program."       
#=============================================================================   

#=============================================================================
# This is the main function that drives all cloning and directory creation
#=============================================================================
def LSDTopoToolsDefault(the_base_directory):
    
    print "=================================================="
    print "Welcome to the LSDTopoTools setup tool!"
    print "This tool will:"
    print " 1. Build a directory structure."
    print " 2. Clone a few of the LSDTopoTools packages."
    print " 3. Clone some test data."
    print " 4. Compile tre programs using the make utility."
    print "IMPORTANT: You need to be on a Linux operating system for this to work."
    print "If you are not on a Linux operating system, you should use our Vagrant tools:"
    print "http://lsdtopotools.github.io/LSDTT_book/#_installing_lsdtopotools_using_virtualbox_and_vagrant"
    print "==================================================="
    print "This software was written by:"
    print "Simon M. Mudd, David Milodowski, Stuart Grieve, Fiona Clubb, "
    print "Declan Valters, and Martin Hurst at the"
    print "Universities of Edinburgh, Manchester and Glasgow"
    print "==================================================="
    print "For an overview of the software please visit:"
    print "http://lsdtopotools.github.io"
    print "For detailed documentation visit"
    print "http://lsdtopotools.github.io/LSDTT_book"
    print "==================================================="
    print "If you are on vagrant, directories should already be there in root"
    print "If you are not on vagrant, the default is to install in your home directory."
    print "If you run this program with a False argument it will install the"
    print "Directory tree in the current directory."
    print "==================================================="    
    
    print "Note: if you are in vagrant the base directories should already exist."
    BuildDirectoryTree(the_base_directory)
            
    print "\n\nI've built the directories. I will now clone the test data."
    CloneData(the_base_directory)  
    
    print "\n\nNow I'll get the analysis driver and compile it."
    CloneMakeAnalysisDriver(the_base_directory)
    
    print "\n\nNow I'll get the chi tool and compile it."
    CloneMakeChiTools(the_base_directory)
        
#=============================================================================

#=============================================================================
# This is the main function that runs the whole thing 
#=============================================================================
def main(argv):
 
    # If there are no arguments, send to the welcome screen
    if not len(sys.argv) > 1:
        print_welcome()
        sys.exit()

    # Get the arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--installation_directory",type=int, default=0, choices=[0, 1],                        help="Tells the program where to install LSDTopoTools.\nOptions are: 0 == home directory, 1 == current directory.\nIf you are in vagrant it will ignore this option and install in the root directory.")
    parser.add_argument("-CRN", "--install_CRN",metavar='True or False',type=bool, default=False, 
                        help="If this is True, installs the CAIRN CRN package.")     
    parser.add_argument("-MChi", "--install_MuddChi2014",metavar='True or False',type=bool, default=False, 
                        help="If this is True, installs programs needed for Mudd et al. 2014 JGR-ES analyses.") 
    args = parser.parse_args()

    # Get the base directory of the installation
    the_base_directory = "~"
    if args.installation_directory == 0:
        the_base_directory = GetBaseDirectory(True)
    elif args.installation_directory == 1:
        the_base_directory = GetBaseDirectory(False) 
        
    # Install or update the default repositories
    LSDTopoToolsDefault(the_base_directory)
        
    # Now go through the optional installations    
    if args.install_CRN:
        CloneMakeCRN_CAIRN(the_base_directory)    
    if args.install_MuddChi2014:
        CloneMakeChiMudd(the_base_directory)          
        
    args = parser.parse_args() 

#=============================================================================
    
    
#=============================================================================    
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print "\n\n======================================================================="
    print "Hello there, I am the going to help you set up LSDTopoTools!"
    print "You will need to tell me what to do."
    print "If you are in vagrant, LSDTopoTools will always be installed in the root directory (\)."
    print "If you are not in vagrant,"
    print "LSDTopoTools will be installed in your home directory if you run this with:"
    print "   python LSDTopoToolsSetup.py -id 0\n"
    print "Or your current directory."
    print "(i.e., the directory from which you called this program)\n"
    print "if you run with this:"
    print "   python LSDTopoToolsSetup.py -id 1\n"
    print "For help type:"
    print "   python LSDTopoToolsSetup.py -h\n"
    print "=======================================================================\n\n "
#=============================================================================



if __name__ == "__main__":
    main(sys.argv[1:])
    
    