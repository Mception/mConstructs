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
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,-1,+1,+1,0,0,0],
[0,0,0,0,0,0,-1,-1,+1,0,0,0],
[0,0,0,0,0,0,-1,+1,-1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0]])#designed to be simple for test purposes

hostRegion= hostMatrix[6:9,6:9]
hostRegion= np.array(hostRegion)#this is the best target for the guest

guestMatrix = np.array([
[+1,-1,-1],
[+1,+1,-1],
[+1,-1,+1]])#designed to bind optimally to hostRegion

forceMap = np.zeros((10,10), dtype=np.int)
mforceMap = (forceMap, forceMap, forceMap, forceMap)
mforceMap = np.array(mforceMap)
#a 4x10x10 matrix holding all net host-guest forces for a guest rotated by 0, 90, 180, & 270 deg.

guestMatrix0 = deepcopy(guestMatrix)
flipMatrix90 = guestMatrix0.transpose()
guestMatrix270 = flipMatrix90[::-1]
flipMatrix180 = guestMatrix270.transpose()
guestMatrix180 = flipMatrix180[::-1]
flipMatrix270 = guestMatrix180.transpose()
guestMatrix90 = flipMatrix270[::-1]
flipMatrix0 = guestMatrix90.transpose()#efficient sequence of rotation and flipping operations

guestMatrices = (guestMatrix0,guestMatrix90,guestMatrix180,guestMatrix270)
flipMatrices = (flipMatrix0,flipMatrix90,flipMatrix180,flipMatrix270)
#allMatrices = (guestMatrices,flipMatrices)

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
print("\n################################################################################")
print("\nThis is the HOST SURFACE:")
print hostMatrix
print("\nTarget HOST-REGION (from host surface):")
print hostRegion
print("\nORIGINAL GUEST (to bind to host surface):")
print guestMatrix
print("\n################################################################################")
print("### AIM: MOVE, FLIP and/or ROTATE GUEST so as to find the target HOST-REGION ###")
print("### NOTE: The more -ve the NET FORCE the stronger the HOST-GUEST interaction ###")
print("################################################################################")
print
calcForceMap(guestMatrices)
print 'Original-guest interactions at 0, 90, 180 and 270 rotations.'
print mforceMap
print
print 'Flipped-guest interactions at 0, 90, 180 and 270 rotations.'
calcForceMap(flipMatrices)
print mforceMap


