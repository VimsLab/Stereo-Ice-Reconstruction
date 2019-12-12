# Produces Disparity maps for all images in the directory using BM and SGBM metric for user requested block size

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

path_annotation = '/home/dasgupta/ICE/'
path_img = '/home/dasgupta/ICE/OATRC_'

for filename in os.listdir(path_annotation):
	if filename.endswith('.csv'):
		pth_csv = os.path.join(path_annotation, filename)

		img_num = ''
		for char in filename.rsplit('.')[0]:
			if char.isdigit():
				img_num += char

		path_name_left = path_img + 'L_Rect' + str((img_num)) + '.jpg'
		path_name_right = path_img + 'R_Rect' + str((img_num)) + '.jpg'


		imageL = cv2.imread(path_name_left,0)
		imageR = cv2.imread(path_name_right,0)

		print(img_num)

		h,w = imageL.shape
		print('For image of size: ', h , 'x' , w)

	    # BM: Block Matching
		blockSize = 19
	    #for b_idx in range(len(blockSizes)):
		numDisparities=32
		print('computing BM disparity w blk size...'+ str(blockSize))
		stereo = cv2.StereoBM_create(numDisparities=numDisparities, blockSize=blockSize)
		disparity = stereo.compute(imageL, imageR)
		disparity = disparity/16.
		#plt.imshow(disparity) # ('gray')
		#plt.title('Block Matching Disparity Map, blocksize: ' + str(blockSize))
		#plt.colorbar()
		#plt.show()
		fname =  'OATRC' + str((img_num)) + 'BlM_Disp.jpg'
		fname2 = 'OATRC' + str((img_num)) + 'BlM_Disp.txt'
		np.savetxt(fname2, disparity, fmt="%4d", delimiter=",", newline="\n")
		cv2.imwrite(fname, 256*disparity/numDisparities) #for bw images

		# SGBM: Semi Global Block Matching
		#for b_idx in range(len(blockSizes)):
		stereo = cv2.StereoSGBM_create(minDisparity=-16,numDisparities=32, blockSize=blockSize)
		right_matcher = cv2.ximgproc.createRightMatcher(stereo)

	    # FILTER Parameters
		lmbda = 80000
		sigma = 1.2
		visual_multiplier = 1.0

		wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
		wls_filter.setLambda(lmbda)
		wls_filter.setSigmaColor(sigma)
		print('computing SGBM disparity w blk size...'+ str(blockSize))
		displ = stereo.compute(imageL, imageR)  # .astype(np.float32)/16
		dispr = right_matcher.compute(imageR, imageL)  # .astype(np.float32)/16
		displ = np.int16(displ)
		dispr = np.int16(dispr)
		filteredImg = wls_filter.filter(displ, imageL, None, dispr)
		filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
		filteredImg = filteredImg/16.
		filteredImg = np.uint8(filteredImg)
		#plt.imshow(filteredImg)
		#plt.title('Semi-Global Block Matching Disparity Map, blocksize: ' + str(blockSize))
		#plt.colorbar()
		#plt.show()
		fname =  'OATRC' + str((img_num)) + 'SBM_Disp.jpg'
		fname2 = 'OATRC' + str((img_num)) + 'SBM_Disp.txt'
		np.savetxt(fname2, filteredImg, fmt="%4d", delimiter=",", newline="\n")
		cv2.imwrite(fname, filteredImg) #produces bw
