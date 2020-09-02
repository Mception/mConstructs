# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017
Updated on Wed Nov 28 20:52 2017
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

rez = 2

time = float(m*n)
print '\nThis may take around {} min(s) to completion an iPad A7 processor.'.format('{0:.2f}'.format(time/120000+(m+n)/600))

guestsize = (z*rez-1, z*rez-1)
randomGuest = np.zeros(guestsize)
guestRegion = np.array(np.random.uniform(-1, 1, (x,y)))
for i in xrange(0, x*rez-1, rez):
	for j in xrange(0, y*rez-1, rez):
		randomGuest[i,j] = guestRegion[i/rez,j/rez]
randomGuest = np.around(randomGuest, decimals=1)
#this evenly inter-disperses the guest charges into a zero-space of resolution, rez

hostsize = (m*rez-1+(z*rez-2)*2, n*rez-1+(z*rez-2)*2)
randomHost = np.zeros(hostsize)
hostRegion = np.array(np.random.uniform(-1, 1, (m,n)))
for i in xrange(0, m*rez, rez):
	for j in xrange(0, n*rez, rez):
		randomHost[i+z*2-2,j+z*2-2] = hostRegion[i/rez,j/rez]
randomHost = np.around(randomHost, decimals=1)
##this evenly places the host into a zero-space of resolution, rez, and includes a zero-border for scanning

spunGuests = np.array((np.zeros(guestsize), np.zeros(guestsize),
											np.zeros(guestsize), np.zeros(guestsize)))
flipGuests = np.array((np.zeros(guestsize), np.zeros(guestsize),
											np.zeros(guestsize), np.zeros(guestsize)))
# alternating four (x by y) / (y by x) matrix arrays to hold the guests & flipped guests rotated by 0, 90, 180, & 270 deg.

mforceMap = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
#if x<>y:
#	mforceMap = (mforceMap[0], np.zeros((m+y-1,n+x-1), dtype=np.float),
#							mforceMap[2], np.zeros((m+y-1,n+x-1), dtype=np.float))
#a four (row, col) or alternating (col, row) matrix holding all net host-binding forces for a guest rotated by 0, 90, 180, & 270 deg.

lmin = np.array(np.zeros(4, dtype=np.float))
lmax = np.array(np.zeros(4, dtype=np.float))
gmin = np.amin(lmin)
gmax = np.amax(lmax)
#defining local and global extrema

def guestForms(guest):
	spunGuests[0] = guest
	flipGuests[1] = spunGuests[0].transpose()
	spunGuests[3] = flipGuests[1][::-1]
	flipGuests[2] = spunGuests[3].transpose()
	spunGuests[2] = flipGuests[2][::-1]
	flipGuests[3] = spunGuests[2].transpose()
	spunGuests[1] = flipGuests[3][::-1]
	flipGuests[0] = spunGuests[1].transpose()
	return
#Guest [positions] of 0, 1, 2, 3 equal the guest-forms rotated by 0, 90, 180, 270 degrees

def calcForceMap(gforms):
	forms = np.shape(gforms)[0]
	for form in xrange(forms):
		row = np.shape(gforms[form])[0]
		col = np.shape(gforms[form])[1]
		xmap = np.shape(mforceMap[form])[0]
		ymap = np.shape(mforceMap[form])[1]
		for i in xrange(xmap):
			for j in xrange(ymap):
				mforceMap[form][i,j] = np.sum(gforms[form] *
				randomHost[i*rez:i*rez+row,j*rez:j*rez+col])
# for i in xrange(xmap-rez):
#	for j in xrange(ymap-rez):
#	upleft = mforceMap[form][i,j]/2
#	downleft = mforceMap[form][i+rez,j]/2
#	upright = mforceMap[form][i,j+rez]/2
#	downright = mforceMap[form][i+rez,j+rez]/2
#	if i % rez == 0 and j % rez == 1:
#	mforceMap[form][i,j] = upleft + upright
#	if i % rez == 1 and j % rez == 0:
#	mforceMap[form][i,j] = upleft + downleft
#	if i % rez == 1 and j % rez == 1:
#	mforceMap[form][i,j] = upleft + downleft + upright + downright
	return

def findExtrema(text):
	forms = np.shape(mforceMap)[0]
	for f in xrange(forms):
		lmin[f] = np.amin(mforceMap[f])
		lmax[f] = np.amax(mforceMap[f])
	gmin = np.amin(lmin)
	gmax = np.amax(lmax)
	for form in xrange(forms):
		rows = np.shape(mforceMap[form])[0]
		cols = np.shape(mforceMap[form])[1]
		for i in xrange(rows):
			for j in xrange(cols):
				xpos = float(i)
				ypos = float(j)
				if mforceMap[form][i,j] == gmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a minimum of {} at position ({}, {})".format(gmin, xpos, ypos)
				if mforceMap[form][i,j] == gmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a maximum of {} at position ({}, {})".format(gmax, xpos, ypos)
	return

print
print np.around(hostRegion, decimals=1)
print 
print np.around(guestRegion, decimals=1)
print
print np.around(guestRegion[::-1], decimals=1)

guestForms(randomGuest)
calcForceMap(spunGuests)
findExtrema('the random')
calcForceMap(flipGuests)
findExtrema('the random flipped')

"""
import scipy.ndimage as nd
guestRotate45 = nd.rotate(randomGuest, 45, order=1)
guestRotate45 = np.around(guestRotate45, decimals=1)

hostRotate45 = nd.rotate(randomHost, 45, reshape=False, order=1)
hostRotate45 = np.around(hostRotate45, decimals=1)
"""
