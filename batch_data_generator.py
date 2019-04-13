'''
The purpose of this file is to use Python to make the images to train AI models with.

Dependencies: python 3.5+, numpy, matplotlib

Python is a bit more accessible than Matlab; therefore, this file will be better for
making training images in the long run.
'''


from PIL import Image
import matplotlib.pyplot as pltfrom os import listdir
from os.path import isfile, join

%matplotlib inline

# load necessary files
cwd = os.getcwd()
backgrounds_path = join(cwd, '/shape_templates')
backgrounds = [f for f in listdir(backgrounds_path) if isfile(join(mypath, f))]

shapes_path = join(cwd, 'assets', 'photoshop files')
shapes = [f for f in listdir(shapes_path) if isfile(join(mypath, f))]


# iterate over background images
alphanumeric_vector = ['A', 'B', 'C', 'D', 'E', 'F', \
                       'G', 'H', 'I', 'J', 'K', 'L', \
                       'M', 'N', 'O', 'P', 'Q', 'R', \
                       'S', 'T', 'U', 'V', 'W', 'X', \
                       'Y', 'Z', '1', '2', '3', '4', \
                       '5', '6', '7', '8', '9']


# create xml files



