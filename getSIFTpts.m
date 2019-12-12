function [MatchPts] = getSIFTpts( imleft,imright)
%This function gets MATCHING points from RECTIFIED image pair, using SIFT
%and geometric tx
%Outputs the (x,y) coordinates in an array;

%imleft = OATRC_L_Rect026;
%imright = OATRC_R_Rect026;
[r,c,ch]=size(imleft);
mask = ones(r,c);

if size(imleft,3)>1;
    grayleft = rgb2gray(imleft);
    grayright = rgb2gray(imright);
else
grayleft = imleft;
grayright = imright;
end
    [fa, da] = vl_sift(single(grayleft)) ;
    [fb, db] = vl_sift(single(grayright)) ;
    [matches, ~] = vl_ubcmatch(da, db) ;
    matchedPoints1 = fa(1:2, matches(1,:));
    matchedPoints2 = fb(1:2, matches(2,:));  
    for x = 1:size(matchedPoints1,2)
       ex = matchedPoints1(1,x);
       ey = matchedPoints1(2,x);
       approx = round([ex,ey]);
%            
%            disp('************************');
%            disp(x);
%            disp(approx(1));
%            disp(approx(2));
%            
       temp = mask(approx(2),approx(1));


       %disp(size(approx(1)));
       inmask(x) = temp;
    end
    invalid = find(~inmask);
    matchedPoints1(:,invalid) = [];
    matchedPoints2(:,invalid) = [];
    matchedPoints1 = matchedPoints1';%transpose
    matchedPoints2 = matchedPoints2';
%         disp(matchedPoints1);
    disp('Number of Matched Points:');
    disp(size(matchedPoints1));
    %uncomment these lines to show matching results
    showMatchedFeatures(imleft,imright,matchedPoints1(100:120,:),matchedPoints2(100:120,:),'montage');
    %pause(5);


    [tform,refinedPoints1,refinedPoints2] = estimateGeometricTransform(matchedPoints1,matchedPoints2, 'projective');
% [~, geometricInliers] = step(gte, matchedPoints1, matchedPoints2);
% refinedPoints1 = matchedPoints1(geometricInliers, :);
% refinedPoints2 = matchedPoints2(geometricInliers, :);
%remove outliers using epipolar constraint
[fMatrix, epipolarInliers, status] = estimateFundamentalMatrix(...
refinedPoints1, refinedPoints2, 'Method', 'RANSAC', ...
'NumTrials', 10000, 'DistanceThreshold', 0.3, 'Confidence', 97);
if status ~= 0 || isEpipoleInImage(fMatrix, size(grayleft)) ...
    || isEpipoleInImage(fMatrix', size(grayright))
error(['For the rectification to succeed, the images must have enough '...
    'corresponding points and the epipoles must be outside the images.']);
end
disp('Number of Refined Points:');
disp(size(refinedPoints1));
inlierPoints1 = refinedPoints1(epipolarInliers, :);
inlierPoints2 = refinedPoints2(epipolarInliers, :);
showMatchedFeatures(imleft,imright,inlierPoints1(1:end,:),inlierPoints2(1:end,:),'montage'); %(1:200:end,:)
pause(5);
disp('Number of Inlier Points:');
disp(size(inlierPoints1));
MatchPts = [inlierPoints1,inlierPoints2];

end
