# synthetic-image-generation

This is synthetic image generation to train machine learning models for the UH drone team.

In order to run:
    1) Install dependencies:
        python 3.6.2+, numpy, matplotlib, pillow, tqdm
    2) Unzip backgrounds in backgrounds folder
    3) cd into synthetic-image-generation folder with terminal
    4) python3 batch_data_generator.py


In the legacy folder, there's a jupyter notebook and matlab file that does almost the
same thing that batch_data_generator.py does.


A few tips:

How to update submodule:
    cd submodule_name
    git checkout master && git pull
    cd ..
    git add submodule_name
    git commit -m "updating submodule to latest"
    git push origin master


How to get rid of entire folders with git:
    git rm -r folder-name


How to add tracked items ONLY with git:
    git add -u


How to split video into images:
    ffmpeg -i 3.mp4 -vf fps= <# images/ # of seconds> out%d.png


Changing file names in bulk:
    Use file_renamer.py