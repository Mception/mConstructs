#coding: utf-8

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017

@author: MJL
"""
import numpy as np
from copy import deepcopy

m = int(raw_input("Enter number of rows for host: "))
n = int(raw_input("Enter number of columns for host: "))

x = int(raw_input("Enter number of rows for guest: "))
y = int(raw_input("Enter number of columns for guest: "))

if m*n<x*y:
	print '\nHost size is too small. Try running script again.'
	raise SystemExit
elif x >= y:
	z = x-1
else:
	z = y-1

hostsize = (m + 2*z, n + 2*z)
randomHost = np.array(np.zeros(hostsize, dtype=np.float))
randomHost[z:z+m,z:z+n] = np.random.uniform(-1, 1, (m, n))
randomHost = np.around(randomHost, decimals=1)

guestsize = (x, y)
randomGuest = np.random.uniform(-1, 1, guestsize)
randomGuest = np.around(randomGuest, decimals=1)

xyguest = randomGuest[::-1]
yxguest = randomGuest.transpose()

xyGuests = np.array((xyguest,xyguest,xyguest,xyguest), dtype=np.float)
yxGuests = np.array((yxguest,yxguest,yxguest,yxguest), dtype=np.float)

spunGuests = (xyGuests[0], yxGuests[0], xyGuests[2], yxGuests[2])
flipGuests = (xyGuests[1], yxGuests[3], xyGuests[3], yxGuests[1])
# four (x by y) or (y by x) matrix arrays to hold the guests & flipped guests rotated by 0, 90, 180, & 270 deg.

xmap = 2*z + m + 1
ymap = 2*z + n + 1
xyforceMap = np.array(np.zeros((xmap-x,ymap-y), dtype=np.float))
yxforceMap = np.array(np.zeros((xmap-y,ymap-x), dtype=np.float))

if x==y:
	mforceMap = np.array((xyforceMap, xyforceMap, xyforceMap, xyforceMap))
else:
	mforceMap = np.array((xyforceMap, yxforceMap, xyforceMap, yxforceMap))
#a four (row, col) or (col, row) matrix holding all net host-binding forces for a guest rotated by 0, 90, 180, & 270 deg.

lmin = np.array(np.zeros(4, dtype=np.float))
lmax = np.array(np.zeros(4, dtype=np.float))
gmin = np.amin(lmin)
gmax = np.amax(lmax)
#defining local and global extrema

def guestForms (guest):
	xyGuests[0] = guest
	xyGuests[1] = xyGuests[0][::-1]
	yxGuests[0] = xyGuests[1].transpose()
	yxGuests[1] = yxGuests[0][::-1]
	xyGuests[2] = yxGuests[1].transpose()
	xyGuests[3] = xyGuests[2][::-1]
	yxGuests[2] = xyGuests[3].transpose()
	yxGuests[3] = yxGuests[2][::-1]
	spunGuests = (xyGuests[0], yxGuests[0], xyGuests[2], yxGuests[2])
	flipGuests = (xyGuests[1], yxGuests[3], xyGuests[3], yxGuests[1])
	return spunGuests
	return flipGuests
#Guest positions of 0, 1, 2, 3 equal the guest-forms rotated by 0, 90, 180, 270 degrees

def calcForceMap(gforms, hform):
	mfmap = mforceMap
	forms = np.shape(gforms)[0]
	for form in range(forms):
		row = np.shape(gforms[form])[0]
		col = np.shape(gforms[form])[1]
		rowshifts = np.shape(mfmap[form])[0]
		colshifts = np.shape(mfmap[form])[1]
		for i in range(rowshifts):
			for j in range(colshifts):
				netforce = np.sum(gforms[form] * hform[i:i+row,j:j+col])
				mfmap[form][i,j] = netforce
	mforceMap[form]=mfmap[form]
	return mforceMap

def findExtrema(mforcemap, text):
	forms = np.shape(mforcemap)[0]
	for form in range(forms):
		lmin[form] = np.amin(mforcemap[form])
		lmax[form] = np.amax(mforcemap[form])
	gmin = np.amin(lmin)
	gmax = np.amax(lmax)
	for form in range(forms):
		rows = np.shape(mforcemap[form])[0]
		cols = np.shape(mforcemap[form])[1]
		for i in range(rows):
			for j in range(cols):
				if mforcemap[form][i,j] == gmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a minimum of {} at position ({}, {})".format(gmin, i, j)
				if mforcemap[form][i,j] == gmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a maximum of {} at position ({}, {})".format(gmax, i, j)
	return mforcemap

print
print randomHost
print 
guestForms(randomGuest)
print spunGuests[0]
print
print flipGuests[0]

calcForceMap(spunGuests, randomHost)
findExtrema(mforceMap, 'the random')
calcForceMap(flipGuests, randomHost)
findExtrema(mforceMap, 'the random flipped')
