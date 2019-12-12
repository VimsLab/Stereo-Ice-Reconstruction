imgOATRC_R60 = imread('./OATRC/20130821160000-cam12010988-1-13860-6506227_R.jpg');
imgOATRC_L60 = imread('./OATRC/20130821160000-cam12010990-0-13860-6506207_L.jpg');

[rect_params_ODEN60] = siftRectify( imgOATRC_L60,imgOATRC_R60,mask ); %  15,185; 10,005; 7,926;  
[OATRC_L_Rect60,OATRC_R_Rect60] = rectifyStereoImages(imgOATRC_L60,imgOATRC_R60,rect_params_ODEN60.tform1,rect_params_ODEN60.tform2); % done

imwrite(OATRC_L_Rect60,'OATRC_L_Rect60.png');
imwrite(OATRC_R_Rect60,'OATRC_R_Rect60.png');

figure;
imshow(OATRC_L_Rect60);
hold on;
figure;
imshow(OATRC_R_Rect60);
hold on;
