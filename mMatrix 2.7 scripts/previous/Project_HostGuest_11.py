#coding: utf-8

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017

@author: MJL
"""
import numpy as np

hostsize = (5, 5)
randomHost = np.random.uniform (-1, 1, hostsize)
randomHost = np.around(randomHost, decimals=0)

#x = int(raw_input("Enter number of rows for guest: "))
#y = int(raw_input("Enter number of columns for guest: "))

#guestsize = (x, y)
#randomGuest = np.random.uniform(-1, 1, guestsize)
#randomGuest = np.around(randomGuest, decimals=0)

randomGuest = np.array(([[1,2],
               [3,4],
               [5,6]]), dtype=np.float)

xyguestflip = randomGuest[::-1]
yxguestspun = randomGuest.transpose()

xyGuests = np.array((randomGuest,randomGuest,randomGuest,randomGuest), dtype=np.float)
yxGuests = np.array((yxguestspun,yxguestspun,yxguestspun,yxguestspun), dtype=np.float)
flipGuests = (xyGuests[1], yxGuests[3], xyGuests[3], yxGuests[1])
spunGuests = (xyGuests[0], yxGuests[0], xyGuests[2], yxGuests[2])

# 4x(gsize, gsize) matrix arrays to eventually hold the guest & flipped forms rotated by 0, 90, 180, & 270 deg.

ro = np.shape(randomHost)[0]-np.shape(randomGuest)[0]
co = np.shape(randomHost)[1]-np.shape(randomGuest)[1]

forceMap = np.zeros((ro+1,co+1), dtype=np.float)
mforceMap = np.array((forceMap, forceMap, forceMap, forceMap))
#a 4x(row, col) matrix holding all net host-binding forces for a guest rotated by 0, 90, 180, & 270 deg.

def guestForms (guest):
    if rowsize == colsize:
        spunGuests[0] = guest
        flipGuests[1] = spunGuests[0].transpose()
        spunGuests[3] = flipGuests[1][::-1]
        flipGuests[2] = spunGuests[3].transpose()
        spunGuests[2] = flipGuests[2][::-1]
        flipGuests[3] = spunGuests[2].transpose()
        spunGuests[1] = flipGuests[3][::-1]
        flipGuests[0] = spunGuests[1].transpose()
    else:
        xyGuests[0] = guest
        xyGuests[1] = xyGuests[0][::-1]
        yxGuests[0] = xyGuests[1].transpose()
        yxGuests[1] = yxGuests[0][::-1]
        xyGuests[2] = yxGuests[1].transpose()
        xyGuests[3] = xyGuests[2][::-1]
        yxGuests[2] = xyGuests[3].transpose()
        yxGuests[3] = yxGuests[2][::-1]
        flipGuests = (xyGuests[1], yxGuests[3], xyGuests[3], yxGuests[1])
        spunGuests = (xyGuests[0], yxGuests[0], xyGuests[2], yxGuests[2])
    return spunGuests
    return flipGuests
#Guest positions of 0, 1, 2, 3 equal the guest-forms rotated by 0, 90, 180, 270 degrees

def calcForceMap(gforms, hform):
	mfmap = mforceMap
	forms = np.shape(gforms)[0]
	rows = np.shape(gforms)[1]
	cols = np.shape(gforms)[2]
	rowshifts = np.shape(hform)[0]-rows+1
	colshifts = np.shape(hform)[1]-cols+1
	for form in range(forms):
		for i in range(rowshifts):
			for j in range(colshifts):
				netforce = np.sum(gforms[form] * hform[i:i+rows,j:j+cols])
				mfmap[form,i,j] = netforce
		mforceMap[form]=mfmap[form]
	return mforceMap

def findExtrema(mforcemap, text):
	forms = np.shape(mforcemap)[0]
	rows = np.shape(mforcemap)[1]
	cols = np.shape(mforcemap)[2]
	fmin = np.amin(mforcemap)
	fmax = np.amax(mforcemap)
	for form in range(forms):
		for i in range(rows):
			for j in range(cols):
				if mforcemap[form,i,j] == fmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a minimum of {} at position ({}, {})".format(fmin, i, j)
				if mforcemap[form,i,j] == fmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a maximum of {} at position ({}, {})".format(fmax, i, j)
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

"""
print("\n############################################################################")
print("### AIM: MOVE, FLIP and/or ROTATE GUEST so as to find target HOST-REGION ###")
print("### NOTE: More -ve the NET FORCE the stronger the HOST-GUEST interaction ###")
print("############################################################################")
print("\nThis is the HOST SURFACE:")
print hostMatrix
print("\nTEST GUEST (to bind to host surface):")
print guestMatrix
print("\nFLIPPED TEST GUEST (to bind to host surface):")
print guestMatrix[::-1]

guestForms(guestMatrix)
calcForceMap(guestMatrices)
mfmapOriginal = deepcopy (mforceMap)
findExtrema(mforceMap, 'ORIGINAL TEST')
print
calcForceMap(flipMatrices)
mfmapFlipped = deepcopy (mforceMap)
findExtrema(mforceMap, 'FLIPPED TEST')


def inputGuest():
	n = int(raw_input("No. of rows: "))
	m = int(raw_input("No. of elements per row: "))
	a = [[input("Input element ({},{}) of guest matrix: ".format(i, j)) for j in range(m)] for i in range(n)]
	b = np.array(a, dtype=np.float)
	guestForms(b)
	calcForceMap(guestMatrices, hostRandom)
	findExtrema(mforceMap, 'YOUR')
	print
	calcForceMap(flipMatrices, hostRandom)
	findExtrema(mforceMap, 'YOUR FLIPPED')
	return guestMatrices
	return flipMatrices

inputGuest()
"""