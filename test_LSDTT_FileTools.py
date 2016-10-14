# Testing of the file tools package
# @author Simon M Mudd
# 

import LSDTT_FileTools as LSDFT

def TestFileTools():
    print "I am building some directories now"
    LSDFT.BuildDirectoryTree()
    LSDFT.CloneData()
    
if __name__ == "__main__":
    TestFileTools() 
