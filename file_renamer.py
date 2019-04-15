"""
This renames a bunch of files that have numbers at the end of the file names.
"""

import os

# input path to folder of pictures
# if it's the current working directory, type down cwd
PATH_TO_FOLDER_OF_PICTURES = "fwd"

STARTING_NUMBER_FOR_RENAMING_IMAGES = 64

TYPES_OF_FILES_TO_RENAME = "jpeg, xml, png"

from os import listdir, makedirs, rename
from os.path import isfile, join, exists

# just a few sanity checks
assert type(STARTING_NUMBER_FOR_RENAMING_IMAGES) is int
assert type(PATH_TO_FOLDER_OF_PICTURES) is str
assert type(TYPES_OF_FILES_TO_RENAME) is str

# TODO: make the feature below:
# if PATH_TO_FOLDER_OF_PICTURES == "cwd"
if PATH_TO_FOLDER_OF_PICTURES == "cwd":
    PATH_TO_FOLDER_OF_PICTURES = os.getcwd()

if PATH_TO_FOLDER_OF_PICTURES == "fwd":
    separator = os.path.join("a","a").split("a")[1]
    path_and_file = os.path.abspath(__file__).split(separator)
    PATH_TO_FOLDER_OF_PICTURES = separator.join(path_and_file[:-1])
# put in path to current working directory

# create list of file types
file_types = TYPES_OF_FILES_TO_RENAME.split(",")
dummy_list = []
# take away whitespaces
for types in file_types:
    dummy_list.append(types.strip())
file_types = dummy_list

# TODO: add in sanity check to check that there are the same number of types for each name

# create list of files
folder_of_files = []
for file_type in file_types:
    folder_of_files += [f for f in listdir(PATH_TO_FOLDER_OF_PICTURES) \
                        if isfile(join(PATH_TO_FOLDER_OF_PICTURES, f)) \
                        if f.endswith(str(file_type))]

# create folder inside current folder for images
new_folder_name = PATH_TO_FOLDER_OF_PICTURES
if PATH_TO_FOLDER_OF_PICTURES[-1] != "/":
    new_folder_name += "/Renamed_Files"
else:
    new_folder_name += "Renamed_Files"
if not exists(new_folder_name):
    makedirs(new_folder_name)

# Give some indication of what you're doing
print('Renaming the following files:')
print(folder_of_files)


# rename files
folder_of_files.sort()
index = STARTING_NUMBER_FOR_RENAMING_IMAGES - 1
for files in folder_of_files:
    file_type = files.split(".")[-1]
    index += 1
    newFileName = str(index) + '.' + file_type
    current_place = join(PATH_TO_FOLDER_OF_PICTURES, files)
    new_place = join(new_folder_name, newFileName)
    rename(current_place, new_place)


'''
# rename files
folder_of_files.sort()
index = STARTING_NUMBER_FOR_RENAMING_IMAGES - 1
for files in folder_of_files:
    file_name = files.split('.')[:-1]
    index += 1
    for types in file_types:
        file_name.append(types)
        currentFileName = ".".join(file_name)
        file_name.remove(types)
        newFileName = str(index) + '.' + types
        current_place = join(PATH_TO_FOLDER_OF_PICTURES, currentFileName)
        new_place = join(new_folder_name, newFileName)
        rename(current_place, new_place)
'''