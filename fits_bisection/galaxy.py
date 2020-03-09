from base import *
from fits import *
from area_matrix import *
from support import *
from write_data import *
from data import *
from matrix import fits_matrix, rotate

DELTA_ANGLE = 10


class galaxy:
    def __init__(self,name,center_row,center_col,semi_major_length,semi_major_angle,isSpiral,wave_band="r"):
        self.name = name
        self.center_row = center_row
        self.center_col = center_col
        self.semi_major_axis_length = semi_major_length
        self.semi_major_angle = semi_major_angle
        self.isSpiral = isSpiral
        self.wave_band = wave_band

        self.fits_path = ""

        self.original_data = np.zeros((1,1))
        self.area_data = np.zeros((1,1))
        self.cropped_data = np.zeros((1,1))
        
        self.data_points = 0
        self.area_data_points = 0 # to test theory
        self.normalized_data_point = 0 # to test theory
        
        self.has_loaded_data = False
        self.has_area_data = False
        self.has_crop_data = False
        self.has_data_point = False
        
        self.cx = -1
        self.cy = -1
        self.shape = (-1,-1)

    def get_original_fits(self):
        self.fits_path = get_fits_path(self.name,self.isSpiral,self.wave_band)
        self.original_data = readFits(self.fits_path)
        self.shape = self.original_data.shape
        (self.cx,self.cy) = cxCyFromCenter(self.center_row,self.center_col,self.shape)
        self.has_loaded_data = True

    def create_area_matrix(self):
        if self.has_loaded_data:
            self.area_data = create_area_matrix(self.cx,self.cy,self.semi_major_axis_length,self.shape)
            self.has_area_data = True

    def crop_data(self):
        if self.has_area_data and self.has_loaded_data:
            self.cropped_data = self.original_data * self.area_data
            self.has_crop_data = True

    def load_original_data_and_crop(self):
        self.get_original_fits()
        self.create_area_matrix()    
        self.crop_data()

    def rotate_cropped_data(self):
        if self.has_crop_data:
            self.data_points = rotate(self.cropped_data,self.cx,self.cy,0,360,DELTA_ANGLE,True,self.name)
            self.has_data_point = True

    def rotate_area_data(self):
        if self.has_area_data:
            self.area_data_points = rotate(self.area_data,self.cx,self.cy,0,360,DELTA_ANGLE,True,self.name)
            

    def fit_data_and_plot(self,showGraph=False):
        if self.has_data_point:
            self.data_points.fitIt()

            nd = noramlize_data_points(self.data_points,self.area_data_points)
            nd.fitIt()
            self.normalized_data_point = nd
            #nd.plot()
            self.data_points = nd #for test (normalize by area)

            if showGraph:
                fitDeg = degrees(self.data_points.fit_phase)
                ActualDeg = degrees(self.semi_major_angle)
                print("{}: actual {}, fit {}".format(fitDeg-ActualDeg,ActualDeg,fitDeg))
                nd.plot()
                #self.data_points.plot()
                #self.area_data_points.plot()

    def run(self):
        self.load_original_data_and_crop()
        self.rotate_cropped_data()
        self.rotate_area_data() #to test idea
        self.fit_data_and_plot(False)

    def save_data(self,sub_dir):
        dir_to_save_in = get_path_to_save_galaxy_info(self.name,self.isSpiral,sub_dir)

        #copy input:
        fits_path = join(dir_to_save_in,"input_a.fits")
        writeFits(self.original_data,fits_path)

        #save area fits:
        fits_area_path = join(dir_to_save_in,"area_b.fits")
        writeFits(self.area_data,fits_area_path)

        #save cropped fits:
        fits_crop_path = join(dir_to_save_in,"cropped_c.fits")
        writeFits(self.cropped_data,fits_crop_path)

        #save cropping params:
        crop_params_path = join(dir_to_save_in,"crop_params.txt")
        heading = ["name","isSpiral","semi_major_len","semi_major_rad","center_row","center_col","number_of_rows","number_of_cols","cx","cy"]
        data = [self.name,str(self.isSpiral),str(self.semi_major_axis_length),str(self.semi_major_angle),str(self.center_row),str(self.center_col),str(self.shape[0]),str(self.shape[1]),str(self.cx),str(self.cy)]
        writeToFile(" ".join(heading), crop_params_path)
        writeToFile(" ".join(data), crop_params_path)
        
        #save cropping data points:
        data_points_path = join(dir_to_save_in,"rotate_data.txt")
        writeInfo(self.data_points,True,data_points_path)

        #save graph of comparison:
        fits_crop_path = join(dir_to_save_in,"graph_d.png")
        self.data_points.plot(fits_crop_path,str(degrees(self.semi_major_angle)))
        
        #save angle coparison:
        angle_comp_path = join(dir_to_save_in,"angle_compare.txt")
        heading = ["name","isSpiral","semi_major_degrees","fit_degrees","delta_angle","fit_amp"]
        data = [self.name,str(self.isSpiral),str(degrees(self.semi_major_angle)),str(degrees(self.data_points.fit_phase)),str(degrees(self.semi_major_angle)-degrees(self.data_points.fit_phase)),str(self.data_points.fit_amp)]
        writeToFile(" ".join(heading), angle_comp_path)
        writeToFile(" ".join(data), angle_comp_path)

    def save_variable_dimension_data(self,sub_dir,vd="100_percent"):
        dir_to_save_in = get_path_to_save_galaxy_info_variable_dimension(self.name,self.isSpiral,sub_dir,vd)
        
        #copy input:
        fits_path = join(dir_to_save_in,"input_a.fits")
        writeFits(self.original_data,fits_path)

        #save area fits:
        fits_area_path = join(dir_to_save_in,"area_b.fits")
        writeFits(self.area_data,fits_area_path)

        #save cropped fits:
        fits_crop_path = join(dir_to_save_in,"cropped_c.fits")
        writeFits(self.cropped_data,fits_crop_path)

        #save cropping params:
        crop_params_path = join(dir_to_save_in,"crop_params.txt")
        heading = ["name","isSpiral","semi_major_len","semi_major_rad","center_row","center_col","number_of_rows","number_of_cols","cx","cy"]
        data = [self.name,str(self.isSpiral),str(self.semi_major_axis_length),str(self.semi_major_angle),str(self.center_row),str(self.center_col),str(self.shape[0]),str(self.shape[1]),str(self.cx),str(self.cy)]
        writeToFile(" ".join(heading), crop_params_path)
        writeToFile(" ".join(data), crop_params_path)
        
        #save cropping data points:
        data_points_path = join(dir_to_save_in,"rotate_data.txt")
        writeInfo(self.data_points,True,data_points_path)

        #save graph of comparison:
        fits_crop_path = join(dir_to_save_in,"graph_d.png")
        self.data_points.plot(fits_crop_path,str(degrees(self.semi_major_angle)))
        
        #save angle coparison:
        angle_comp_path = join(dir_to_save_in,"angle_compare.txt")
        heading = ["name","isSpiral","semi_major_degrees","fit_degrees","delta_angle","fit_amp"]
        data = [self.name,str(self.isSpiral),str(degrees(self.semi_major_angle)),str(degrees(self.data_points.fit_phase)),str(degrees(self.semi_major_angle)-degrees(self.data_points.fit_phase)),str(self.data_points.fit_amp)]
        writeToFile(" ".join(heading), angle_comp_path)
        writeToFile(" ".join(data), angle_comp_path)
