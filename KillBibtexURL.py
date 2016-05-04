# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 09:42:40 2016

@author: smudd
"""

import os

# this deletes all the @URL fields from a bibtex file
def KillBibtexURL(filename, newfilename):
    
    
    if os.access(filename,os.F_OK):
        this_file = open(filename, 'r')
        lines = this_file.readlines()
        this_file.close()
        
        new_file = open(newfilename,'w')
        
        new_lines = []
        
        for line in lines:
            if("Url" not in line and "url" not in line):
                new_lines.append(line)
                new_file.write(line)
        new_file.close()
        
        print new_lines
    else:
        print "Hey buddy, I couldn't find the .bib file. Are you sure you have the right filename?"
                
if __name__ == "__main__":
    
    filename = "T://Papers_LaTeX//length_scale_paper//GR_version2.bib"
    newfilename = "T://Papers_LaTeX//length_scale_paper//GR_version3.bib"
    KillBibtexURL(filename, newfilename)