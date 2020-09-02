# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017
Updated on Thu Nov 30 02:24 2017
@author: MJL
"""
import numpy as np
from copy import deepcopy

m = int(raw_input("Enter number of rows for host: "))
n = int(raw_input("Enter number of columns for host: "))

x = int(raw_input("Enter number of rows for guest: "))
y = int(raw_input("Enter number of columns for guest: "))

rez = int(raw_input("Enter resolution for calculations (1 = low; 8 = high): "))*2

if rez <1 or rez > 8:
	rez = int(raw_input("Re-enter resolution between 1 = low and 8 = high: "))*2

if m*n<x*y:
	print '\nHost size is too small for guest.\nHost will be treated as the guest.'
	xcopy = x
	ycopy = y
	x = deepcopy(m)
	y = deepcopy(n)
	m = deepcopy(xcopy)
	n = deepcopy(ycopy)
if x >= y:
	z = x
else:
	z = y

time = float(m*n)
print '\nThis may take around {} min(s) to complete an iPad A7 processor.'.format('{0:.2f}'.format(time/120000+(m+n)/600))

rez = 4

gsize = z*rez-rez+1
randomGuest = np.zeros((gsize,gsize))
guestRegion = np.array(np.random.uniform(-1, 1, (x,y)))
for i in xrange(0, x*rez-rez+1, rez):
	for j in xrange(0, y*rez-rez+1, rez):
		randomGuest[i,j] = guestRegion[i/rez,j/rez]
		randomGuest = np.around(randomGuest, decimals=1)
# this evenly inter-disperses the guest charges into a zero-squared space of
# resolution, rez, so that rotated guests can be positioned in same the space

guestSpun45 = np.array(np.zeros((gsize,gsize)))
for i in xrange(0,gsize,rez):
	for j in xrange(0,gsize,rez):
		guestSpun45[(i+j)/2,(j-i)/2+(z-1)*rez/2] = randomGuest[i,j]
#this rotates the guest to a 45 degree form, appropriate for host binding

hostsize = (m*rez-rez+1+(z*rez-rez)*2, n*rez-rez+1+(z*rez-rez)*2)
randomHost = np.zeros(hostsize)
hostRegion = np.array(np.random.uniform(-1, 1, (m,n)))
for i in xrange(0, m*rez, rez):
	for j in xrange(0, n*rez, rez):
		randomHost[i+z*rez-rez,j+z*rez-rez] = hostRegion[i/rez,j/rez]
		randomHost = np.around(randomHost, decimals=1)
# this evenly places the host into a zero-squared space of resolution, rez,
# and includes a zero-border for scanning purposes for the rotated guests

spunGuestsFull = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
flipGuestsFull = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
spunGuestsHalf = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
flipGuestsHalf = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
spunGuests45 = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
flipGuests45 = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
# each are 4 square matrix arrays, holding the guests & flipped guests,
# which are rotated in increments of 45 and/or 90 degrees

fmapSpunFull = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapFlipFull = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapSpunHalf = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapFlipHalf = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapSpun45 = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapFlip45 = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
# each are 4 square matrix arrays holding all net host-guest binding forces
# for a set of rotated guests, so that extrema can be found

lminSF = np.array((np.zeros((4,3), dtype=np.float)))
lmaxSF = np.array(np.zeros((4,3), dtype=np.float))
gminSF = 0
gmaxSF = 0#spun-full extrema
lminFF = np.array(np.zeros((4,3), dtype=np.float))
lmaxFF = np.array(np.zeros((4,3), dtype=np.float))
gminFF = 0
gmaxFF = 0#flip-full extrema
lminSH = np.array(np.zeros((4,3), dtype=np.float))
lmaxSH = np.array(np.zeros((4,3), dtype=np.float))
gminSH = 0
gmaxSH = 0#spun-half extrema
lminFH = np.array(np.zeros((4,3), dtype=np.float))
lmaxFH = np.array(np.zeros((4,3), dtype=np.float))
gminFH = 0
gmaxFH = 0#flip-half extrema
lminS45 = np.array(np.zeros((4,3), dtype=np.float))
lmaxS45 = np.array(np.zeros((4,3), dtype=np.float))
gminS45 = 0
gmaxS45 = 0#spun-45 extrema
lminF45 = np.array(np.zeros((4,3), dtype=np.float))
lmaxF45 = np.array(np.zeros((4,3), dtype=np.float))
gminF45 = 0
gmaxF45 = 0#flip-45 extrema
# output variables to hold local and global extrema

def guestForms(guest, spunforms, flipforms):
	spunforms[0] = guest
	flipforms[1] = spunforms[0].transpose()
	spunforms[3] = flipforms[1][::-1]
	flipforms[2] = spunforms[3].transpose()
	spunforms[2] = flipforms[2][::-1]
	flipforms[3] = spunforms[2].transpose()
	spunforms[1] = flipforms[3][::-1]
	flipforms[0] = spunforms[1].transpose()
	return
#Guest [positions] of 0, 1, 2, 3 equal guest-forms rotated by 0, 90, 180, 270
#degrees; if a 45 deg. form is inputed, then 135, 225, 315 forms are ouputed

#def guestSpun45(spun0):
#	guest = spun0
#	for i in xrange(0,gsize,2):
#		for j in xrange(0,gsize,2):
#			guestSpun45[i/2+j/2,j/2-i/2+2] = guest[i,j]
#	return

def calcForceMap(gforms, mfmap, shift): #shift = 0 for full (on-top) shifts
	forcemap = mfmap 											#shift = 2 for half (inbetween) shifts
	forms = np.shape(gforms)[0]
	for form in xrange(forms):
		row = np.shape(gforms[form])[0]
		col = np.shape(gforms[form])[1]
		xmap = np.shape(mfmap[form])[0]
		ymap = np.shape(mfmap[form])[1]
		if shift == 0:
			for i in xrange(xmap):
				for j in xrange(ymap):
						forcemap[form][i,j] = np.sum(gforms[form] *
						randomHost[i*rez:i*rez+row,j*rez:j*rez+col])
		if shift == 1:
			for i in xrange(xmap-rez):
				for j in xrange(ymap-rez):
					upleft = forcemap[form][i,j]/2
					downleft = forcemap[form][i+rez,j]/2
					upright = forcemap[form][i,j+rez]/2
					downright = forcemap[form][i+rez,j+rez]/2
					if i % rez == 0 and j % rez == 1:
						mfmap[form][i,j] = upleft + upright
					if i % rez == 1 and j % rez == 0:
						mfmap[form][i,j] = upleft + downleft
					if i % rez == 1 and j % rez == 1:
						forcemap[form][i,j] = upleft + downleft + upright + downright
	mfmap = forcemap
	return mfmap

def findExtrema(mfmap, lmin, lmax, gmin, gmax, text):
	forms = np.shape(mfmap)[0]
	forcemap = mfmap
	for f in xrange(forms):
		lmin[f,0] = np.amin(forcemap[f])
		lmax[f,0] = np.amax(forcemap[f])
	gmin = deepcopy(np.amin(lmin[:,0]))
	gmax = deepcopy(np.amax(lmax[:,0]))
	for form in xrange(forms):
		rows = np.shape(forcemap[form])[0]
		cols = np.shape(forcemap[form])[1]
		for i in xrange(rows):
			for j in xrange(cols):
				xpos = i-z+1
				ypos = j-z+1
				if forcemap[form][i,j] == lmin[form,0]:
					lmin[form,1] = xpos
					lmin[form,2] = ypos
				if forcemap[form][i,j] == lmax[form,0]:
					lmax[form,1] = xpos
					lmax[form,2] = ypos
				if forcemap[form][i,j] == gmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a global minimum of {} at position ({}, {})".format(gmin, xpos, ypos)	
				if forcemap[form][i,j] == gmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a global maximum of {} at position ({}, {})".format(gmax, xpos, ypos)
	print "\nLocal minima & maxima for {} guest are:".format(text)
	print lmin
	print
	print lmax
	mfmap = forcemap
	return mfmap

print
print np.around(hostRegion, decimals=1)
print 
print np.around(guestRegion, decimals=1)
print
print np.around(guestRegion[::-1], decimals=1)
print
print np.around(guestSpun45, decimals=1)

guestForms(randomGuest,spunGuestsFull,flipGuestsFull)

calcForceMap(spunGuestsFull,fmapSpunFull, 0)
findExtrema(fmapSpunFull,lminSF,lmaxSF,gminSF,gmaxSF,'the random')

calcForceMap(flipGuestsFull,fmapFlipFull, 0)
findExtrema(fmapFlipFull,lminFF,lmaxFF,gminFF,gmaxFF,'the random flipped')



#halfShifts(spunGuestsHalf,fmapSpunHalf)
#findExtrema('the half-shifted')
"""
import scipy.ndimage as nd
guestRotate45 = nd.rotate(randomGuest, 45, order=1)
guestRotate45 = np.around(guestRotate45, decimals=1)

