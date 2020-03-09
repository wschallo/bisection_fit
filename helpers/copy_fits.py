from shutil import copyfile
from os.path import join
import os

#source folder with fits:
SRC_DIR = ""

#dest folder:
DEST_DIR = ""

def copy_file(src,dest):
    copyfile(src, dst)

def get_fits_files_from_source_dir():
    for file in os.listdir(SRC_DIR):
        if file.endswith(".fits"):
            print(os.path.join(SRC_DIR, file))

def copy_all_fits_files():
    get_fits_files_from_source_dir()

if __name__ == "__main__":
    copy_all_fits_files()
