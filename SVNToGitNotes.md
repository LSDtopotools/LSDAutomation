Notes on moving SVN tracked files to the git repository
============================================================

[Simon M. Mudd](http://simon-m-mudd.github.io/), 26-08-2015

Overview and Rationale
--------------------------

These notes are for the benefit of developers of the [LSDTopoTools](http://lsdtopotools.github.io/) software package. 

The development of our tools occurs within a [subversion](https://subversion.apache.org/) repository at the [University of Edinburgh](https://www.wiki.ed.ac.uk/display/ecdfwiki/Version+Control+Service). 
Subversion is [hated by prominent programmers](https://www.youtube.com/watch?v=idLyobOhtO4), but at the moment we are not quite ready to have totally open source development and [bitbucket](https://bitbucket.org/) only allows 6 developers if you want a free repository. Hence, SVN. 

However, once our code is ready for distribution, our philosophy is to make it open source. 
In the past we have posted the code on [CSDMS](http://csdms.colorado.edu/wiki/Main_Page), but I (SMM) have decided that I wsant a bit more control over the subversioning so have put it in our own [github](https://github.com/LSDtopotools) repositories. 

Transfer of drivers from SVN to GitHub
---------------------------------------

So, if you are an LSDTopoTools developer, how do you move cade from the SVN repository to github?

At the risk of being pedantic, to review the directory structure of LSDTopoTools, we have the objects in a trunk folder. 
This trunk folder then contains folders with the driver functions. These driver functions manage the objects and perform analyses. 
The idea is that if you distribute a DEM and the code to another person, that person can reporduce your analysis exactly. 



Copying files using SVNToGitAutomator.py
----------------------------------------------

The `.make` files in the driver function folders contain all the informations about files needed to compile, so these are used by a python script to copy files from subversioned folders into a git folder. 


The script for doing this is called SVNToGitAutomator.py. 

You need to give this script 3 strings. You can find the place to put these strings at the bottom of the script. They are:

1. `ObjectsDirectory`: The directory path of the objects
2. `DriverDirectory`: The path to the driver functions. *THIS IS NOT THE FULL PATH*, rather it is the extra directory above the objects path!
3. `TargetDirectory`: This is the path where you will put (or have) your github repository.

Here are some examples. In Windows:

```ObjectsDirectory = 'T:\devel_projects\LSDTopoTools\trunk'
DriverDirectory = 'driver_functions_MuddChi2014'
TargetDirectory = 'T:\Git_projects\LSDTopoTools_ChiMudd2014'```

In Linux:

```ObjectsDirectory = '/home/smudd/SMMDataStore/devel_projects/LSDTopoTools/trunk'
DriverDirectory = 'driver_functions_MuddChi2014'
TargetDirectory = '/home/smudd/SMMDataStore/Git_projects/LSDTopoTools_ChiMudd2014'```

Once the script runs, you should have all the files needed to compile the code in the `TargetDirectory`. 


Adding to the git repo
-------------------------------------------------

If the copied folder is not a git repo, you need to do the following:

Navigate to the `TargetDirectory` folder.

It is probably a good idea to add a `readme.md` file to this folder. 

Then type `git init`.

Then `git add *`. It is important you do this before you compile or else all the compiled binary files will be added to the git repository.

Next go to github and make a new repository. 

Then go back to the `TargetDirectroy` folder and add an `origin` path using git. 

For example:

```git remote add origin https://github.com/LSDtopotools/LSDTopoTools_ChiMudd2014.git

git push -u origin master```