# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017

@author: MJL
"""
import numpy as np
from copy import deepcopy

hostMatrix = np.array([
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,-1,-1,-1,0,0,0,0,0,0,0],
[0,0,+1,-1,+1,0,0,0,0,0,0,0],
[0,0,+1,+1,-1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,-1,+1,+1,0,0,0],
[0,0,0,0,0,0,-1,-1,+1,0,0,0],
[0,0,0,0,0,0,-1,+1,-1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0]], dtype=np.float)
#designed to be simple for test purposes and features two host regions

guestMatrix = np.array([
[+1,-1,-1],
[+1,+1,-1],
[+1,-1,+1]], dtype=np.float)
#designed to bind optimally (force of -9) to the two host regions

guestMatrices = np.array((guestMatrix,guestMatrix,guestMatrix,guestMatrix), dtype=np.float)
flipMatrices = np.array((guestMatrix,guestMatrix,guestMatrix,guestMatrix), dtype=np.float)
# a 4x3x3 matrix array to eventually hold the guest forms rotated by 0, 90, 180, & 270 deg.

forceMap = np.zeros((10,10), dtype=np.float)
mforceMap = np.array((forceMap, forceMap, forceMap, forceMap))
#a 4x10x10 matrix holding all net host-guest forces for a guest rotated by 0, 90, 180, & 270 deg.

userGuest = np.zeros((3,3), dtype=np.float)

def guestForms (guest):
    guestMatrices[0] = guest
    flipMatrices[1] = guestMatrices[0].transpose()
    guestMatrices[3] = flipMatrices[1][::-1]
    flipMatrices[2] = guestMatrices[3].transpose()
    guestMatrices[2] = flipMatrices[2][::-1]
    flipMatrices[3] = guestMatrices[2].transpose()
    guestMatrices[1] = flipMatrices[3][::-1]
    flipMatrices[0] = guestMatrices[1].transpose()
    guestMatrices[1] = flipMatrices[0]
    return guestMatrices
    return flipMatrices
#Guest positions of 0, 1, 2, 3 equal the guest-forms rotated by 0, 90, 180, 270 degrees

def calcForceMap(gforms):
	mfmap = mforceMap
	numforms = np.shape(gforms)[0]
	numshifts = np.shape(hostMatrix)[0]-2
	for form in range(numforms):
		for i in range(numshifts):
			for j in range(numshifts):
				netforce = np.sum(gforms[form] * hostMatrix[i:i+3,j:j+3])
				mfmap[form,i,j] = netforce
		mforceMap[form]=mfmap[form]
	return mforceMap

def findExtrema(mforcemap, text):
	numforms = np.shape(mforcemap)[0]
	numrows = np.shape(mforcemap)[1]
	numcols = np.shape(mforcemap)[2]
	fmin = np.amin(mforcemap)
	fmax = np.amax(mforcemap)
	for form in range(numforms):
		print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
		for i in range(numrows):
			for j in range(numcols):
				if mforcemap[form,i,j] == fmin:
					print "found a minimum of {} at position ({}, {}).".format(fmin, i, j)
				if mforcemap[form,i,j] == fmax:
					print "found a maximum of {} at position ({}, {}).".format(fmax, i, j)
	return mforcemap

def inputGuest():
	n = int(raw_input("No. of rows: "))
	m = int(raw_input("No. of elements per row: "))
	a = [[input("Input element ({},{}) of guest matrix: ".format(i, j)) for j in range(m)] for i in range(n)]
	a = np.array(a, dtype=np.float)
	guestForms(a)
	print guestMatrices
	calcForceMap(guestMatrices)
	findExtrema(mforceMap, 'YOUR')
	print
	calcForceMap(flipMatrices)
	print flipMatrices
	findExtrema(mforceMap, 'YOUR FLIPPED')
	return guestMatrices
	return flipMatrices

print("\n############################################################################")
print("### AIM: MOVE, FLIP and/or ROTATE GUEST so as to find target HOST-REGION ###")
print("### NOTE: More -ve the NET FORCE the stronger the HOST-GUEST interaction ###")
print("############################################################################")
print("\nThis is the HOST SURFACE:")
print hostMatrix
print("\nTEST GUEST (to bind to host surface):")
print guestMatrices[0]
print("\nFLIPPED TEST GUEST (to bind to host surface):")
print flipMatrices[0]
print("\n### Enter <mfmapOriginal> or <mfmapFlipped> ###\n### for the complete force-maps over host   ###")

guestForms(guestMatrices[0])
calcForceMap(guestMatrices)
mfmapOriginal = deepcopy (mforceMap)
findExtrema(mforceMap, 'ORIGINAL TEST')
print
calcForceMap(flipMatrices)
mfmapFlipped = deepcopy (mforceMap)
findExtrema(mforceMap, 'FLIPPED TEST')
print

print guestMatrices
print flipMatrices


inputGuest()


