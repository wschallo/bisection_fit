from base import *

def solveForLengthOfSideOfRightTriangle(b,c):
    #a^2 + b^2 = c^2
    
    return sqrt((c**2)-(b**2))

def pointIsInCircle(cx,cy,radius,x,y):
    return sqrt((abs(x-cx)**2) + (abs(y-cy)**2)) <= radius

def getAreaBelowNegativeLine(a,b,c,d):
    area_of_triangle = (b-a)*(d-c)*0.5
    below_triangle = c * (b-a)
    left_of_triangle = d * a
    return (area_of_triangle + below_triangle + left_of_triangle)

def getAreaAboveNegativeLine(a,b,c,d):
    return 1.0 - getAreaBelowNegativeLine(a,b,c,d)

def getAreaBelowPositiveLine(a,b,c,d):
    area_of_triangle = (b-a)*(d-c)*0.5
    below_triangle = c * (b-a)
    right_of_triangle = (1.0 - b)*d
    return (area_of_triangle + below_triangle + right_of_triangle)

def getAreaAbovePositiveLine(a,b,c,d):
    return 1.0 - getAreaBelowPositiveLine(a,b,c,d)

def getAreaOfPixelInCircle(cx,cy,radius,left_x,right_x,bottom_y,top_y):
    bottomLeftCorner = pointIsInCircle(cx,cy,radius,left_x,bottom_y)
    bottomRightCorner = pointIsInCircle(cx,cy,radius,right_x,bottom_y)
    topLeftCorner = pointIsInCircle(cx,cy,radius,left_x,top_y)
    topRightCorner = pointIsInCircle(cx,cy,radius,right_x,top_y)
    
    areCornersInCircle = [bottomLeftCorner,
                          bottomRightCorner,
                          topLeftCorner,
                          topRightCorner]
    
    if False not in areCornersInCircle:
        #all corners of pixel in cirlce
        return 1.0
    elif True not in areCornersInCircle:
        #all corners of pixel not in cirlce
        return 0.0
    else:
        if False not in [bottomLeftCorner,bottomRightCorner]:
            #bottom side of pixel in circle
            ##here = pixle in top half of circle
            if topLeftCorner == True:
                #bottom side and top left corner in cirlce (top right not in circle) [case 1]
                deltaY_TopIntersection = top_y - cy
                deltaX_TopIntersection = solveForLengthOfSideOfRightTriangle(deltaY_TopIntersection,radius)

                deltaX_RightIntersection = right_x - cx
                deltaY_RightIntersection = solveForLengthOfSideOfRightTriangle(deltaX_RightIntersection,radius)

                x_of_top_intersection = cx + deltaX_TopIntersection
                y_of_right_intersection = cy + deltaY_RightIntersection

                a = x_of_top_intersection - left_x
                b = 1.0
                c = y_of_right_intersection - bottom_y
                d = 1

                return getAreaBelowNegativeLine(a,b,c,d)
            
            elif topRightCorner == True:
                #bottom side and top right corner in cirlce (top left not in circle) [case 2]
                deltaY_TopIntersection = top_y - cy
                deltaX_TopIntersection = solveForLengthOfSideOfRightTriangle(deltaY_TopIntersection,radius)

                deltaX_LeftIntersection = cx - left_x
                deltaY_LeftIntersection = solveForLengthOfSideOfRightTriangle(deltaX_LeftIntersection,radius)

                x_of_top_intersection = cx - deltaX_TopIntersection
                y_of_left_intersection = cy + deltaY_LeftIntersection
                
                a = 0.0
                b = x_of_top_intersection - left_x
                c = y_of_left_intersection - bottom_y
                d = 1.0

                return getAreaBelowPositiveLine(a,b,c,d)
            else:
                #only bottom side in circle (top side not in circle) [case 3]

                #check this is working
                
                deltaX_leftIntersection = abs(cx-left_x)
                deltaY_leftIntersection = solveForLengthOfSideOfRightTriangle(deltaX_leftIntersection,radius)

                deltaX_rightIntersection = abs(cx-right_x)
                deltaY_rightIntersection = solveForLengthOfSideOfRightTriangle(deltaX_rightIntersection,radius)
                triangle_area = abs(deltaY_leftIntersection-deltaY_rightIntersection)*1.0*0.5
                area_below = ((min(deltaY_leftIntersection,deltaY_rightIntersection) + cy)-bottom_y) * 1.0
                
                return (triangle_area+area_below)
                
            
        elif False not in [topLeftCorner,topRightCorner]:
            #top side of pixel in circle
            ##here = pixle in bottom half of circle
            if bottomLeftCorner == True:
                #top side and bottom left corner in cirlce (bottom right not in circle) [case 4]
                deltaY_bottomIntersection = cy - bottom_y 
                deltaX_bottomIntersection = solveForLengthOfSideOfRightTriangle(deltaY_bottomIntersection,radius)

                deltaX_rightIntersection =  right_x - cx
                deltaY_rightIntersection = solveForLengthOfSideOfRightTriangle(deltaX_rightIntersection,radius)

                x_of_bottom_intersection = cx + deltaX_bottomIntersection
                y_of_right_intersection = cy - deltaY_rightIntersection

                a = x_of_bottom_intersection - left_x
                b = 1.0
                c = 0.0
                d = y_of_right_intersection - bottom_y

                return getAreaAbovePositiveLine(a,b,c,d)
                
            elif bottomRightCorner == True:
                #top side and bottom right corner in cirlce (bottom left not in circle) [case 5]
                deltaX_leftIntersection = cx - left_x
                deltaY_leftIntersection = solveForLengthOfSideOfRightTriangle(deltaX_leftIntersection,radius)

                deltaY_bottomIntersection = cy - bottom_y
                deltaX_bottomIntersection = solveForLengthOfSideOfRightTriangle(deltaY_bottomIntersection,radius)

                y_of_left_intersection = cy - deltaY_leftIntersection
                x_of_bottom_intersection = cx - deltaX_bottomIntersection

                a = 0.0
                b = x_of_bottom_intersection - left_x
                c = 0.0
                d = y_of_left_intersection - bottom_y

                return getAreaAboveNegativeLine(a,b,c,d)

            else:
                #only top side in circle (top side not in circle)
                deltaX_leftIntersection = abs(cx-left_x)
                deltaY_leftIntersection = solveForLengthOfSideOfRightTriangle(deltaX_leftIntersection,radius)

                deltaX_rightIntersection = abs(cx-right_x)
                deltaY_rightIntersection = solveForLengthOfSideOfRightTriangle(deltaX_rightIntersection,radius)
                triangle_area = abs(deltaY_leftIntersection-deltaY_rightIntersection)*1.0*0.5
                area_above = (1.0-((cy-min(deltaY_leftIntersection,deltaY_rightIntersection))-bottom_y)) * 1.0

                return (triangle_area+area_above)
            
        elif False not in [bottomLeftCorner,topLeftCorner]:
            #left side of pixel in circle
            if bottomRightCorner == True:
                #left side and bottom right corner in cirlce (top right not in circle)
                ##this is covered in case 1
                pass
            elif topRightCorner == True:
                #left side and top right corner in cirlce (bottom right not in circle)
                ##this is covered in case 4
                pass
            else:
                #only left side in circle (top side not in circle) [case 6]
                deltaY_top_intersection = abs(cy-top_y)
                deltaX_top_intersection = solveForLengthOfSideOfRightTriangle(deltaY_top_intersection,radius)
                
                deltaY_bottom_intersection = abs(cy-bottom_y)
                deltaX_bottom_intersection = solveForLengthOfSideOfRightTriangle(deltaY_bottom_intersection,radius)

                triangle_area = abs(deltaX_top_intersection-deltaX_bottom_intersection)*1.0*0.5
                area_to_left = ((min(deltaX_top_intersection,deltaX_bottom_intersection)+cx) - left_x) * 1.0

                return (triangle_area + area_to_left)
            
        elif False not in [bottomRightCorner,topRightCorner]:
            #right side of pixel in circle
            if bottomLeftCorner == True:
                #right side and bottom left corner in cirlce (top left not in circle)
                ##this is covered in case 2
                pass
            elif topLeftCorner == True:
                #right side and top left corner in cirlce (bottom left not in circle)
                ##this is covered in case 5
                pass
            else:
                #only right side in circle (top side not in circle) [case 7]
                deltaY_top_intersection = abs(cy-top_y)
                deltaX_top_intersection = solveForLengthOfSideOfRightTriangle(deltaY_top_intersection,radius)
                
                deltaY_bottom_intersection = abs(cy-bottom_y)
                deltaX_bottom_intersection = solveForLengthOfSideOfRightTriangle(deltaY_bottom_intersection,radius)

                triangle_area = abs(deltaX_top_intersection-deltaX_bottom_intersection)*1.0*0.5
                area_to_right = (1.0-((cx-(min(deltaX_top_intersection,deltaX_bottom_intersection))) - left_x)) * 1.0

                return (triangle_area + area_to_right)
            
        elif bottomLeftCorner == True:
            #only bottom left corner in circle [case 8]
            deltaX_left_intersection = left_x - cx
            deltaY_left_intersection = solveForLengthOfSideOfRightTriangle(deltaX_left_intersection,radius)

            deltaY_bottom_intersection = bottom_y - cy
            deltaX_bottom_intersection = solveForLengthOfSideOfRightTriangle(deltaY_bottom_intersection,radius)

            y_of_left_intersection = cy + deltaY_left_intersection
            x_of_bottom_intersection = cx + deltaX_bottom_intersection

            a = 0
            b = x_of_bottom_intersection - left_x
            c = 0
            d = y_of_left_intersection - bottom_y

            return getAreaBelowNegativeLine(a,b,c,d)

        elif bottomRightCorner == True:
            #only bottom right corner in circle [case 9]
            deltaX_right_intersection = cx - right_x
            deltaY_right_intersection = solveForLengthOfSideOfRightTriangle(deltaX_right_intersection,radius)

            deltaY_bottom_intersection = bottom_y - cy
            deltaX_bottom_intersection = solveForLengthOfSideOfRightTriangle(deltaY_bottom_intersection,radius)

            y_of_right_intersection = cy + deltaY_right_intersection
            x_of_bottom_intersection = cx - deltaX_bottom_intersection

            a = x_of_bottom_intersection - left_x
            b = 1.0
            c = 0.0
            d = y_of_right_intersection - bottom_y

            return getAreaBelowPositiveLine(a,b,c,d)
            
        elif topLeftCorner == True:
            #only top left corner in circle [case 10]
            deltaX_left_intersection = left_x - cx
            deltaY_left_intersection = solveForLengthOfSideOfRightTriangle(deltaX_left_intersection,radius)

            deltaY_top_intersection = cy - top_y
            deltaX_top_intersection = solveForLengthOfSideOfRightTriangle(deltaY_top_intersection,radius)

            y_of_left_intersection = cy - deltaY_left_intersection
            x_of_top_intersection = cx + deltaX_top_intersection

            a = 0.0
            b = x_of_top_intersection - left_x
            c = y_of_left_intersection - bottom_y
            d = 1.0

            return getAreaAbovePositiveLine(a,b,c,d)
            
        elif topRightCorner == True:
            #only top right corner in circle [case 11]
            deltaY_top_intersection = cy - top_y
            deltaX_top_intersection = solveForLengthOfSideOfRightTriangle(deltaY_top_intersection,radius)

            deltaX_right_intersection = cx - right_x
            deltaY_right_intersection = solveForLengthOfSideOfRightTriangle(deltaX_right_intersection,radius)

            x_of_top_intersection = cx - deltaX_top_intersection
            y_of_right_intersection = cy - deltaY_right_intersection

            a = right_x - x_of_top_intersection
            b = 1.0
            c = y_of_right_intersection - bottom_y
            d = 1.0

            return getAreaAboveNegativeLine(a,b,c,d)
        else:
            print("error")
    return 0 

def create_area_matrix(cx,cy,semiMajorAxes,shape):
    (number_of_rows,number_of_cols) = shape
    radius = semiMajorAxes + 1

    area_array = np.zeros(shape)
    for (left_x,right_x) in zip(range(number_of_cols),range(1,number_of_cols+1)):
        for (bottom_y,top_y) in zip(range(number_of_rows),range(1,number_of_rows+1)):
                current_area =  (cx,cy,radius,left_x,right_x,bottom_y,top_y)
                col = left_x
                row = number_of_rows - bottom_y - 1
                area_array[row][col] = getAreaOfPixelInCircle(cx,cy,radius,left_x,right_x,bottom_y,top_y)
    return area_array
    
