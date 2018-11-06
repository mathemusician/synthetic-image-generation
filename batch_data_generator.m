%% Made by Kyle and Jesse
% This generates synthetic images for training our machine learning
% algorithm
% available shapes are: circle, cross, heptagon, hexagon, octagon,
% pentagon, quarterCircle, rectangle, semiCircle, square, star, trapezoid,
% and triangle

clear all
%% Step 1 - Getting user input and import relevant data

% get background images
batchSize = 2;
background_imgs = getAllFiles('backgrounds/');


% Other constant varibles moved outside of for loop 
% (TODO - these should be all caps to follow convention?
aV = ['A':'Z', '0':'9']; % short for "Alphanumeric Vector"

%% Step 2 - The rest of the owl


shape_list = {'circle', 'cross', 'heptagon', 'hexagon', 'octagon', 'pentagon', ... 
          'quarterCircle', 'rectangle', 'semiCircle', 'square', 'star' ...
          'trapezoid', 'triangle'};

% i keeps track of the image names
i = 0;
% use this to add the end of for loop
size_background_imgs = size(background_imgs);


for cellIndex = 1:size_background_imgs(1) % iterate over background images
    backgroundImage = background_imgs(cellIndex);
    backgroundString = strjoin(backgroundImage);
    last_word = strsplit(backgroundString, '.');
    
    % check if images are jpeg
    if isempty(setdiff(last_word(end), {'DS_Store'})) == 1
        continue
    end
    
    for shapeChoice = shape_list % iterate over shapes
        % get important info for each shape
        baseShape = imread(['assets/shape_templates/', strjoin(shapeChoice), '.png']);
        % settings = readtable('assets/settings.csv');
        fid = fopen('assets/settings.csv');
        settings = textscan(fid, '%s%s%s%s', 'Delimiter', ',');
        fclose(fid);
        rowSetting = find(strcmp(settings{1}, shapeChoice));
        fontSize = str2num(settings{2}{rowSetting});
        position = [str2num(settings{3}{rowSetting}), str2num(settings{4}{rowSetting})];

        % Get coordinates for black pixels by selecting non-white pixels
        logic_mask = baseShape(:,:,1)~=255 | baseShape(:,:,2)~=255 | baseShape(:,:,3)~=255;
        [x_cor, y_cor] = find(logic_mask);

        rgb1 = [0, 0, 0];
        rgb2 = [0, 0, 0];

        for rand_var=1:batchSize
            % Generate random non-black color for the object
            rgb1(1) = randi([60,255],1);
            rgb1(2) = randi([60,255],1);
            rgb1(3) = randi([0, 60],1);

            % Generate random color that contrasts with object color
            loopFlag = 1;
            while(loopFlag == 1)
                rgb2 = randi([0,255],1,3);
                lab1 = rgb2lab(rgb1/255);
                lab2 = rgb2lab(rgb2/255);

                deltaE = sqrt(sum((lab1 - lab2) .^ 2));
                if (deltaE > 7) % contrast lower bound
                    loopFlag = 0;
                end
            end

            % Generate random alphanumeric
            alphanumeric = aV(randi(numel(aV)));


            % Change the entire image from black to another color
            clear shape
            shape(:,:,1) = baseShape(:,:,1) + rgb1(1);
            shape(:,:,2) = baseShape(:,:,2) + rgb1(2);
            shape(:,:,3) = baseShape(:,:,3) + rgb1(3);

            % Apply mask
            maskedShape = bsxfun(@times, shape, cast(~logic_mask, 'like', shape));

            % Draw and rasterize alphanumeric on the image
            modifiedShape = insertText(maskedShape, position, alphanumeric, ...
                'FontSize', fontSize, 'BoxOpacity', 0, 'AnchorPoint', 'Center', ...
                'Font', 'Arial', 'TextColor', rgb2);

            % get background image (I call it little_cat)
            shape = modifiedShape;
            little_cat = imread(backgroundString);
            size_cat = size(little_cat);
            size_shape = size(shape);
            x_max = size_cat(1) - size_shape(1);
            y_max = size_cat(2) - size_shape(2);

            % find maximum x and y translations
            change_x = randi([0 x_max],1);
            change_y = randi([0 y_max],1);
            x_tr = x_cor + change_x;
            y_tr = y_cor + change_y;

            size_x_cor = size(x_cor);
            for n = 1:size_x_cor(1)
                little_cat(x_tr(n), y_tr(n), :) = shape(x_cor(n), y_cor(n), :);
            end

            % Write the image as lossless jpg
            i = i + 1;
            imwrite(little_cat, ['test_images/', num2str(i),'.jpg'], 'jpg', 'Quality', 100.0);
            
            
            % MAKE XML FILE USING BRUTE FORCE
            folder = 'test_images';
            filename = [num2str(i),'.jpg'];
            path = [pwd, folder];
            height = 40; % this is something that's known
            width = 40;
            depth = 3;
            xmin = change_y; % I'm not sure why it works when it's switched
            xmax = change_y + 40; % but it does...
            ymin = change_x;
            ymax = change_x + 40;
            xml_string = ['<annotation verified="yes">\n', ...
                        '\t<folder>' folder '</folder>\n', ...
                        '\t<filename>' filename '</filename>\n' ...
                        '\t<path>' path '</path>\n' ...
                        '\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n' ...
                        '\t<size>' newline ...
                        '\t\t<width>' int2str(width) '</width>' newline ...
                        '\t\t<height>' int2str(height) '</height>' newline ...
                        '\t\t<depth>' int2str(depth) '</depth>' newline ...
                        '\t</size>\n' ...
                        '\t<segmented>0</segmented>\n' ...
                        '\t<object>' newline ...
                        '\t\t<name>' strjoin(shapeChoice) '</name>' newline, ...
                        '\t\t<pose>Unspecified</pose>' newline, ...
                        '\t\t<truncated>0</truncated>' newline, ...
                        '\t\t<difficult>0</difficult>' newline, ...
                        '\t\t<bndbox>' newline ...
                        '\t\t\t<xmin>' int2str(xmin) '</xmin>' newline ...
                        '\t\t\t<ymin>' int2str(ymin) '</ymin>' newline ...
                        '\t\t\t<xmax>' int2str(xmax) '</xmax>' newline ...
                        '\t\t\t<ymax>' int2str(ymax) '</ymax>' newline ...
                        '\t\t</bndbox>' newline ...
                        '\t</object>\n' ...
                        '</annotation>\n'];
            xml_name = [num2str(i) '.xml'];
            xml_path = [folder '/' xml_name];
            fileID = fopen(xml_path,'w');
            fprintf(fileID, xml_string);
            fclose(fileID);
        end
    end
end

function fileList = getAllFiles(dirName) % I grabbed this from the internet

  dirData = dir(dirName);      % Get the data for the current directory
  dirIndex = [dirData.isdir];  % Find the index for directories
  fileList = {dirData(~dirIndex).name}';  % Get a list of the files
  if ~isempty(fileList)
    fileList = cellfun(@(x) fullfile(dirName,x),...  % Prepend path to files
                       fileList,'UniformOutput',false);
  end
  subDirs = {dirData(dirIndex).name};  % Get a list of the subdirectories
  validIndex = ~ismember(subDirs,{'.','..'});  % Find index of subdirectories
                                               %   that are not '.' or '..'
  for iDir = find(validIndex)                  % Loop over valid subdirectories
    nextDir = fullfile(dirName,subDirs{iDir});    % Get the subdirectory path
    fileList = [fileList; getAllFiles(nextDir)];  % Recursively call getAllFiles
  end

end
