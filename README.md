# Sea Ice Reconstruction

**Requirements:**
  1. Matlab 2019
  2. Python 3.x
  3. pytorch 1.0.0, texttable, numpy, cv2
  4. SIFT package for Matlab from http://www.vlfeat.org/install-matlab.html
  
  
 **Data:**      
    
 Data is hosted here: http://vims.cis.udel.edu/psitres/psitres_db.php
 
 **Usage:**
      
 The entire workflow is described in the paper: https://github.com/VimsLab/Stereo-Ice-Reconstruction/blob/master/DISP9.pdf
 
 1. Download stereo image pairs from the repository 
 2. Get Rectification parameters by running the script: siftRectify_PARAMS.m
 3. Rectify the stereo image pair using the script: RECT_Images.m
 4. To generate ground truth for the stereo pair, run the script: getSIFTpts.m
 5. Run the scripts for estimating disparity maps (DISP*.m, DISP*.py)
 6. Estimate Mutual Information between stereo image pairs using: Patch_ALL.py
 7. Perform grouping of the patches extracted above, using Gaussian Mixture Model: Patch_GMM_Data.py
 8. Choose the best patch size and nuber of distributions by examining the output of above script
 9. Use the stereo algorithms to estimate the reconstruction of the groups according to previous output
 
 For reconstruction using the Neural Network, download weights from: https://drive.google.com/file/d/1BlH7IafX-X0A5kFPd50WkZXqxo0_gtoI/view?usp=sharing
 Then run:
 CUDA_VISIBLE_DEVICES=0,1 python DISP_NN.py --datapath ./data-mbtest/   --outdir ./mboutput --loadmodel ./weights/final-768px.tar  --testres 1 --clean 0.8 --max_disp -1
 
To train from scratch, download and extract training data in folder /d/. 
Then run: 
CUDA_VISIBLE_DEVICES=0,1 python DISP_Train.py --maxdisp 32 --batchsize 28 --database /d/ --logname log1 --savemodel /dir/  --epochs 10
 
 
**Parameters:**
        
testres: 1 is full resolution, and 0.5 is half resolution
max_disp: maximum disparity range to search
clean: threshold of cleaning. clean=0 means removing all the pixels.


 **Examples:**
                                                     
						               
	Left and Right Images from PSITRES
   <img src="Images/OATRC_07_LR_Montage.jpg" alt="LEFT-RIGHT"/>
    
	 	 
	Matched Features after Rectification (only 20 matches shown for illustration)	 
 <img src="Images/OATRC_Matched_Features07siParam.jpg" alt="Matched"/> 
 	
	       
	Disparity Map using GCS created from above input
  <img src="Images/OATRC07GCS_Disp.jpg" alt="Disparity-GCS"/> 
 	
	   
	       Histogram of Patch Similarity using Normalized Mutual Information.
	 Three regions per image are obtained using Gaussian Mixture Model on NMI scores of kernel pairs (9x9 size). 

  <img src="Images/Patch9_nmi_mod3.png" alt="Patch9_mod3"/> 
  	

         RMSE (Y-axis in pixels) error for each Algorithm by Group
	 
 <img src="Images/RMSE_T.png" alt="RMSE"/>
  	Result of applying stereo algorithms using above procedure
