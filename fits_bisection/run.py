from get_galaxy import *
from fits import *
import matplotlib.pyplot as plt
from math import sqrt

def run_on_large_batch(isSpiral,limit):
    weHave = getBulges(True) #CURRENTLY USES BUlDGE RADIUS AS SEMI MAJOR
    gals = loadParams(isSpiral,weHave,limit)

    
    

    while len(gals) != 0:
        current_gal = gals.pop()
        
        print(current_gal.name)
        #current_gal.semi_major_axis_length = 0.6 * current_gal.semi_major_axis_length
        current_gal.run()
        #current_gal.save_data("output_y4_x_plus_0.5")
        #current_gal.fit_data_and_plot(True)
        current_gal.save_data("bulge_8_23_19_1") #uncomment this line to run properly
        
        current_gal = None #save memory by removing object (should only be factor for large runs)
        del current_gal

def run_area_comp_on_large_batch(isSpiral,limit):
    gals = loadParams(isSpiral,[],limit)

    to_plot = []

    while len(gals) != 0:
        current_gal = gals.pop()
        #print(current_gal.name)
        current_gal.run()
        #current_gal.save_data("output_test")
        print(current_gal.original_data.shape[0]*current_gal.original_data.shape[1],current_gal.original_data.shape[0],current_gal.original_data.shape[1])
        #if str(input()) == str(1):
        plotAreaDiff((current_gal.normalized_data_point.getDifferenceSum()),current_gal.name)
        
        current_gal = None #save memory by removing object (should only be factor for large runs)
        del current_gal
    return to_plot

def manualRun():
    #gal = loadParams(True,["1237648720697360592"])[0] #compared website and openlab data
    #1237648720158654584
    
    #gal = loadParams(True,["1237648720158654584"])[0]
    gal = loadParams(True,["1237648704595624148"])[0]
    print(gal.semi_major_axis_length)
    #gal.semi_major_axis_length = 7.929384701*.75

    #gal.semi_major_axis_length = 62.02705673/2
    #gal.semi_major_axis_length = 16.09999005

    #gal.center_row = 43.0345
    #gal.center_col = 42.369
    #gal.center_row = 56.37697781
    #gal.center_col = 56.22958479

    #gal.run()
    #print(gal.area_data_points.getDifferenceSum())
    #gal.maxAreaDiff()
    #gal.fit_data_and_plot(True)
    #gal.save_data("test_8_23_19_multiply_75")

def test():
    image_data = fits.getdata("C:\\Users\\wills\\Desktop\\fits_bisection\\output_normal\\sp\\1237648720697360592\\input_a.fits", ext=0)
    read_f = readFits("C:\\Users\\wills\\Desktop\\fits_bisection\\output_normal\\sp\\1237648720697360592\\input_a.fits")

    print(read_f[2][3],image_data[2][3])
    print(read_f[31][74],image_data[31][74])
    
    plt.figure()
    plt.imshow(image_data, cmap='gray')
    plt.colorbar()
    plt.show()

def plotAreaDiff(delta_angles,title):
    #plt.hist(delta_angles, range=[-0.002, 0.002],density=False, bins=100)
    plt.hist(delta_angles,density=False, bins=100)
    print(len(delta_angles))
    #plt.hist(delta_angles.values(), bins=36)
    plt.title(title)
    plt.xlabel('(area_1-area_2)/total_area')
    plt.ylabel('Probability')
    plt.show()

if __name__ == "__main__":
    ##1237651495756497248: 37.11172823, 0.5132206787, 52.17440309, 48.46392926
    #gal = loadParams(True,["1237651495756497248"])[0]
    #gal.run()
    #manualRun()
    #to_plot = run_area_comp_on_large_batch(True,1000)
    
    #test()
    #gal.save_data("output_test")
    #run_on_large_batch(True,10)

    #manualRun()
    
    run_on_large_batch(True,1000)
    #run_on_large_batch(False,5000)
    #run_on_large_batch(False,500)
    
    #run_on_large_batch(True,100) 
    ##run_on_large_batch(False,500)
    #manualRun()
    #run_on_large_batch(True,1000) #currently trying new cx and cy
    #b = "C:\\Users\\wills\\Desktop\\fits_bisection\\output_new_cy\\sp\\1237655503499559298\\input_a.fits"
    #c = readFits(b)
    #print(c[0][4])
    #print(c[1][4])
    #print(c[2][4])
    #print(c[8][9])
    """
    print("spirals")
    for each_gal in loadParams(True,[],100):
        print(each_gal.name)
        each_gal.run()
        each_gal.save_data("output_test5")
    """
    """
    print("ellipticals")
    for each_gal in loadParams(False,[],5):
        print(each_gal.name)
        each_gal.run()
        each_gal.save_data("output_test2")
    """
#run_on_large_batch: 100 gals in 2:36
#python (x,y) = matlab(x+1,y+1) [using imread]
#ex: python[0][4] = matlab[1][5]


