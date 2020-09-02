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

hostTarget = hostMatrix[6:9,6:9]
hostTarget = np.array(hostTarget)

guestMatrix = np.array([
[+1,-1,-1],
[+1,+1,-1],
[+1,-1,+1]])#designed to bind best to hostTarget

hostRegion = np.array([
[-1,+1,+1],
[-1,-1,+1],
[-1,+1,-1]])#this is the same as the hostTarget

mforceMap = (np.zeros((10,10), dtype=np.int), np.zeros((10,10), dtype=np.int), np.zeros((10,10), dtype=np.int), np.zeros((10,10), dtype=np.int))
mforceMap = np.array(mforceMap)
#A 4x10x10 matrix holding all net host-guest forces for a guest rotated by 0, 90, 180, & 270 deg.

guestMatrix0 = deepcopy(guestMatrix)
flipMatrix90 = guestMatrix0.transpose()
guestMatrix270 = flipMatrix90[::-1]
flipMatrix180 = guestMatrix270.transpose()
guestMatrix180 = flipMatrix180[::-1]
flipMatrix270 = guestMatrix180.transpose()
guestMatrix90 = flipMatrix270[::-1]
flipMatrix0 = guestMatrix90.transpose()

guestMatrices = (guestMatrix0,guestMatrix90,guestMatrix180,guestMatrix270)
flipMatrices = (flipMatrix0,flipMatrix90,flipMatrix180,flipMatrix270)
allMatrices = (guestMatrix0,guestMatrix90,guestMatrix180,guestMatrix270, flipMatrix0,flipMatrix90,flipMatrix180,flipMatrix270)

def calcForces(guestforms, text):
	guestForm = deepcopy(guestforms)
	numforms = np.shape(guestForm)[0]
	for i in range(numforms):
		print "\nFor {} guest, spun {}-degrees:".format(text, i*90)
		print guestForm[i]
		netForce = np.sum(guestForm[i] * hostRegion)
		print "Net force = {} (over host-guest region).".format(netForce)
	return guestForm

print 'A test run on spinning and flipping guest over target host region.'
calcForces(guestMatrices, 'original')
calcForces(flipMatrices, 'flipped')

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

print
calcForceMap(guestMatrices)
print 'Original-guest interactions at 0, 90, 180 and 270 rotations.'
print mforceMap
print
print 'Flipped-guest interactions at 0, 90, 180 and 270 rotations.'
calcForceMap(flipMatrices)
print mforceMap

