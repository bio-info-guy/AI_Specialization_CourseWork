function [sx, sy, sWidth, sHeight] = auto_crop ( f )

%getting size of the input image
Ro = size(f,1);
Co = size(f,2);
img = f;
%% Crazy Amount of Filtering, Not much method, just try and luck
img2 = imgaussfilt3(img, 5, 'FilterSize',15);
level = graythresh(rgb2gray(img));
if level > 0.60
    img = im2single(imbinarize(img2, level));
end
if level <= 0.62
    img = im2single(imbinarize(img2)).*im2single(imbinarize(img2, 0.62));
end
img_gray = im2single(rgb2gray(img2)).*rgb2gray(im2single(img));
edges = edge(img_gray,'canny', [], 0.01);
edges = stdfilt(edges, ones(15));
edges = medfilt2(edges);
final = imfill(edges, 'holes');
final = im2single(imbinarize(final));% final should be a binary image where the document is 1 and everywhere else is 0

%figure
%imshowpair(f,bw,'montage')
%% Find Edges by assuming the document is at centered in the picture and filtering was good enough
r = Ro / 2;
c = Co / 2;
sy_mark = 0; % var indicating a good top edge posiiton has been found
sx_mark = 0; % var indicating a good left edge position has been found
sWidthmark = 0; % var indicating a good width (right edge) has been found
sHeightmark = 0;% var indicating a good height (bottom edge) has been found
vec_size = 30; % size of vector to find position of edge
vert = zeros(vec_size,1); % vector of zeros to find top & bottom edge
hori = zeros(1, vec_size); % vector of zeros to find right & left edge

for x = c : -1 : 20 % start from center and go left until vector is all zero
    if final(r,x-15:1:x+14) == hori
        sx = x+ vec_size;
        sWidth = Co - 2*sx;
        if c - x > 50 && x > 25 % a good edge is away from the center but also slightly away from side of image
            sx_mark = 1;
        end
        break;
    end
end

for x = c : 1 : Co-20 % find right edge and assign width
    if final(r, x-15:1:x+14) == hori
        if x - c > 50 && Co - x > 25 % a good edge is away from the center but also slightly away from side of image
            sWidthmark = 1;
        end
        if sx_mark == 1 
            sWidth = x - (sx + vec_size); % assign width using left edge for now
            break;
        end
        sx = Co - x + vec_size; % if no good left edge is found, then use symmetry
        sWidth = x - (sx + vec_size);
        break;
    end
end

for y = r : -1 : 20  % start from center and go up until vector is all zero
    if final (y-15:1:y+14,c) == vert  
        sy = y+vec_size;
        sHeight = Ro - 2*sy;
        if r - y > 50 && y > 25 % a good edge is away from the center but also slightly away from side of image
            sy_mark = 1;
        end
        break;
    end
end



for y = r : 1 : Ro-20  % find bottom edge and assign height
    if final(y-15:1:y+14,c) == vert
        if y - r > 50 && Ro - y > 25 % a good edge is away from the center but also slightly away from side of image
            sHeightmark = 1;
        end
        if sy_mark == 1
            sHeight = y - (sy + vec_size);
            break;
        end
        sy = Ro - y+vec_size; % use symmetry to find top if no good top was found
        sHeight = y - (sy + vec_size);
        break;
    end
end


%% if right or bottom edges are not good enough, but a top and left edges are found then assume document is centered
if sWidthmark == 0 && sx_mark == 1
    sWidth = Co - 2*sx;
end
if sHeightmark == 0 && sy_mark == 1
    sHeight = Ro - 2*sy;
end

%% Worse Cases in which no corresponding edges are found 
if sHeightmark == 0 && sy_mark == 0 % if no top and bottom found use center 60% of image height
    sy = floor(Ro*0.2);
    sHeight = floor(Ro*0.6);
end
if sWidthmark == 0 && sx_mark == 0 % if no left and right found use center 60% of image width
    sx = floor(Co*0.2);
    sWidth = floor(Co*0.6);
end 
%% Worst Worst case, found document too small then simply use center 60% of image
area = sWidth*sHeight/(Ro*Co);
if area < 0.1
    sy = floor(Ro*0.2);
    sHeight = floor(Ro*0.6);
    sx = floor(Co*0.2);
    sWidth = floor(Co*0.6);
end
%fprintf ( 'sx: %.0f sy: %.0f W: %.0f H: %.0f A: %.04f\n', sx, sy, sWidth, sHeight, area);
