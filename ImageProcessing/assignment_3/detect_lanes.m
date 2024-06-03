function [rho1, theta1, rho2, theta2] = detect_lanes (img)
    %% First Filter image using Gaussian filter and a polugon mask to only select ROI
    height  = size(img,1);
    width  = size(img,2);
    img = im2single(imbinarize(img, 0.6)).*im2single(img);
    bim = rgb2gray(img);
    bim = imgaussfilt(bim);
    ROI_x = [0.27*width; 0.46*width; 0.52*width; 0.73*width];  % Region of Interest X coordinates
    ROI_y= [0.65*height ;0.4*height; 0.4*height; 0.65*height];  % Region of Interest Y coordinates
    mask = poly2mask(ROI_x,ROI_y,height,width);  % Create a mask for ROI
    bim = imbinarize(bim, 0.55);

    %% After Preprocessing look for edges in the image using Canny method and find lines using Hough transform
    img_edges = edge(bim, 'canny');
    img_edges(~mask)= 0;
    bwareaopen(img_edges, 50);
    [H,theta,rho]=hough(img_edges);
    p=houghpeaks(H,10,'threshold',ceil(0.1*max(H(:))));
    lines = houghlines(img_edges,theta,rho,p,'FillGap',20,'MinLength',40);
    
    %% Set initial estiamtes for the theta and rhos
    theta1 = -2.56;
    rho1 = -365;
    theta2 = -.68;
    rho2 = 138;
    theta1_ = -2.56;
    rho1_ = -365;
    theta2_ = -.69;
    rho2_ = 136;
    
    %% start looking for lines that may match the two lanes
    % Find left lane first
    max_len = 0;
    maxind = 1;
    err = 0.1;
    for k = 1:length(lines)
        len = norm(lines(k).point1 - lines(k).point2);
        new_err = abs(theta1_ - lines(k).theta*(pi/180)+pi);
        if (len > max_len && lines(k).theta > 0 && new_err < err)
          maxind = k;
          max_len = len;
          err = new_err;
        end
    end
    if ~isempty(lines)
        if (lines(maxind).theta > 0 && err < 0.21)
            theta1 = lines(maxind).theta*(pi/180)-pi;
            rho1 = -lines(maxind).rho;
        end
    end
    %find right lane
    max_len = 0;
    second_ind = 1;
    err = 0.16;
    for k = 1:length(lines)
        len = norm(lines(k).point1 - lines(k).point2);
        new_err = abs(theta2_ - lines(k).theta*(pi/180));
        if (len > max_len && lines(k).theta < 0 && new_err < err)
            second_ind = k;
            max_len = len;
            err = new_err;
        end
    end
    if ~isempty(lines)
        if (lines(second_ind).theta < 0 && err < 0.25)
            theta2 = lines(second_ind).theta*(pi/180);
            rho2 = lines(second_ind).rho;
        end
    end
    %% Error correction: use initial estimates if the lines that were found are too extreme 
    if theta2 < -.89 || theta2 > -0.49
        theta2 = theta2_;
        rho2 = rho2_;
    end
    if theta1 > -2.32 || theta1 < -2.8
        theta1 = theta1_;
        rho1 = rho1_;
    end
    if(rho1 > 0)
        rho1 = -rho1;
    end
    if(rho2 < 0)
        rho2 = -rho2;
    end
    
end