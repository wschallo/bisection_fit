import os
import matplotlib.pyplot as plt

def label_to_mult(label):
    return float(label.strip().split("_")[0])/100.0

def make_plot_and_save(ratios,angle_diffs,flux_diffs,path_to_save):
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('ratio of buldge radius')
    ax1.set_ylabel('delta anlge (deg)', color=color)
    ax1.scatter(ratios,angle_diffs,color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('delta flux (photons/pixels^2)', color=color)  # we already handled the x-label with ax1
    ax2.scatter(ratios,flux_diffs,color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(path_to_save)

def compare_angles(path,path_to_save):
    diffs = []
    names = []

    d = path
    dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    for each in dirs:
        angle_compare = os.path.join(d, each,"100_percent","angle_compare.txt")
        if not os.path.exists(angle_compare):
            print("here")
            continue
        with open(angle_compare) as f:
            first_line = True
            for e in f.readlines():
                if first_line:
                    first_line = False
                    continue
                to_parse = e.strip().split(" ")
                actual = float(to_parse[2])
                mine = float(to_parse[3])
                difference = float(to_parse[4])
                diffs.append(difference)
                if abs(difference) <= 5.0:
                    names.append(each)

    print(names)
    #print(names[0])
                
    #plt.hist(diffs,bins=50)
    #plt.ylabel("number of galaxies")
    #plt.xlabel("angle difference")
    #plt.title("500 eliptical galaxies, 1.25 * bulge_radius")
    #plt.show()
    
    

def get_angle_compare(path,path_to_save):
    d = path
    dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    xs = []
    ys = []
    zs = []
    for each in dirs:
        angle_compare = os.path.join(d, each,"angle_compare.txt")
        with open(angle_compare) as f:
            first_line = True
            for e in f.readlines():
                if first_line:
                    first_line = False
                    continue
                to_parse = e.strip().split(" ")
                #print(label_to_mult(each))
                #print(to_parse)
                actual = float(to_parse[2])
                mine = float(to_parse[3])
                difference = float(to_parse[4])
                percent_diff = float(to_parse[5])
                #print(abs(percent_diff)) #absolut difference in flux
                #print(difference)
                xs.append(label_to_mult(each))
                ys.append(difference) #angle diff.
                zs.append(percent_diff) #flux diff.
    make_plot_and_save(xs,ys,zs,path_to_save)
    
def get_all_angle(path,to_save):
    d = path
    dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    for each_gal in dirs:
        print(each_gal)
        angle_compare_path = os.path.join(path,each_gal)
        save_figure_path = os.path.join(to_save,"{}.png".format(each_gal))
        #print(angle_compare_path,save_figure_path)
        if not os.path.exists(save_figure_path):
            get_angle_compare(angle_compare_path,save_figure_path)
    

if __name__ == "__main__":
    #pa = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\outut_diff_flux\\test_variable_size\\sp\\1237648704595624148"
    #pa = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\outut_diff_flux\\test_variable_size\\sp\\1237648721748099461"
    #pa = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\output_difference_in_flux\\r_band\\sp\\1237648720149610779"
    #get_angle_compare(pa)
    #pa = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\output_difference_in_flux\\r_band\\el" #(previous)
    #pa_output = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\output_difference_in_flux\\r_band\\el_angle_comp" #(prveious)
    pa = "D:\\Galaxies\\i_minus_g_output\\el" #changed for i-g
    pa_output = "D:\\Galaxies\\i_minus_g_output\\el_angle_comp" #changed for i-g
    compare_angles(pa,pa_output)
    #get_all_angle(pa,pa_output)
