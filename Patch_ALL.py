import cv2
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
import csv
import os
path_annotation = '/home/dasgupta/ICE/'
path_img = '/home/dasgupta/ICE/OATRC_'
path_DISP = '/home/dasgupta/ICE/OATRC'

krn_size = 9
n=[]
n_nmi=[]
for filename in os.listdir(path_annotation):
	if filename.endswith('.csv'):
		pth_csv = os.path.join(path_annotation, filename)
		img_num = ''
		for char in filename.rsplit('.')[0]:
			if char.isdigit():
				img_num += char

		path_name_left = path_img + 'L_Rect' + str((img_num)) + '.jpg'
		path_name_right = path_img + 'R_Rect' + str((img_num)) + '.jpg'
		pth_SAD = path_DISP + str((img_num)) + 'SAD_Disp' + '.jpg'
		pth_BlM = path_DISP + str((img_num)) + 'BlM_Disp' + '.jpg'
		pth_SBM = path_DISP + str((img_num)) + 'SBM_Disp' + '.jpg'
		pth_GCS = path_DISP + str((img_num)) + 'GCS_Disp' + '.jpg'


		imageL = cv2.imread(path_name_left,0)
		imageR = cv2.imread(path_name_right,0)
		imageSAD = cv2.imread(pth_SAD,0)
		imageBlM = cv2.imread(pth_BlM,0)
		imageGCS = cv2.imread(pth_GCS,0)
		imageSBM = cv2.imread(pth_SBM,0)

		print(img_num)

		print(imageL.shape)

		with open(pth_csv) as csvfile:
			reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
			i = 0

			for row in reader: # each row is a list

				patch_centerL = np.array([row[0], row[1]])
				patch_centerR = np.array([row[2], row[3]])

				#Getting the Center Values (x,y) for L & R images from MatchPts
				#Then forming a 9x9 window across that center pt from L & R images
				krn_xL = int(patch_centerL[0] - krn_size / 2)
				krn_yL = int(patch_centerL[1] - krn_size / 2)
				patchL = imageL[krn_xL:krn_xL+krn_size, krn_yL:krn_yL+krn_size]

				krn_xR = int(patch_centerR[0] - krn_size / 2)
				krn_yR = int(patch_centerR[1] - krn_size / 2)
				patchR = imageR[krn_xR:krn_xR+krn_size, krn_yR:krn_yR+krn_size]

				#print(krn_xL,patch_centerL[0],patchL)

				if (patchR.shape == patchL.shape):
					patchDiff = np.subtract(patchL, patchR)
					patchMean =  np.mean(patchDiff)
					MI = nmi(np.reshape(patchR, np.product(patchR.shape)),np.reshape(patchL, np.product(patchL.shape)))
					#print(MI)
					if (patchDiff.size>0):
						key = img_num + '_' + str(i)
						i+=1
						#print('Key:',key)
						n.append(patchMean)
						x = int(patch_centerL[0])
						y =  int(patch_centerL[1])
						#print(imageSAD[x,y],imageBlM[x,y],imageSBM[x,y],imageGCS[x,y])
						if MI is not None and x <= imageSAD.shape[0] and x <= imageBlM.shape[0] and x <= imageSBM.shape[0] and y <= imageSAD.shape[1] and y <= imageBlM.shape[1] and y <= imageSBM.shape[1]:
							n_nmi.append([key,row[0],row[1],abs(row[0] - row[2]), MI,imageSAD[x,y],imageBlM[x,y],imageSBM[x,y],imageGCS[x,y]],dtype='U4, float32, float32, float32, float32, float32, float32, float32, float32')

	#print(len(n))

n = np.stack(n, axis=0 )
n_nmi = np.stack(n_nmi, axis=0 )
print(type(n_nmi))
print(n_nmi.shape)

print("Final size:" , len(n))
#print("kernel size:" , krn_size)
patch_name = 'patch' + str((krn_size))
patch_name_nmi = 'patch_nmi' + str((krn_size))

np.save(patch_name, n)
np.save(patch_name_nmi, n_nmi)
np.savetxt('NMI9.csv',n_nmi,delimiter=',')
