from astropy.io import fits
from os.path import exists
import matplotlib.pyplot as plt
import xlrd

def readFits(path):
    hdul = fits.open(path)
    data = hdul[0].data
    return data

def writeFits(matrix,path):
    hdu = fits.PrimaryHDU(matrix)
    hdu.writeto(path)

#for analysis:
def plot_histogrm_of_brightness(brightness):
    avg = sum(brightness)/len(brightness)
    print(avg)
    plt.hist(brightness,bins = 30)
    plt.xlabel("difference in brightness (between I-band and G-band)")
    plt.ylabel("number of pixels")
    plt.title("Composite I-G Fits Image of an Elliptical Galaxy. Avg diff. = {}".format(int(avg)))
    plt.show()


def anlyze_brightness_of_fits(path):
    diffs = []
    
    the_data = readFits(path)
    for each in the_data:
        for every in each:
            if every > 0.0:
                diffs.append(every)
    plot_histogrm_of_brightness(diffs)

def anlyze_avg_brightness_of_fits(path):
    diffs = []
    
    the_data = readFits(path)
    for each in the_data:
        for every in each:
            if every > 0.0:
                diffs.append(every)
    return sum(diffs)/len(diffs)


def get_offsets():
    offset_path = "D:\\Galaxies\\i_minus_g\\galaxy_offset_list.xlsx"

    wb = xlrd.open_workbook(offset_path)
    sheet = wb.sheet_by_index(0)

    the_dict = {}
    for i in range(1000):
        row = sheet.row_values(i)
        name = str(row[0])
        offset = abs(float(row[1]))
        the_dict[name] = offset
    return the_dict

def get_fits_avg_from_name(name,offset=0):
    the_path = "D:\\Galaxies\\i_minus_g_output\\el\\{}\\100_percent\\cropped_c.fits".format(name)
    #print(the_path)
    if exists(the_path):
        diff_avg = anlyze_avg_brightness_of_fits(the_path)
        new_diff = diff_avg-offset
        #new_diff = diff_avg
    else:
        new_diff = None
    return new_diff

def plot_avgs(avgs):
    avg = sum(avgs)/len(avgs)
    to_plot = []
    for i in avgs:
        if abs(i) < 250:
            to_plot.append(i)
    plt.hist(to_plot,bins = 75)
    plt.xlabel("average difference in brightness (between I-band and G-band)")
    plt.ylabel("number of pixels")
    plt.title("Average Brightness Difference from 500 Elliptical Galaxies Composite Images [corrected for offset]. Avg = {}".format(int(avg)))
    plt.show()


def get_avg_for_all():
    the_dict = get_offsets()

    avgs = []

    for each_name in the_dict:
        new_diff = get_fits_avg_from_name(each_name,the_dict[each_name])
        if new_diff != None:
            avgs.append(new_diff)
    plot_avgs(avgs)
        

if __name__ == "__main__":
    #path = "D:\\Galaxies\\i_minus_g_output\\el\\1237645943978983553\\100_percent\\cropped_c.fits"
    #if you get an error like this:
    #ERROR: IOError: File-like object does not have a 'write' method, required for mode 'ostream'. [astropy.io.fits.file]
    #try uncommenting lines below, and run it:
    #fits_image_filename = fits.util.get_testdata_filepath('test0.fits')
    #hdul = fits.open(fits_image_filename)
    #anlyze_brightness_of_fits(path)
    get_avg_for_all()
