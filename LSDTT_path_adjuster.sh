#!/bin/bash
# A bash script used to set paths for the current terminal session

echo "Hello, I am going to ad some LSDTopoTools directories to your path."
echo "IMPORTANT: This DOES NOT modify your profile!!"
echo "It only updates paths for this session."
echo "YOU MUST RUN WITH: source LSDTT_path_adjuster.sh"
echo "Otherwise it will not work in the current session."
echo "You will need to run this script each time you start and LSDTopoTools session."

if [ -d /LSDTopoTools/ ]
  then
    echo "LSDTT is in the root directory."
    basedir="/"
elif [ -d ~/LSDTopoTools/ ]
  then
    echo "LSDTT is in the home directory."
    basedir="~/"
else
  echo "Didn't find LSDTT. I'll assusme it is in the home directory."
  basedir="~/"
fi

echo "The basedir is $basedir"

# Now start looking for the paths
echo "Looking for the analysis driver."
searchpath="LSDTopoTools/Git_projects/LSDTopoTools_AnalysisDriver/Analysis_driver"
fullpath="$basedir$searchpath"
echo "The full search path is $fullpath"
if [ -d "$fullpath/" ]
  then
    echo "This path exists. I will add it to the path for this session."

    if [[ $PATH != *"$fullpath"* ]]
      then
        echo "The searchpath is not in the path. I will add it."
        PATH=$PATH:$fullpath
    else
      echo "The searchpath is in the path."
    fi
else
  echo "This path is not installed."
fi

echo "Looking for the chi tools."
searchpath="LSDTopoTools/Git_projects/LSDTopoTools_ChiMudd2014/driver_functions_MuddChi2014"
fullpath="$basedir$searchpath"
echo "The full search path is $fullpath"
if [ -d "$fullpath/" ]
  then
    echo "This path exists. I will add it to the path for this session."

    if [[ $PATH != *"$fullpath"* ]]
      then
        echo "The searchpath is not in the path. I will add it."
        PATH=$PATH:$fullpath
    else
      echo "The searchpath is in the path."
    fi
else
  echo "This path is not installed."
fi

echo "Looking for the channel extraction tools."
searchpath="LSDTopoTools/Git_projects/LSDTopoTools_ChannelExtraction/driver_functions_ChannelExtraction"
fullpath="$basedir$searchpath"
echo "The full search path is $fullpath"
if [ -d "$fullpath/" ]
  then
    echo "This path exists. I will add it to the path for this session."

    if [[ $PATH != *"$fullpath"* ]]
      then
        echo "The searchpath is not in the path. I will add it."
        PATH=$PATH:$fullpath
    else
      echo "The searchpath is in the path."
    fi
else
  echo "This path is not installed."
fi

echo "Looking for the CAIRN."
searchpath="LSDTopoTools/Git_projects/LSDTopoTools_CRNBasinwide/driver_functions_CRNBasinwide"
fullpath="$basedir$searchpath"
echo "The full search path is $fullpath"
if [ -d "$fullpath/" ]
  then
    echo "This path exists. I will add it to the path for this session."

    if [[ $PATH != *"$fullpath"* ]]
      then
        echo "The searchpath is not in the path. I will add it."
        PATH=$PATH:$fullpath
    else
      echo "The searchpath is in the path."
    fi
else
  echo "This path is not installed."
fi

echo "The path is now:"
echo $PATH
