'''
The purpose of this file is to use Python to make the images to train AI models with.

Dependencies: python 3.6.2, numpy, matplotlib, pillow, tqdm

Python is a bit more accessible than Matlab; therefore, this file will be better for
making training images in the long run.
'''


from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from os.path import isfile, join
from os import listdir
import os
from random import randint
import numpy as np
import copy
from tqdm import tqdm


#############################################
# SPECIFY NUMBER OF IMAGES YOU WANT TO MAKE #
number_of_images = 100
#############################################



# load backgrounds and shapes
cwd = os.getcwd()
backgrounds_path = join(cwd, 'backgrounds')
backgrounds = [f for f in listdir(backgrounds_path) if isfile(join(backgrounds_path, f))]
if '.DS_Store' in backgrounds:
    backgrounds.remove('.DS_Store')
backgrounds_raw = []
for files in backgrounds:
    im = Image.open(join(backgrounds_path,files))
    im = im.convert('RGB')
    im = np.asarray(im, dtype=np.uint8)
    backgrounds_raw.append(im)

shapes_path = join(cwd, 'assets', 'shape_templates')
shapes = [f for f in listdir(shapes_path) if isfile(join(shapes_path, f))]
shapes_raw = []
for files in shapes:
    im = Image.open(join(shapes_path,files))
    im = im.convert('L') # make it boolean
    im = np.asarray(im)
    shapes_raw.append(im)


alphanumeric_vector = ['A', 'B', 'C', 'D', 'E', 'F', \
                       'G', 'H', 'I', 'J', 'K', 'L', \
                       'M', 'N', 'O', 'P', 'Q', 'R', \
                       'S', 'T', 'U', 'V', 'W', 'X', \
                       'Y', 'Z', '1', '2', '3', '4', \
                       '5', '6', '7', '8', '9']


for file_number in tqdm(range(number_of_images)):
    # choose random alphanumeric and background
    letter = alphanumeric_vector[randint(0,len(alphanumeric_vector)-1)]
    background = copy.deepcopy(backgrounds_raw[randint(0,len(backgrounds)-1)])
    background.setflags(write=1) # make image writable
    shape_choice = randint(0,len(shapes)-1)
    shape = shapes_raw[shape_choice]

    # choose random color
    color_of_background = np.array([randint(0,255),randint(0,255),randint(0,255)])
    color_of_letter =     np.array([randint(0,255),randint(0,255),randint(0,255)])
    color_difference = np.sqrt(np.sum(np.square(color_of_background-color_of_letter)))
    # make sure the color difference is greater than a threshold
    while color_difference < 12:
        color_of_letter = np.array([randint(0,255),randint(0,255),randint(0,255)])
        color_difference = np.sqrt(np.sum(np.square(color_of_background-color_of_letter)))
        
        
    # draw random shape to a random background
    x_coor, y_coor = np.where(shape==False)
    x_max = background.shape[0]-1 - shape.shape[0]-1
    y_max = background.shape[1]-1 - shape.shape[1]-1
    change_x = randint(0, x_max)
    change_y = randint(0, y_max)
    x_tr = x_coor + change_x
    y_tr = y_coor + change_y
    background_mask = (x_tr, y_tr)
    background[background_mask] = color_of_background


    # draw letter on picture
    im = Image.fromarray(background)
    draw = ImageDraw.Draw(im)
    font_path = join(cwd, 'fonts', 'Arial.ttf')
    font_size = 26
    font = ImageFont.truetype(font_path, font_size)
    # change color to rgba
    rgba_color = tuple(color_of_letter.tolist() + [0])
    draw.text((12+change_y, 8+change_x), letter, font=font, fill=rgba_color)


    # create jpeg
    im.save(join(cwd, "test_images", f"{file_number}.jpeg"),'jpeg')

    # create xml file
    folder = 'test_images'
    filename = f'{file_number}.jpeg'
    path = join(cwd, folder)
    height = 40 # this is something that's known
    width = 40
    depth = 3
    xmin = change_y      # I'm not sure why it works when it's switched
    xmax = change_y + 40 # but it does...
    ymin = change_x
    ymax = change_x + 40
    newline = '\n'
    xml_string = [  '<annotation verified="yes">\n', 
                    '\t<folder>', folder, '</folder>\n',
                    '\t<filename>', filename, '</filename>\n',
                    '\t<path>', path, '</path>\n',
                    '\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n',
                    '\t<size>', newline,
                    '\t\t<width>', str(width), '</width>', newline,
                    '\t\t<height>', str(height), '</height>', newline,
                    '\t\t<depth>', str(depth), '</depth>', newline,
                    '\t</size>\n',
                    '\t<segmented>0</segmented>\n',
                    '\t<object>', newline,
                    '\t\t<name>', shapes[shape_choice][:-4], '</name>', newline,
                    '\t\t<pose>Unspecified</pose>', newline,
                    '\t\t<truncated>0</truncated>', newline,
                    '\t\t<difficult>0</difficult>', newline,
                    '\t\t<bndbox>', newline,
                    '\t\t\t<xmin>', str(xmin), '</xmin>', newline,
                    '\t\t\t<ymin>', str(ymin), '</ymin>', newline,
                    '\t\t\t<xmax>', str(xmax), '</xmax>', newline,
                    '\t\t\t<ymax>', str(ymax), '</ymax>', newline,
                    '\t\t</bndbox>', newline,
                    '\t</object>\n',
                    '</annotation>\n']
    xml_name = f'{file_number}.xml'
    xml_path = join(folder, xml_name)
    file_object = open(xml_path, 'w')
    file_object.write(''.join(xml_string))
    file_object.close()


