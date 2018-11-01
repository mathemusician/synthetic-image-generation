% Use tic,toc for timing

%% Step 1 - Getting user input and importing relevant data

shapeChoice = input('What shape would you like to generate an image for?\n', 's');

% Import relevant data and assign variables adhering to choice
shape = imread(['assets/shape_templates/', shapeChoice, '.png']);
settings = readtable('assets/settings.csv');
rowSetting = find(strcmp(settings{:,1}, shapeChoice));
fontSize = settings{rowSetting,2};
position = [settings{rowSetting,3}, settings{rowSetting,4}];

%% Step 2 - Color choices and other random number generation
% rgb1 is the color of the object
% rgb2 is the color of the alphanumeric

% Generate random non-black color for the object
rgb1 = 0;
rgb2 = 0;
loopFlag = 1; % Using flags because no do...while loops in MATLAB
while (loopFlag == 1) % ensuring random color is never too close to black
    rgb1 = randi([0,255],1,3); 
    if (rgb1(1) > 60 | rgb1(2) > 60 | rgb1(3) < 60)
        loopFlag = 0;
    end
end

% Generate random color that contrasts with object color
loopFlag = 1;
while(loopFlag == 1)
    rgb2 = randi([0,255],1,3);
    lab1 = rgb2lab(rgb1/255);
    lab2 = rgb2lab(rgb2/255);
    
    deltaE = sqrt(sum((lab1 - lab2) .^ 2));
    if (deltaE > 5)
        loopFlag = 0;
    end
end

% Generate random alphanumeric
aV = ['A':'Z', '0':'9']; % short for "Alphanumeric Vector"
alphanumeric = aV(randi(numel(aV)));

%% Step 3 - Image manipulation

% Change the object's color from black to random color
% (actually changes the entire image, but it's faster this way)
shape(:,:,1) = shape(:,:,1) + rgb1(1);
shape(:,:,2) = shape(:,:,2) + rgb1(2);
shape(:,:,3) = shape(:,:,3) + rgb1(3);

% Create masked image
red = shape(:,:,1);
green = shape(:,:,2);
blue = shape(:,:,3);
mask = ~(red == 255 & green == 255 & blue == 255); % Mask is logical: NOT whitespace
maskedShape = bsxfun(@times, shape, cast(mask, 'like', shape));

% Draw text on the image
modifiedShape = insertText(maskedShape, position, alphanumeric, ...
    'FontSize', fontSize, 'BoxOpacity', 0, 'AnchorPoint', 'Center', ...
    'Font', 'Arial', 'TextColor', rgb2);

% Display the shape
image(modifiedShape);

%% TODO
% export batches at a time