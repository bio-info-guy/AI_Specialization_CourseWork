% Please edit this function only, and submit this Matlab file in a zip file 
% along with your PDF report
function [r,c] = i_spy ( object_im, big_im)
%object_im = Object image that needs to be detected
%big_im = Image in which detections needs to be done.

Ro = size(object_im, 1); 
Co = size(object_im, 2); 

Rb = size(big_im, 1); 
Cb = size(big_im, 2); 
% using single precision for faster calculations
object_im =  im2single(rgb2gray(object_im));
big_im = im2single(rgb2gray(big_im));
% using cross correlation to find point of best template match
C=normxcorr2(object_im, big_im);
[r, c] = find(C==max(C(:)));
r = r-Ro+1;
c = c-Co+1;
return;
% finding point of color which appears least common in big image
edges = unique(object_im);
counts = histc(big_im(:),edges);
[x,y] = find(object_im == edges(counts == min(counts)));
x = x(1);
y = y(1);
loss=10^9;
r=0;c=0;
k=0;
for i=1:(Rb-Ro+1)
    for j=1:(Cb-Co+1)
        k = k+1;
        new_loss = abs(big_im(i+x-1,j+y-1,1) - object_im(x,y,1));
        if (new_loss < loss)
            if(new_loss == 0)
                f_loss = sum(sum(abs(big_im(i:i+Ro-1,j:j+Co-1,:) - object_im)));
                if (f_loss == 0)
                    r = i;
                    c = j;
                    return;
                end
            end
        end
    end
end
return;
end
