import numpy as np
#import sklearn
from sklearn.mixture import GaussianMixture as GMM

pth_patch = './patch_nmi9.npy'
patches = np.load(pth_patch)

patch=[]
x=[]
y=[]
d=[]
sad=[]
blm=[]
sbm=[]
gcs=[]

#Create LIST of the Mutual Information & other vars from oatch_nmi9.npy
#Take each element from patch_nmi & insert each of x,y,d, etc. into an array
for i in range(len(patches)):
    if patches[i][4] <= 1: #NMI needs to <=1
        x.append(patches[i][1])
        y.append(patches[i][2])
        d.append(patches[i][3])
        patch.append(patches[i][4])
        sad.append(patches[i][5])
        blm.append(patches[i][6])
        sbm.append(patches[i][7])
        gcs.append(patches[i][8])

#patch: <class 'numpy.ndarray'>; (16020,); need to reshape it to (16020,1)
#Create ndarray of the data from above lists
patch = np.stack(patch, axis=0 ).reshape(-1, 1)
x = np.stack(x, axis=0 ).reshape(-1, 1)
y = np.stack(y, axis=0 ).reshape(-1, 1)
d = np.stack(d, axis=0 ).reshape(-1, 1)
sad = np.stack(sad, axis=0 ).reshape(-1, 1)
blm = np.stack(blm, axis=0 ).reshape(-1, 1)
sbm = np.stack(sbm, axis=0 ).reshape(-1, 1)
gcs = np.stack(gcs, axis=0 ).reshape(-1, 1)

#lst = [x,y,d,sad,blm,sbm,gcs]
#for item in lst:
#   item = np.stack(item, axis=0 ).reshape(-1, 1)

gmm = GMM(
    n_components=3,
    max_iter=100000,
    tol=1e-10,
    covariance_type='full',
    random_state = 50,
).fit(patch)

#label: <class 'numpy.ndarray'>; (16020,); need to reshape it to (16020,1)
label  = gmm.predict(patch.reshape(-1,1))
label = label.reshape(-1, 1)

pat_lab =  np.column_stack((x,y,d,patch,label,sad,blm,sbm,gcs))

print(type(pat_lab))
print(pat_lab.shape)

np.save('Patch9_Lab', pat_lab)
np.savetxt('Patch_Labs.csv',pat_lab,delimiter=',')
