from os import getcwd, makedirs
from os.path import join, isdir,exists
from math import sqrt, radians, tan, ceil, floor, degrees
from numpy import rot90
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

CURRENT_DIRECTORY = getcwd()
DATA_SOURCE_PATH = join(CURRENT_DIRECTORY,"data_source")
#FITS_FILE_DIRECTORY = "C:\\Users\\wills\\Desktop\\sparcfire\\fitsFileAnalysis\\fits" #(previous)
FITS_FILE_DIRECTORY = "D:\\Galaxies\\galaxies_input" #changed for i-g
FITS_FILE_DIRECTORY_I_G = "D:\\Galaxies\\i_minus_g"
#BASE_DIR = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\output" #(previous)
BASE_DIR = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\output_i-g" #changed for i-g

BASE_VD_SAD_DIR = "D:\\Galaxies\\output\\run_2_7_2020" #changed

def get_params_path(isSpiral):
    file_name = "{}_params.txt".format("sp" if isSpiral else "el")
    return join(DATA_SOURCE_PATH,file_name)

#below changed for i-g, used to be 'r'
def get_fits_path(name,isSpiral,band="r"):
    sub_directory = "sp" if isSpiral else "el"
    fits_file_name = "{}_{}.fits".format(name,band)
    #print(join(FITS_FILE_DIRECTORY,sub_directory,fits_file_name))
    #return join(FITS_FILE_DIRECTORY,sub_directory,fits_file_name) #(previous)
    #return join(FITS_FILE_DIRECTORY,fits_file_name) #changed for i-g
    if band == "i-g":
        return join(FITS_FILE_DIRECTORY_I_G,fits_file_name)
    else:
        return join(FITS_FILE_DIRECTORY, sub_directory, name, fits_file_name)


def get_path_to_save_galaxy_info(name,isSpiral,sub_dir,make_dir=True):
    sp_string = "sp" if isSpiral else "el"
    full_path = join(CURRENT_DIRECTORY,sub_dir,sp_string,name)

    if make_dir and not exists(full_path):
        makedirs(full_path)

    return full_path


def get_partial_path_to_save_galaxy_info_variable_dimension(name,isSpiral,sub_dir):
    sp_string = "sp" if isSpiral else "el"
    return join(BASE_VD_SAD_DIR,sp_string,name)

def get_path_to_save_galaxy_info_variable_dimension(name,isSpiral,sub_dir,vd="100_percent",make_dir=True):
    sp_string = "sp" if isSpiral else "el"
    #full_path = join(CURRENT_DIRECTORY,sub_dir,sp_string,name)
    #full_path = join(CURRENT_DIRECTORY,sub_dir,sp_string,name,vd) #(previous)
    full_path = join(BASE_VD_SAD_DIR,sp_string,name,sub_dir,vd)#changed for i-g

    if make_dir and not exists(full_path):
        makedirs(full_path)

    return full_path

def get_path_to_save_params(name,isSpiral,make_dir=True):
    sp_string = "sp" if isSpiral else "el"
    full_path = join(BASE_VD_SAD_DIR, sp_string, name)

    if make_dir and not exists(full_path):
        makedirs(full_path)

    return full_path
