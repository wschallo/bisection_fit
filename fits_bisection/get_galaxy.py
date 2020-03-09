from galaxy import galaxy
from base import get_params_path

def create_galaxy(name,center_row,center_col,semi_major_length,semi_major_angle,isSpiral):
    return galaxy(name,center_row,center_col,semi_major_length,semi_major_angle,isSpiral)

def loadParams(isSpiral,to_get=[],limit=-1):
    galaxies = []
    
    isHeader = True

    bulgeRadius = loadAxis(True)
    
    with open(get_params_path(isSpiral),'r') as f:
        for each_line in f.readlines():
            if isHeader:
                isHeader = False
            else:
                toParse = each_line.strip().split(":")
                info = toParse[1].strip().replace(" ","").split(",")
                
                name = str(toParse[0])
                if (to_get == [] or name in to_get):
                    #majoraxis = float(info[0])/2 #not sure if should divide by 2
                    majoraxis = bulgeRadius[name]
                    angle = float(info[1])
                    row = float(info[2])
                    col = float(info[3])

                    galaxies.append(create_galaxy(name,row,col,majoraxis,angle,isSpiral))

                if (to_get != [] and len(galaxies) == len(to_get)): break
                if (limit != -1 and len(galaxies) > limit): break
                
            
    return galaxies

def getBulges(isSpiral):
    name = []
    path = "C:\\Users\\wills\\Desktop\\sparcfire\\fits_bisection\\bulge.txt"
    with open(path,'r') as f:
        for each_line in f:
            to_parse = each_line.strip().split(" ")
            name.append(to_parse[0])
    return name

def loadAxis(isSpiral):
    bulge_radius = dict()
    path = "C:\\Users\\wills\\Desktop\\sparcfire\\fits_bisection\\bulge.txt"
    with open(path,'r') as f:
        for each_line in f:
            to_parse = each_line.strip().split(" ")
            name = to_parse[0]
            bulge = float(to_parse[1])
            bulge_radius[name] = bulge
    return bulge_radius
