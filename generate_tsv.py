import os
import csv 

def label_to_mult(label):
    return float(label.strip().split("_")[0])/100.0

def write_to_tsv(to_write,the_path,gal_name,is_spiral):
    to_write = sorted(to_write,key=lambda x: x[0])
    for each in to_write:
        write_this = [gal_name,is_spiral,each[0],each[1][0],each[1][1]]
        with open(the_path,'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(write_this)
    

def get_angle_compare(path,path_to_save,gal_name = "",is_spiral = True):
    d = path
    dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    xs = []
    ys = []
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
                ys.append((difference,percent_diff)) #angle diff.
    write_to_tsv(zip(xs,ys),path_to_save,gal_name,is_spiral)


def get_all_angle(path,to_save):
    d = path
    dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    for each_gal in dirs:
        print(each_gal)
        angle_compare_path = os.path.join(path,each_gal)
        #save_figure_path = os.path.join(to_save,"{}.png".format(each_gal))
        #print(angle_compare_path,save_figure_path)
        #if not os.path.exists(save_figure_path):
        get_angle_compare(angle_compare_path,to_save,each_gal,False)
            
if __name__ == "__main__":
    pa = "C:\\Users\\wills\\Desktop\\sparcfire\\refactored_fits_bisection\\output_difference_in_flux\\r_band\\el"
    pa_output = "C:\\Users\\wills\\Desktop\\fits_bisection.csv"
    get_all_angle(pa,pa_output)
