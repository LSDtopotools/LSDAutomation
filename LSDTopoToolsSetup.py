# This is a python script for setting up LSDTopoTools on your computer
# It creates a directory structure, clones the appropriate repositories
# And makes the programs. 
# @author Simon M Mudd
# @date 16-10-2016

import os
import subprocess

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

# This function clones both the test data and the workshop data from github
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
        print "I am calling a subprocess with the following entries:"
        print git
        print git_worktree
        print git_dir      
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])
    
    print "/n/nI am going to check the workshop data files."
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
        

def LSDTopoToolsSetUp(WantHomeDirectory = True):
    
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
    print "Note: if you are in vagrant the base directories should already exist."
    BuildDirectoryTree(the_base_directory)
            
    print "\n\nI've built the directories. I will now clone the test data."
    CloneData(the_base_directory)    

        
    
    
if __name__ == "__main__":
    LSDTopoToolsSetUp() 