from base import *
from data import *
from support import *

class fits_matrix:
    def __init__(self,fits_matrix,cx,cy):
        self.data = fits_matrix
        
        self.cx = cx
        self.cy = cy
        self.number_of_rows =self.data.shape[0]
        self.number_of_cols =self.data.shape[1]
        
        self.total_col_sum = sum(self.data)
        self.total = sum(self.total_col_sum)
        self.col_sum_above = self._construct_col_sum_above()
        self.col_sum_below = self._construct_col_sum_below()

        self.col_area_above = self._construct_area_above()
        self.col_area_below = self._construct_area_below()

    def _construct_area_above(self):
        col_area_above = []
        last_row = np.zeros(self.number_of_cols)
        
        for row_ind in range(self.number_of_rows):
            col_area_above.append(last_row)
            last_row = last_row + np.ones(self.number_of_cols)
            
        return np.array(col_area_above)

    def _construct_area_below(self):
        col_area_below = []
        last_row = np.zeros(self.number_of_cols)
        
        for row_ind in reversed(range(self.number_of_rows)):
            col_area_below.append(last_row)
            last_row = last_row + np.ones(self.number_of_cols)
            
        return np.array(list(reversed(col_area_below)))

    def _construct_col_sum_above(self):
        col_sum_above = []
        last_row = np.zeros(self.number_of_cols)
        
        for row_ind in range(self.number_of_rows):
            col_sum_above.append(last_row)
            last_row = last_row + self.data[row_ind,:]
            
        return np.array(col_sum_above)

    def _construct_col_sum_below(self):
        col_sum_below = []
        last_row = np.zeros(self.number_of_cols)
        
        for row_ind in reversed(range(self.number_of_rows)):
            col_sum_below.append(last_row)
            last_row = last_row + self.data[row_ind,:]
            
        return np.array(list(reversed(col_sum_below)))

    def _convert_cord_to_row_col(self,x,y,roundDown = True):
        row = self.number_of_rows - floor(y) - 1
        col = floor(x)

        if row < 0 or row >= self.number_of_rows:
            print("error converting",row,x,y)

        if roundDown:
            return (int(floor(row)),int(floor(col)))
        else:
            return (row,col)

    def get_tile_at_cord(self,x,y):
        (row,col) = self._convert_cord_to_row_col(x,y)
        return self.data[row][col]

    def get_sum_below_cord(self,x,y):
        (row,col) = self._convert_cord_to_row_col(x,y)
        return self.col_sum_below[row][col]
    
    def get_sum_above_cord(self,x,y):
        (row,col) = self._convert_cord_to_row_col(x,y)
        return self.col_sum_above[row][col]
    
    def get_area_below_cord(self,x,y):
        (row,col) = self._convert_cord_to_row_col(x,y)
        return self.col_area_below[row][col]
    
    def get_area_above_cord(self,x,y):
        (row,col) = self._convert_cord_to_row_col(x,y)
        return self.col_area_above[row][col]
        
    def is_cartessian_y_val_below_matrix(self,y_val):
        return y_val < 0

    def is_cartessian_y_val_above_matrix(self,y_val):
        return y_val >= self.number_of_rows

    def is_cartessian_y_val_in_matrix(self,y_val):
        return not (self.is_cartessian_y_val_below_matrix(y_val) or self.is_cartessian_y_val_above_matrix(y_val))


    def _split_at_angle_between_0_and_45(self,degree):
        y = get_equation_of_line_with_posiitve_slope(degree, self.cx, self.cy)
        
        xs = list(range(self.number_of_cols + 1)) #adding 1 to make zip work correctly
        ys = list(map(lambda x: y(x), xs))

        pos_sum = 0
        neg_sum = 0

        total_pos_area = 0
        total_neg_area = 0

        for(left_x,right_x,left_y,right_y) in zip(xs,xs[1:],ys,ys[1:]):
            if self.is_cartessian_y_val_below_matrix(right_y):
                #entire column is above
                
                pos_sum += self.total_col_sum[left_x]
                total_pos_area += self.number_of_rows
                
            elif self.is_cartessian_y_val_above_matrix(left_y):
                #entire column is below
                
                neg_sum += self.total_col_sum[left_x]
                total_neg_area += self.number_of_rows

            
            elif self.is_cartessian_y_val_below_matrix(left_y) and self.is_cartessian_y_val_in_matrix(right_y):
                #crosses bottom (left_y < 0 and right_y > 0)

                int_between = get_integers_between_vals(0,right_y)
                intersects_bottom_at_x_val = secant_method(left_x,right_x,y,10^-6,10)
                
                if len(int_between) == 0:
                    avg_val = (0 + right_y)/2
                    neg_sum += self.get_sum_below_cord(left_x,avg_val)
                    pos_sum += self.get_sum_above_cord(left_x,avg_val)
                    
                    total_neg_area += self.get_area_below_cord(left_x,avg_val)
                    total_pos_area += self.get_area_above_cord(left_x,avg_val)

                    base = floor(avg_val)
                    a = intersects_bottom_at_x_val - left_x
                    b = 1
                    c = right_y - base
                    d = 0

                    (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                    weight_of_tile = self.get_tile_at_cord(left_x,avg_val)
                    pos_sum += (area_above * weight_of_tile)
                    neg_sum += (area_below * weight_of_tile)

                    total_neg_area += area_below
                    total_pos_area += area_above
                    
                else:
                    avg_val_top = (int_between[-1] + right_y)/2
                    avg_val_bottom = (int_between[0] + 0)/2
                    neg_sum += self.get_sum_below_cord(left_x,avg_val_bottom)
                    pos_sum += self.get_sum_above_cord(left_x,avg_val_top)

                    total_neg_area += self.get_area_below_cord(left_x,avg_val_bottom)
                    total_pos_area += self.get_area_above_cord(left_x,avg_val_top)

                    x_vals = [intersects_bottom_at_x_val]
                    y_vals = [0]
                    for each_int in int_between:
                        intersects_int_at = secant_method(0,right_x,lambda x: (y(x) - (each_int)),10^-6,10)
                        x_vals.append(intersects_int_at)
                        y_vals.append(each_int)
                    x_vals.append(right_x)
                    y_vals.append(right_y)

                    for (sub_division_left_x,sub_division_left_y,sub_division_right_x, sub_division_right_y) in zip(x_vals,y_vals,x_vals[1:],y_vals[1:]):
                        sub_divison_avg = (sub_division_left_y + sub_division_right_y)/2

                        base = floor(sub_divison_avg)

                        a = sub_division_left_x - left_x
                        b = sub_division_right_x - left_x
                        c = sub_division_right_y - base
                        d = sub_division_left_y - base
                        
                        (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                        weight_of_tile = self.get_tile_at_cord(left_x,base)
                        pos_sum += (area_above * weight_of_tile)
                        neg_sum += (area_below * weight_of_tile)

                        total_neg_area += area_below
                        total_pos_area += area_above
                
            elif self.is_cartessian_y_val_above_matrix(right_y) and self.is_cartessian_y_val_in_matrix(left_y):
                #crosses top (left_y < self.number_rows and right_y >= self.number_of_rows)

                int_between = get_integers_between_vals(left_y,self.number_of_rows)
                intersects_top_at_x_val = secant_method(left_x,right_x,lambda x: (y(x) - (self.number_of_rows)),10^-6,10)
                
                if len(int_between) == 0:
                    avg_val = (left_y + self.number_of_rows)/2
                    neg_sum += self.get_sum_below_cord(left_x,avg_val)
                    pos_sum += self.get_sum_above_cord(left_x,avg_val)

                    total_neg_area += self.get_area_below_cord(left_x,avg_val)
                    total_pos_area += self.get_area_above_cord(left_x,avg_val)

                    base = floor(avg_val)
                    a = 0
                    b = intersects_top_at_x_val - left_x
                    c = 1
                    d = left_y - base

                    (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                    weight_of_tile = self.get_tile_at_cord(left_x,avg_val)
                    pos_sum += (area_above * weight_of_tile)
                    neg_sum += (area_below * weight_of_tile)

                    total_neg_area += area_below
                    total_pos_area += area_above
                    
                else:
                    avg_val_top = (int_between[-1] + self.number_of_rows)/2
                    avg_val_bottom = (int_between[0] + left_y)/2
                    neg_sum += self.get_sum_below_cord(left_x,avg_val_bottom)
                    pos_sum += self.get_sum_above_cord(left_x,avg_val_top)

                    total_neg_area += self.get_area_below_cord(left_x,avg_val_bottom)
                    total_pos_area += self.get_area_above_cord(left_x,avg_val_top)

                    x_vals = [left_x]
                    y_vals = [left_y]
                    for each_int in int_between:
                        intersects_int_at = secant_method(left_x,right_x,lambda x: (y(x) - (each_int)),10^-6,10)
                        x_vals.append(intersects_int_at)
                        y_vals.append(each_int)
                    x_vals.append(intersects_top_at_x_val)
                    y_vals.append(self.number_of_rows)

                    for (sub_division_left_x,sub_division_left_y,sub_division_right_x, sub_division_right_y) in zip(x_vals,y_vals,x_vals[1:],y_vals[1:]):
                        sub_divison_avg = (sub_division_left_y + sub_division_right_y)/2

                        base = floor(sub_divison_avg)

                        a = sub_division_left_x - left_x
                        b = sub_division_right_x - left_x
                        c = sub_division_right_y - base
                        d = sub_division_left_y - base
                        
                        (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                        weight_of_tile = self.get_tile_at_cord(left_x,base)
                        pos_sum += (area_above * weight_of_tile)
                        neg_sum += (area_below * weight_of_tile)

                        total_neg_area += area_below
                        total_pos_area += area_above

            elif self.is_cartessian_y_val_below_matrix(left_y) and self.is_cartessian_y_val_above_matrix(right_y):
                #very step line
                int_between = get_integers_between_vals(0,self.number_of_rows)
                intersects_top_at_x_val = secant_method(left_x,right_x,lambda x: (y(x) - self.number_of_rows),10^-6,10)
                intersects_bottom_at_x_val = secant_method(left_x,right_x,lambda x: y(x),10^-6,10)
                
                avg_val_top = (int_between[-1] + self.number_of_rows)/2
                avg_val_bottom = (int_between[0])/2
                neg_sum += self.get_sum_below_cord(left_x,avg_val_bottom)
                pos_sum += self.get_sum_above_cord(left_x,avg_val_top)

                total_neg_area += self.get_area_below_cord(left_x,avg_val_bottom)
                total_pos_area += self.get_area_above_cord(left_x,avg_val_top)

                x_vals = [intersects_bottom_at_x_val]
                y_vals = [0]
                for each_int in int_between:
                    intersects_int_at = secant_method(left_x,right_x,lambda x: (y(x) - (each_int)),10^-6,10)
                    x_vals.append(intersects_int_at)
                    y_vals.append(each_int)
                x_vals.append(intersects_top_at_x_val)
                y_vals.append(self.number_of_rows)

                for (sub_division_left_x,sub_division_left_y,sub_division_right_x, sub_division_right_y) in zip(x_vals,y_vals,x_vals[1:],y_vals[1:]):
                    sub_divison_avg = (sub_division_left_y + sub_division_right_y)/2

                    base = floor(sub_divison_avg)

                    a = sub_division_left_x - left_x
                    b = sub_division_right_x - left_x
                    c = sub_division_right_y - base
                    d = sub_division_left_y - base
                    
                    (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                    weight_of_tile = self.get_tile_at_cord(left_x,base)
                    pos_sum += (area_above * weight_of_tile)
                    neg_sum += (area_below * weight_of_tile)

                    total_neg_area += area_below
                    total_pos_area += area_above
                
            else:
                #both sides are in matrix
                int_between = get_integers_between_vals(left_y,right_y)
                
                if len(int_between) == 0:
                    avg_val = (left_y + right_y)/2
                    neg_sum += self.get_sum_below_cord(left_x,avg_val)
                    pos_sum += self.get_sum_above_cord(left_x,avg_val)

                    total_neg_area += self.get_area_below_cord(left_x,avg_val)
                    total_pos_area += self.get_area_above_cord(left_x,avg_val)

                    base = floor(avg_val)
                    a = 0
                    b = 1
                    c = right_y - base
                    d = left_y - base

                    (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                    weight_of_tile = self.get_tile_at_cord(left_x,avg_val)
                    pos_sum += (area_above * weight_of_tile)
                    neg_sum += (area_below * weight_of_tile)

                    total_neg_area += area_below
                    total_pos_area += area_above
                    
                else:
                    avg_val_top = (int_between[-1] + right_y)/2
                    avg_val_bottom = (int_between[0] + left_y)/2
                    neg_sum += self.get_sum_below_cord(left_x,avg_val_bottom)
                    pos_sum += self.get_sum_above_cord(left_x,avg_val_top)

                    total_neg_area += self.get_area_below_cord(left_x,avg_val_bottom)
                    total_pos_area += self.get_area_above_cord(left_x,avg_val_top)

                    x_vals = [left_x]
                    y_vals = [left_y]
                    for each_int in int_between:
                        intersects_int_at = secant_method(left_x,right_x,lambda x: (y(x) - (each_int)),10^-6,10)
                        x_vals.append(intersects_int_at)
                        y_vals.append(each_int)
                    x_vals.append(right_x)
                    y_vals.append(right_y)

                    for (sub_division_left_x,sub_division_left_y,sub_division_right_x, sub_division_right_y) in zip(x_vals,y_vals,x_vals[1:],y_vals[1:]):
                        sub_divison_avg = (sub_division_left_y + sub_division_right_y)/2

                        base = floor(sub_divison_avg)

                        a = sub_division_left_x - left_x
                        b = sub_division_right_x - left_x
                        c = sub_division_right_y - base
                        d = sub_division_left_y - base
                        
                        (area_above,area_below) = area_of_tile_divide_by_positive_line(a,b,c,d)
                        weight_of_tile = self.get_tile_at_cord(left_x,base)
                        pos_sum += (area_above * weight_of_tile)
                        neg_sum += (area_below * weight_of_tile)

                        total_neg_area += area_below
                        total_pos_area += area_above
                    
                    
        return (pos_sum,neg_sum,total_pos_area,total_neg_area)
            

    def split(self, degree):
        if degree >= 0 and degree <= 90:
            (pos_sum,neg_sum,pos_area,neg_area) = self._split_at_angle_between_0_and_45(degree)
            return (pos_sum,neg_sum,pos_area,neg_area)

def rotate(data,cx,cy,startDegree = 0, stopDegree = 180, deltaDegree = 0.25, includeStopDegree = True,name=""):
    dataFromRotation = dataForGalaxy(name,sum(sum(data)))
    matrix0 = fits_matrix(data,cx,cy)

    (data90,cx90,cy90) = rotate90clockwise(data,cx,cy)
    matrix90 = fits_matrix(data90,cx90,cy90)

    (data180,cx180,cy180) = rotate90clockwise(data90,cx90,cy90)
    matrix180 = fits_matrix(data180,cx180,cy180)

    (data270,cx270,cy270) = rotate90clockwise(data180,cx180,cy180)
    matrix270 = fits_matrix(data270,cx270,cy270)

    currentDegree = startDegree
    while currentDegree < stopDegree or (includeStopDegree and currentDegree == stopDegree):
        if currentDegree < 90:
            (pos_sum,neg_sum,pos_area,neg_area) = matrix0.split(currentDegree)
        elif currentDegree < 180:
            (neg_sum,pos_sum,neg_area,pos_area) = matrix90.split(currentDegree - 90) #for graph to line up at endpoints, order flipped
        elif currentDegree < 270:
            (pos_sum,neg_sum,pos_area,neg_area) = matrix180.split(currentDegree - 180)
        elif currentDegree < 360:
            (neg_sum,pos_sum,neg_area,pos_area) = matrix270.split(currentDegree - 270) #for graph to line up at endpoints, order flipped
        dataFromRotation.addDataPoint(currentDegree,pos_sum,neg_sum)
        currentDegree += deltaDegree
        
    return dataFromRotation

