# This is a collection of tools for automating directory creation and dowloading the LSDTT packages
import os
import LSDOSystemTools as LSDost
import subprocess

def BuildDirectoryTree():
    
    # first find the LSDTopoTools directory
    path = "./LSDTopoTools/"
    if not os.access(path,os.F_OK):
        print "Making path: "
        os.mkdir(path)
        print path
    else:
        print "Path: " +path+" already exists."   
        
    # first find the Git_projects directory
    path = "./LSDTopoTools/Git_projects"
    if not os.access(path,os.F_OK):
        print "Making path: "
        os.mkdir(path)
        print path
    else:
        print "Path: " +path+" already exists."          
        
    # first find the Git_projects directory
    path = "./LSDTopoTools/Topographic_projects"
    if not os.access(path,os.F_OK):
        print "Making path: "
        os.mkdir(path)
        print path
    else:
        print "Path: " +path+" already exists."         
        
def CloneData():
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
    
    print "I am going to check the test data files."
    file = "./LSDTopoTools/Topographic_projects/Test_data/Mandakini.bil"
    if not os.path.isfile(file):
        print "There is no test data. Cloning in a subprocess"
        repo_address = "https://github.com/LSDtopotools/LSDTT_vagrant_datasets.git"
        target_directory = "./LSDTopoTools/Topographic_projects/Test_data"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        print "I wonder where I am now"
        this_cwd = os.getcwd()
        print "I am at: " + this_cwd
        
        git_worktree = "--work-tree="+this_cwd+"/LSDTopoTools/Topographic_projects/Test_data/"
        git_dir = "--git-dir="+this_cwd+"/LSDTopoTools/Topographic_projects/Test_data/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])
        
    
    
    
    
    