hostRotate45 = nd.rotate(randomHost, 45, reshape=False, order=1)
hostRotate45 = np.around(hostRotate45, decimals=1)
"""
"""
# Function to rotate a matrix
def rotateMatrix(mat):
 
    if not len(mat):
        return
     
    
        #top : starting row index
        #bottom : ending row index
        #left : starting column index
        #right : ending column index
    
 
    top = 0
    bottom = len(mat)-1
 
    left = 0
    right = len(mat[0])-1
 
    while left < right and top < bottom:
 
        # Store the first element of next row,
        # this element will replace first element of
        # current row
        prev = mat[top+1][left]
 
        # Move elements of top row one step right
        for i in range(left, right+1):
            curr = mat[top][i]
            mat[top][i] = prev
            prev = curr
 
        top += 1
 
        # Move elements of rightmost column one step downwards
        for i in range(top, bottom+1):
            curr = mat[i][right]
            mat[i][right] = prev
            prev = curr
 
        right -= 1
 
        # Move elements of bottom row one step left
        for i in range(right, left-1, -1):
            curr = mat[bottom][i]
            mat[bottom][i] = prev
            prev = curr
 
        bottom -= 1
 
        # Move elements of leftmost column one step upwards
        for i in range(bottom, top-1, -1):
            curr = mat[i][left]
            mat[i][left] = prev
            prev = curr
 
        left += 1
 
    return mat
"""
