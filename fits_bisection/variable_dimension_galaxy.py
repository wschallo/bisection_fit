from galaxy import *
from write_data import writeToFile
from base import get_path_to_save_params
from os.path import join

def multiplier_to_string(mult):
    return "{}_percent".format(str(int(mult*100)))

class variable_dimension_galaxy:
    def __init__(self,name,center_row,center_col,semi_major_length,semi_major_angle,isSpiral,wave_band="r"):
        self.original_galaxy = galaxy(name,center_row,center_col,semi_major_length,semi_major_angle,isSpiral,wave_band)
        self.galaxies = {1.0:self.original_galaxy}

        self.name = name
        self.isSpiral = isSpiral

        self.center_col = center_col
        self.center_row = center_row
        self.semi_major_length = semi_major_length
        self.semi_major_angle = semi_major_angle
        #self.isSpiral = isSpiral

        self.wave_band = wave_band

    def save_base_params(self,the_path,the_params):
        to_write_header = []
        to_write_data = []

        the_dict = the_params.get_dict()
        for each_key in sorted(the_dict.keys()):
            to_write_header.append(each_key)
            to_write_data.append(str(the_dict[each_key]))

        writeToFile(" ".join(to_write_header), the_path)
        writeToFile(" ".join(to_write_data), the_path)
        
    def run(self,start_dimension_multiplier=0.5,end_dimension_multiplier=1.0,step=0.25,to_save=True,sub_folder="",params_to_save={}):
        current_mult = start_dimension_multiplier

        while current_mult <= end_dimension_multiplier:
            if current_mult != 1.0:
                current_gal_vd = galaxy(self.name,self.center_row,self.center_col,self.semi_major_length*current_mult,self.semi_major_angle,self.isSpiral,self.wave_band)
                self.galaxies.update({current_mult:current_gal_vd})
            current_mult += step

        if to_save:
            for (each_vd,each_vd_gal) in self.galaxies.items():
                each_vd_gal.run()
                each_vd_gal.save_variable_dimension_data(sub_folder,vd=multiplier_to_string(each_vd))
            if params_to_save != {}:
                the_dir_path = join(get_path_to_save_params(self.name,self.isSpiral),"galaxy_params.txt")
                self.save_base_params(the_dir_path,params_to_save)
                
        

            
