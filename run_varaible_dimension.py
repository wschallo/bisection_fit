from fits_bisection.get_galaxy import *
from fits_bisection.fits import *
from fits_bisection.variable_dimension_galaxy import *
import matplotlib.pyplot as plt
from math import sqrt
from get_galaxies import *
from os.path import exists
from fits_bisection.base import get_fits_path
from get_galaxies import get_galaxies, get_path_to_r_csv
from galaxy_params.read_galaxy_params import read_galaxy_param_for_a_galaxy
from os.path import exists
from galaxy_params.galaxy_params import galaxy_params
from fits_bisection.base import get_fits_path

#BANDS_TO_RUN = ["r","i","g"]
BANDS_TO_RUN = ["i-g"]
MIN_RATIO = 0.5
MAX_RATIO = 1.5
RADIUS_STEPS = 8.0

def run_on_single_galaxy(name,center_row,center_col,semi_major_length,semi_major_angle,is_spiral,start_dimension_multiplier=0.5,end_dimension_multiplier=1.0,step=0.25,save_it=True,sub_folder="",params_to_save={},wave_band="r"):
    the_galaxy = variable_dimension_galaxy(name,center_row,center_col,semi_major_length,semi_major_angle,is_spiral,wave_band)
    the_galaxy.run(start_dimension_multiplier,end_dimension_multiplier,step,save_it,sub_folder,params_to_save)

def run_on_single_galaxy_with_params(galaxy_param,wave_band_to_run="r"):
    if isinstance(galaxy_param,galaxy_params) and galaxy_param.is_valid():
        the_name = galaxy_param.get_name()
        the_row = galaxy_param.get_row()
        the_col = galaxy_param.get_col()
        the_len = galaxy_param.get_radius()
        the_angle = galaxy_param.get_angle()
        the_is_spiral = galaxy_param.get_is_spiral()

        run_on_single_galaxy(the_name, the_row, the_col, the_len, the_angle, the_is_spiral,
                             start_dimension_multiplier=MIN_RATIO, end_dimension_multiplier=MAX_RATIO, step=1.0/RADIUS_STEPS, save_it=True,
                             sub_folder=wave_band_to_run,params_to_save=galaxy_param,wave_band=wave_band_to_run)

def run_on_bath(is_spiral):
    galaxy_names = get_galaxies(is_spiral)

    for each_galaxy in galaxy_names:
        print(each_galaxy)
        cvs_path = get_path_to_r_csv(each_galaxy,is_spiral)

        #skip galaxy if there is no csv file
        if not exists(cvs_path):
            print("no csv")
            continue

        #skip galaxy if we have run it (remove this for later run):
        #check_path = "D:\\Galaxies\\output\\run_2_7_2020\\el\\{}\\galaxy_params.txt".format(each_galaxy)
        #if exists(check_path):
        #continue

        #skip galaxy in name is here:
        if each_galaxy == "1237652934035964198":
            continue

        the_galaxy_param = read_galaxy_param_for_a_galaxy(cvs_path,each_galaxy,is_spiral,wave_band="r")

        for each_band in BANDS_TO_RUN:
            try:
                #skip band if fits doesn't exist
                if not exists(get_fits_path(each_galaxy,is_spiral,band=each_band)):
                    print("no path")
                    print(get_fits_path(each_galaxy,is_spiral,band=each_band))
                    continue
                run_on_single_galaxy_with_params(the_galaxy_param, wave_band_to_run=each_band)
            except ZeroDivisionError as e:
                print("divide by zero error: {} band {}".format(each_galaxy,each_band))

if __name__ == "__main__":
    run_on_bath(False) #run on spiral galaxies



