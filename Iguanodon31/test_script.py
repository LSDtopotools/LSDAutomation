import Iguanodon31 as Ig

lat = 45.219843
lon = 26.739798
path = '/home/s1675537/PhD/LSDTopoData/knickpoint/test_download/'
Ig.get_SRTM30_from_point(path, 'test_1', lat = lat, lon = lon, get_main_basin = True)

print("done")