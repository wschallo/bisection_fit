from base import *

def cxCyFromCenter(center_row,center_col,shape,convertFromOneBasedIndexing=False):
    #center_row and center_col are refrenced from top left corner -> convert to cartesian (bottom left)
    #convert from 1 base indexing corrects indexing to fit python conventions
    number_of_rows = shape[0]
    
    #cx = center_col - 1
    #cx = center_col + 0.5 #x plus 0.5
    cx = center_col - 0.5 #x minus 0.5 #correct? 8/14/19
    #cx = center_col - 1 #used for something 1-3
    
    #cy = number_of_rows - (center_row - 1) #default (area_norm) # number 2
    #cy = number_of_rows - 1 - center_row #sanity # number 3
    ##cy = number_of_rows - center_row + 0.5 #sanity2 #number 4
    #cy = number_of_rows - center_row - 0.5 #sanity3 #number 5
    #cy = number_of_rows - (center_row - 2)
    #cy = number_of_rows - (center_row)  #new cy # number 1
    
    #cy = (number_of_rows - int(center_row)) + (center_row - int(center_row)) #something_1
    #cy = (number_of_rows - int(center_row)) - (center_row - int(center_row)) #something_2
    #cy = (number_of_rows - int(center_row)) - (center_row - int(center_row)) - 0.5 #something_3
    cy = (number_of_rows - int(center_row)) - (center_row - int(center_row)) + 0.5 #something 5 #correct? 8/14/19
    #cx = center_col - 1
    #cy = number_of_rows - (center_row)

    
    return (cx,cy)

def rotate90clockwise(matrix,cx,cy):
    return (rot90(matrix),matrix.shape[0]-cy,cx)

def get_equation_of_line_with_posiitve_slope(degree,cx,cy):
    #y - y1 = m(x - x1) -> y = (m(x - cx)) + y1
    #for a positive slope: m = tan(angle)
    m = 1 if degree == 45 else tan(radians(degree)) #to reduce error, manually setting m = 1 if degree == 45
    #m = tan(radians(degree))
    return lambda x: (m * (x - cx)) + cy

def get_integers_between_vals(min_val,max_val):
    return list(range(int(floor(min_val))+1,int(ceil(max_val))))

def secant_method(p0,p1,f,TOL,N):
    #adapted from: Numerical Analysis 10E pg.71

    i = 2
    q0 = f(p0)
    q1 = f(p1)
    p = 0 #temp

    try:

        while i <= N:
            p = p1 - q1*(p1 - p0)/(q1 - q0) #compute p_i
            if abs(p - p1) < TOL:
                return p
            else:
                i = i + 1
                p0 = p1
                q0 = q1
                p1 = p
                q1 = f(p)
        return p
    
    except ZeroDivisionError:
        return p

def area_of_tile_divide_by_positive_line(a,b,c,d):
    area_of_triangle = (b-a)*(c-d)*0.5
    area_below_triangle = d * (b-a)
    area_to_right_of_triangle = 1.0 * (1.0 - b)

    area_below = area_of_triangle + area_below_triangle + area_to_right_of_triangle
    area_above = 1 - area_below

    if area_below < 0 or area_below > 1:
        print("area error",a,b,c,d)
    return (area_above,area_below)

def plotIt(x,y,name,y1=[],y1_label = "",y2_label = "",saveTo = "",x_label="Degree",y_label="Brightness Difference/ Total Brightness"):
    plt.plot(x,y,'-k',label = y1_label)
    if y1 != []:
        plt.plot(x,y1,'-b', label = y2_label)
    plt.title("Galaxy: {}".format(name))
    plt.xlabel("Degree")
    #plt.ylabel("Brightness Difference/ Total Brightness") #check which one datapoints/ fit and plot
    plt.ylabel("Difference in flux") #check which one datapoints/ fit and plot
    plt.legend(loc='upper left')
    if saveTo == "":
        plt.show()
    else:
        plt.savefig(saveTo)
    plt.clf()
