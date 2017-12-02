## Prepare_drivers_mn_collinearity.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function takes a single driver file and then spawns
## many driver files with different sigma values for testing the sensitivty
## to sigma. It puts each one in a different sub-directory.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 03/07/17
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def test_sigma_sensitivity(DataDirectory, DriverFileName, start_sigma=10, n_sigma=10, d_sigma=10):
    """
    This function generates a series of drivers to test the
    sensitivity of the MLE collinearity to sigma. Puts each
    new driver in a different sub-directory within the original
    directory.

    Args:
        DataDirectory: the data directory
        DriverFileName: name of the driver file
        start_sigma: the starting sigma value (default = 10)
        n_sigma: the number of sigma values to test (default = 10)
        d_sigma: the step to change sigma values (default = 10)

    Author: FJC
    """
    import os
    import numpy as np

    # get the name of the driver file
    FileName = DataDirectory+DriverFileName
    print "FileName is"+FileName

    # read in the lines
    f = open(FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    f.close()

    # declare strings for searching
    write_str = "write path"
    sigma_str = "collinearity_MLE_sigma"

    # get a list of sigma values
    end_sigma = start_sigma+(n_sigma*d_sigma)
    sigmas = np.arange(start_sigma,end_sigma,step=d_sigma)

    # for each value of sigma, generate a new sub-directory
    for sigma in sigmas:
        # generate a new sub-directory
        sub_dir = DataDirectory+'Chi_analysis_sigma_'+str(sigma)+"/"
        print sub_dir
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        new_lines = []
        # change the lines for the value of sigma
        for line in lines:
            # need to find the lines with the write path, and sigma
            if write_str in line:
                line = write_str+ ": "+sub_dir+"\n"
            if sigma_str in line:
                line = sigma_str+ ": "+str(sigma)+"\n"
            new_lines.append(line)

        print new_lines
        f = open(sub_dir+DriverFileName, 'w')
        f.writelines(new_lines)
        f.close()


if __name__ == "__main__":
    DataDirectory = '/home/s0923330/LSDTopoData/movern_analysis/kentucky_srtm/'
    DriverFileName = 'Kentucky_DEM.driver'
    start_sigma = 200
    n_sigma = 9
    d_sigma = 100
    test_sigma_sensitivity(DataDirectory, DriverFileName, start_sigma, n_sigma, d_sigma)
