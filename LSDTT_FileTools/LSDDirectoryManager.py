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

# This function clones both the test data and the workshop data from github
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
    
    print "I am going to check the workshop data files."
    file = "./LSDTopoTools/Topographic_projects/LSDTT_workshop_data/WA.bil"
    if not os.path.isfile(file):
        print "There is no test data. Cloning in a subprocess"
        repo_address = "https://github.com/LSDtopotools/LSDTT_workshop_data.git"
        target_directory = "./LSDTopoTools/Topographic_projects/LSDTT_workshop_data"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        print "I wonder where I am now"
        this_cwd = os.getcwd()
        print "I am at: " + this_cwd
        
        git_worktree = "--work-tree="+this_cwd+"/LSDTopoTools/Topographic_projects/LSDTT_workshop_data/"
        git_dir = "--git-dir="+this_cwd+"/LSDTopoTools/Topographic_projects/LSDTT_workshop_data/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])   
    
# This function clones both the test data and the workshop data from github
def CloneMakeAnalysisDriver():
    git = "git"
    clone = "clone"
    pull = "pull"
    origin = "origin"
    master = "master"
    
    print "I am going to check if the repository exists."
    file = "./LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/LSDRaster.cpp"
    if not os.path.isfile(file):
        print "I don't see the LSDraster.cpp. I am going to try cloning the LSDTopoTools_AnalysisDriver repo."
        repo_address = "https://github.com/LSDtopotools/LSDTopoTools_AnalysisDriver.git"
        target_directory = "./LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver"
        subprocess.call([git,clone,repo_address,target_directory])
    else:
        print "The repo with " + file+ " exists. I am updating."
        print "I wonder where I am now"
        this_cwd = os.getcwd()
        print "I am at: " + this_cwd
        
        git_worktree = "--work-tree="+this_cwd+"/LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/"
        git_dir = "--git-dir="+this_cwd+"/LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/.git"
        subprocess.call([git,git_worktree,git_dir,pull,origin,master])    
        
    print "I should have the AnalysisDriver. Now I am going to make the program for you."
    makef = "make -f"
    LSDTTpath = "/LSDTopoTools/Git_projects/"
    target = this_cwd+LSDTTpath+"/LSDTopoTools_AnalysisDriver/Analysis_driver/Drive_analysis_from_paramfile.make"
    subprocess.call([makef,target])  