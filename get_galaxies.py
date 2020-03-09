import os
import csv

PATH_FOR_SP = "D:\\Galaxies\\galaxies_input\\sp"
PATH_FOR_EL = "D:\\Galaxies\\galaxies_input\\el"

def get_galaxies(is_spiral):
    d = PATH_FOR_SP if is_spiral else PATH_FOR_EL

    return [o for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]

def get_path_to_r_csv(name,is_spiral):
    d = PATH_FOR_SP if is_spiral else PATH_FOR_EL
    file_name = "{}_r.csv".format(name)
    return os.path.join(d,name,file_name)
