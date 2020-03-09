import csv
from galaxy_params import galaxy_params
from galaxy_params_constants import TRUE_STRINGS,FALSE_STRINGS, KEYS

def _is_bool_string(the_string):
    return the_string in TRUE_STRINGS or the_string in FALSE_STRINGS

def _convert_string_to_bool(the_string):
    if the_string in TRUE_STRINGS:
        return True
    return False

def _is_float_string(the_string):
    try:
        float(the_string)
        return True
    except:
        return False

def _convert_string_to_float(the_string):
    return float(the_string)


def clean_row(the_row):
    new_row = []
    for each_entry in the_row:
        the_entry = each_entry.strip()
        if len(the_entry) > 0 and not the_entry.isspace():
            if _is_bool_string(the_entry):
                the_entry = _convert_string_to_bool(the_entry)
            elif _is_float_string(the_entry):
                the_entry = _convert_string_to_float(the_entry)
            new_row.append(the_entry)
    return new_row

def read_csv_raw_data(csv_file):
    header = []
    data = []
    is_header = True
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if is_header:
                header = clean_row(row)
                is_header = False
            else:
                data = clean_row(row)
    return (header,data)

def get_data_dict(header,data):
    the_dict = dict()

    try:
        for i in range(len(header)):
            the_current_key = header[i]
            the_current_data = data[i]

            if the_current_key in KEYS:
                the_dict[the_current_key] = the_current_data
    except:
        pass

    return the_dict


def read_galaxy_param_for_a_galaxy(csv_path,name,is_spiral,wave_band="r"):
    the_params = galaxy_params()

    (header, data) = read_csv_raw_data(csv_path)
    the_params_dict = get_data_dict(header, data)

    #load params:
    the_params.load_dict(the_params_dict)

    #set input params:
    the_params.set_the_input_params()

    #set name and is spiral:
    the_params.set_name(name)
    the_params.set_is_spiral(is_spiral)
    the_params.set_wave_band(wave_band)

    return the_params

if __name__ == "__main__":
    the_path = "D:\\Galaxies\\galaxies_input\\el\\1237645943978983553\\1237645943978983553_r.csv"
    the_name = "1237645943978983553"
    is_spiral = False

    read_galaxy_param_for_a_galaxy(the_path,the_name,is_spiral)


