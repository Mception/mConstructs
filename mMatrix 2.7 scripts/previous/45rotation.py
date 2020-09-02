import numpy as np
from copy import deepcopy

msize = 6
mMatrix = np.arange(msize*msize).reshape((msize,msize))
mSpun45 = np.array(np.zeros((msize,msize)))

def m45(molIn,mol45): # rotates molecule by 45 deg (keeping values unchanged)
	msize = np.shape(molIn)[0]
	cNum = msize/2
	for c in xrange(cNum):
		size = msize-c
		shift = cNum-c
		mol45[c,c+shift:size] = molIn[c,c:size-shift] #top row right
		mol45[c+shift:size,size-1] = molIn[c:size-shift,size-1] #right col down
		mol45[size-1,c:size-shift] = molIn[size-1,c+shift:size] #bottom row left
		mol45[c:size-shift,c] = molIn[c+shift:size,c] #left col up
		if shift > 1:
			mol45[c+1:c+shift,size-1] = molIn[c,size-shift:size-1]
			mol45[size-1,size-shift:size-1] = molIn[size-shift:size-1,size-1][::-1]
			mol45[size-shift:size-1,c] = molIn[size-1,c+1:c+shift]
			mol45[c,c+1:c+shift] = molIn[c+1:c+shift,c][::-1]
		if c == cNum-1 and msize%2 == 1:
			mol45[cNum,cNum] = molIn[cNum,cNum]
	return 

m45(mMatrix,mSpun45)

print mMatrix
print
print mSpun45.astype(int)

