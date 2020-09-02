# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017
Updated on Thu Nov 29 11:24 2017
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

rez = 2

gsize = z*rez-1
randomGuest = np.zeros((gsize,gsize))
guestRegion = np.array(np.random.uniform(-1, 1, (x,y)))
for i in xrange(0, x*rez-1, rez):
	for j in xrange(0, y*rez-1, rez):
		randomGuest[i,j] = guestRegion[i/rez,j/rez]
randomGuest = np.around(randomGuest, decimals=1)
#this evenly inter-disperses the guest charges into a zero-squared space of resolution, rez

hostsize = (m*rez-1+(z*rez-2)*2, n*rez-1+(z*rez-2)*2)
randomHost = np.zeros(hostsize)
hostRegion = np.array(np.random.uniform(-1, 1, (m,n)))
for i in xrange(0, m*rez, rez):
	for j in xrange(0, n*rez, rez):
		randomHost[i+z*2-2,j+z*2-2] = hostRegion[i/rez,j/rez]
randomHost = np.around(randomHost, decimals=1)
# this evenly places the host into a zero-squared space of resolution, rez,
# and includes a zero-border for scanning

spunGuestsFull = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
flipGuestsFull = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
spunGuestsHalf = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
flipGuestsHalf = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
spunGuests45 = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
flipGuests45 = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
# each are 4 square matrix arrays, holding the guests & flipped guests
# rotated by 45 or 90 degrees

fmapSpunFull = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapFlipFull = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapSpunHalf = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapFlipHalf = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapSpun45 = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
fmapFlip45 = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
# each are 4 square matrix arrays holding all net host-guest binding forces for a set of rotated guests

lminSF = np.array(np.zeros(4, dtype=np.float))
lmaxSF = np.array(np.zeros(4, dtype=np.float))
gminSF = np.amin(lminSF)
gmaxSF = np.amax(lmaxSF)#spun-full extrema
lminFF = np.array(np.zeros(4, dtype=np.float))
lmaxFF = np.array(np.zeros(4, dtype=np.float))
gminFF = np.amin(lminFF)
gmaxFF = np.amax(lmaxFF)#flip-full extrema
lminSH = np.array(np.zeros(4, dtype=np.float))
lmaxSH = np.array(np.zeros(4, dtype=np.float))
gminSH = np.amin(lminSH)
gmaxSH = np.amax(lmaxSH)#spun-half extrema
lminFH = np.array(np.zeros(4, dtype=np.float))
lmaxFH = np.array(np.zeros(4, dtype=np.float))
gminFH = np.amin(lminFH)
gmaxFH = np.amax(lmaxFH)#flip-half extrema
lminS45 = np.array(np.zeros(4, dtype=np.float))
lmaxS45 = np.array(np.zeros(4, dtype=np.float))
gminS45 = np.amin(lminS45)
gmaxS45 = np.amax(lmaxS45)#spun-45 extrema
lminF45 = np.array(np.zeros(4, dtype=np.float))
lmaxF45 = np.array(np.zeros(4, dtype=np.float))
gminF45 = np.amin(lminF45)
gmaxF45 = np.amax(lmaxF45)#flip-45 extrema
# to hold local and global extrema

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
#Guest [positions] of 0, 1, 2, 3 equal guest-forms rotated by 0, 90, 180, 270 degrees

def calcForceMap(gforms, mfmap, shift): #shift = 0 for full (on-top) interactions
	forcemap = mfmap                    #shift = 2 for half (inbetween) interactions
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
		lmin[f] = np.amin(forcemap[f])
		lmax[f] = np.amax(forcemap[f])
	gmin = np.amin(lmin)
	gmax = np.amax(lmax)
	for form in xrange(forms):
		rows = np.shape(forcemap[form])[0]
		cols = np.shape(forcemap[form])[1]
		for i in xrange(rows):
			for j in xrange(cols):
				xpos = float(i)
				ypos = float(j)
				if forcemap[form][i,j] == gmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a minimum of {} at position ({}, {})".format(gmin, xpos, ypos)
				if forcemap[form][i,j] == gmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a maximum of {} at position ({}, {})".format(gmax, xpos, ypos)
	mfmap = forcemap
	return mfmap

print
print np.around(hostRegion, decimals=1)
print 
print np.around(guestRegion, decimals=1)
print
print np.around(guestRegion[::-1], decimals=1)

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
