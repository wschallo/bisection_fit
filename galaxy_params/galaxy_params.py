from galaxy_params_constants import NAME_KEY, IS_SPIRAL_KEY, ROW_KEY, COL_KEY, COMP_AXIS_RATIO_KEY, COMP_ANGLE_KEY, BAD_BUGLE_FIT_KEY, BULGE_AXIS_RATIO_KEY, BULGE_MAJ_AXIS_LEN_KEY, BULGE_ANGLE_KEY, DISK_ANGLE_KEY, DISK_MAJ_AXIS_LEN, DISK_AXIS_RATIO_KEY, INPUT_RADIUS_KEY, WAVE_BAND_KEY

class galaxy_params:
    def __init__(self):
        self.name = ""
        self.is_spiral = False
        self.row = -1.0
        self.col = -1.0
        self.wave_band = ""

        self.radius = -1.0
        self.angle = -1.0
        self.axis_ratio = -1.0

        self.bad_bulge_fit = False
        self.bulge_axis_ratio = -1.0
        self.bulge_maj_axis_len = -1.0
        self.bulge_angle = -1.0

        self.disk_axis_ratio = -1.0
        self.disk_maj_axis_len = -1.0
        self.disk_angle = -1.0

    def is_valid(self):
        valid_name = len(self.get_name()) > 0
        valid_row = self.get_row() > 0
        valid_col = self.get_col() > 0
        valid_radius = self.get_radius() > 0

        return valid_name and valid_row and valid_col and valid_radius

    def set_name(self,the_name):
        if isinstance(the_name,str) and len(the_name) > 0:
            self.name = the_name

    def set_is_spiral(self,is_it_spiral):
        if isinstance(is_it_spiral,bool):
            self.is_spiral = is_it_spiral

    def set_row(self,the_row):
        if isinstance(the_row,float) and the_row > 0.0:
            self.row = the_row

    def set_col(self,the_col):
        if isinstance(the_col,float) and the_col > 0.0:
            self.col = the_col

    def set_radius(self,the_radius):
        if isinstance(the_radius,float) and the_radius > 0.0:
            self.radius = the_radius

    def set_angle(self,the_angle):
        if isinstance(the_angle,float):
            self.angle = the_angle

    def set_axis_ratio(self,the_axis_ratio):
        if isinstance(the_axis_ratio,float):
            self.axis_ratio = the_axis_ratio

    def set_bad_bulge_fit(self,the_fit):
        if isinstance(the_fit,bool):
            self.bad_bulge_fit = the_fit

    def set_bulge_axis_ratio(self,the_ratio):
        if isinstance(the_ratio,float):
            self.bulge_axis_ratio = the_ratio

    def set_bulge_axis_len(self,the_len):
        if isinstance(the_len,float) and the_len > 0.0:
            self.bulge_maj_axis_len = the_len

    def set_bulge_angle(self,the_angle):
        if isinstance(the_angle,float):
            self.bulge_angle = the_angle

    def set_disk_axis_ratio(self,the_ratio):
        if isinstance(the_ratio,float):
            self.disk_axis_ratio = the_ratio

    def set_disk_axis_len(self,the_len):
        if isinstance(the_len,float) and the_len > 0.0:
            self.disk_maj_axis_len = the_len

    def set_disk_angle(self,the_angle):
        if isinstance(the_angle,float):
            self.disk_angle = the_angle

    def set_wave_band(self,the_wave_band):
        if isinstance(the_wave_band, str):
            self.wave_band = the_wave_band

    def get_name(self):
        return self.name

    def get_is_spiral(self):
        return self.is_spiral

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_radius(self):
        return self.radius

    def get_angle(self):
        return self.angle

    def get_ratio(self):
        return self.axis_ratio

    def get_bad_bulge_fit(self):
        return self.bad_bulge_fit

    def get_bulge_axis_ratio(self):
        return self.bulge_axis_ratio

    def get_bulge_maj_axis_len(self):
        return self.bulge_maj_axis_len

    def get_bulge_angle(self):
        return self.bulge_angle

    def get_disk_axis_ratio(self):
        return self.disk_axis_ratio

    def get_disk_axis_len(self):
        return self.disk_maj_axis_len

    def get_disk_angle(self):
        return self.disk_angle

    def get_wave_band(self):
        return self.wave_band

    def set_the_input_params(self):
        # use bulge_major_axis_len as input radius:
        radius_to_use = self.get_bulge_maj_axis_len()
        self.set_radius(radius_to_use)

        # use disk_ratio as comp. angle:
        ratio_to_use = self.get_disk_axis_ratio()
        self.set_axis_ratio(ratio_to_use)

        # use disk_angle as comp. angle:
        angle_to_use = self.get_disk_angle()
        self.set_angle(angle_to_use)

    def get_dict(self):
        the_dict = dict()

        the_dict[NAME_KEY] = self.get_name()
        the_dict[IS_SPIRAL_KEY] = self.get_is_spiral()
        the_dict[ROW_KEY] = self.get_row()
        the_dict[COL_KEY] = self.get_col()

        the_dict[WAVE_BAND_KEY] = self.get_wave_band()

        the_dict[INPUT_RADIUS_KEY] = self.get_radius()
        the_dict[COMP_ANGLE_KEY] = self.get_angle()
        the_dict[COMP_AXIS_RATIO_KEY] = self.get_ratio()

        the_dict[BAD_BUGLE_FIT_KEY] = self.get_bad_bulge_fit()
        the_dict[BULGE_AXIS_RATIO_KEY] = self.get_bulge_axis_ratio()
        the_dict[BULGE_MAJ_AXIS_LEN_KEY] = self.get_bulge_maj_axis_len()
        the_dict[BULGE_ANGLE_KEY] = self.get_bulge_angle()

        the_dict[DISK_AXIS_RATIO_KEY] = self.get_disk_axis_ratio()
        the_dict[DISK_MAJ_AXIS_LEN] = self.get_disk_axis_len()
        the_dict[DISK_ANGLE_KEY] = self.get_disk_angle()
        return the_dict


    def load_dict(self,the_dict):
        for the_key in the_dict:
            the_value = the_dict[the_key]

            if the_key == NAME_KEY:
                self.set_name(the_value)
            elif the_key == IS_SPIRAL_KEY:
                self.set_is_spiral(the_value)
            elif the_key == ROW_KEY:
                self.set_row(the_value)
            elif the_key == COL_KEY:
                self.set_col(the_value)
            elif the_key == WAVE_BAND_KEY:
                self.set_wave_band(the_value)
            elif the_key == COMP_ANGLE_KEY:
                self.set_angle(the_value)
            elif the_key == COMP_AXIS_RATIO_KEY:
                self.set_axis_ratio(the_value)
            elif the_key == INPUT_RADIUS_KEY:
                self.set_radius(the_value)
            elif the_key == BAD_BUGLE_FIT_KEY:
                self.set_bad_bulge_fit(the_value)
            elif the_key == BULGE_AXIS_RATIO_KEY:
                self.set_bulge_axis_ratio(the_value)
            elif the_key == BULGE_MAJ_AXIS_LEN_KEY:
                self.set_bulge_axis_len(the_value)
            elif the_key == BULGE_ANGLE_KEY:
                self.set_bulge_angle(the_value)
            elif the_key == DISK_AXIS_RATIO_KEY:
                self.set_disk_axis_ratio(the_value)
            elif the_key == DISK_MAJ_AXIS_LEN:
                self.set_disk_axis_len(the_value)
            elif the_key == DISK_ANGLE_KEY:
                self.set_disk_angle(the_value)
        

        
