# synthetic-image-generation

This is synthetic image generation to train machine learning models for the UH drone team.<br />

In order to run: <br />
    1) Install dependencies: <br />
        python 3.6.2+, numpy, matplotlib, pillow, tqdm <br />
    2) Unzip backgrounds from https://drive.google.com/file/d/18enPCV9VU2c9fEIRByIQA99x_6gbzIzB/view?usp=sharing <br />
    3) cd into synthetic-image-generation folder with terminal <br />
    4) python3 batch_data_generator.py <br />


In the legacy folder, there's a jupyter notebook and matlab file that does almost the
same thing that batch_data_generator.py does. <br />


A few tips: <br />
<br />
How to update submodule: <br />
    cd submodule_name <br />
    git checkout master && git pull<br />
    cd ..<br />
    git add submodule_name<br />
    git commit -m "updating submodule to latest"<br />
    git push origin master<br />


How to get rid of entire folders with git:<br />
    git rm -r folder-name<br />


How to add tracked items ONLY with git:<br />
    git add -u<br />


How to split video into images:<br />
    ffmpeg -i 3.mp4 -vf fps= <# images/ # of seconds> out%d.png<br />


Changing file names in bulk:<br />
    Use file_renamer.py<br />
