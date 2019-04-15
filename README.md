# synthetic-image-generation

This is synthetic image generation to train machine learning models for the UH drone team.


How to update submodule:
    cd submodule_name
    git checkout master && git pull
    cd ..
    git add submodule_name
    git commit -m "updating submodule to latest"
    git push origin master


How to get rid of entire folders:
    git rm -r folder-name


How to add tracked items ONLY:
    git add -u


How to split video into images:
    ffmpeg -i 3.mp4 -vf fps= <# images/ # of seconds> out%d.png


Changing file names in bulk:
    Use file_renamer.py