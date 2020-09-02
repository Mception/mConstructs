# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017
Updated on Tues Nov 28 16:00 2017
@author: MJL
"""
import numpy as np
from copy import deepcopy
"""
m = int(raw_input("Enter number of rows for host: "))
n = int(raw_input("Enter number of columns for host: "))

x = int(raw_input("Enter number of rows for guest: "))
y = int(raw_input("Enter number of columns for guest: "))

if m*n<x*y:
	print '\nHost size is too small for guest.\nHost will be treated as guest.'
	xcopy = x
	ycopy = y
	x = deepcopy(m)
	y = deepcopy(n)
	m = deepcopy(xcopy)
	n = deepcopy(ycopy)

time = float(m*n)
print '\nThis may take around {} min(s) to complete on an iPad A7 processor.'.format('{0:.2f}'.format(time/120000+(m+n)/600))
"""	
x = 5
y = 5
m = 7
n = 7

if x >= y:
	z = x-1
else:
	z = y-1
	
xhost = m + 2*z
yhost = n + 2*z

hostsize = (xhost, yhost)
randomHost = np.array(np.zeros(hostsize, dtype=np.float))
randomHost[z:z+m,z:z+n] = np.random.uniform(-1, 1, (m, n))
randomHost = np.around(randomHost, decimals=1)
#this sets a zero border around the host for off grid scanning

guestsize = (x, y)
randomGuest = np.random.uniform(-1, 1, guestsize)
randomGuest = np.around(randomGuest, decimals=1)

spunGuests = np.array((np.zeros((x,y)), np.zeros((y,x)), np.zeros((x,y)), np.zeros((y,x))))
flipGuests = np.array((np.zeros((x,y)), np.zeros((y,x)), np.zeros((x,y)), np.zeros((y,x))))
# alternating four (x by y) / (y by x) matrix arrays to hold the guests & flipped guests rotated by 0, 90, 180, & 270 deg.

mforceMap = np.array((np.zeros((4,xhost-x+1,yhost-y+1), dtype=np.float)))
if x<>y:
	mforceMap = (mforceMap[0], np.zeros((xhost-y+1,yhost-x+1), dtype=np.float), mforceMap[2], np.zeros((xhost-y+1,yhost-x+1), dtype=np.float))
#a four (row, col) or alternating (col, row) matrix holding all net host-binding forces for a guest rotated by 0, 90, 180, & 270 deg.

mforceMapx2= np.array((np.zeros((4,2*(xhost-x)+1,2*(yhost-y)+1), dtype=np.float)))
if x<>y:
	mforceMapx2 = (mforceMapx2[0], np.zeros((2*(xhost-y)+1,2*(yhost-x)+1), dtype=np.float), mforceMapx2[2], np.zeros((2*(xhost-y)+1,2*(yhost-x)+1), dtype=np.float))
#a four (row, col) or alternating (col, row) matrix holding all net host-binding forces for a guest rotated by 0, 90, 180, & 270 deg.

guestmap45 = np.array(np.zeros((x,y), dtype=np.float))
mforceMap45 = np.array((np.zeros((4,xhost-x-1,yhost-y-1), dtype=np.float)))
if x<>y:
	mforceMap45 = (mforceMap45[0], np.zeros((xhost-y-1,yhost-x-1), dtype=np.float), mforceMap45[2], np.zeros((xhost-y-1,yhost-x-1), dtype=np.float))
#a four (row, col) or alternating (col, row) matrix holding all net host-binding forces for a guest rotated by 45, 135, 225, & 315 deg.

lmin = np.array(np.zeros(4, dtype=np.float))
lmax = np.array(np.zeros(4, dtype=np.float))
gmin = np.amin(lmin)
gmax = np.amax(lmax)
#defining local and global extrema

def guestForms (guest):
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
	for form in range(forms):
		row = np.shape(gforms[form])[0]
		col = np.shape(gforms[form])[1]
		xmap = np.shape(mforceMapx2[form])[0]
		ymap = np.shape(mforceMapx2[form])[1]
		for i in range(xmap):
			for j in xrange(ymap):
				if i % 2 == 0 and j % 2 == 0:
					mforceMapx2[form][i,j] = np.sum(gforms[form] * randomHost[i/2:i/2+row,j/2:j/2+col])
		for i in range(xmap-1):
			for j in xrange(ymap-1):
				upleft = mforceMapx2[form][i,j]/2
				downleft = mforceMapx2[form][i+1,j]/2
				upright = mforceMapx2[form][i,j+1]/2
				downright = mforceMapx2[form][i+1,j+1]/2
				if i % 2 == 0 and j % 2 == 1:
					mforceMapx2[form][i,j] = upleft + upright
				if i % 2 == 1 and j % 2 == 0:
					mforceMapx2[form][i,j] = upleft + downleft
				if i % 2 == 1 and j % 2 == 1:
					mforceMapx2[form][i,j] = upleft + downleft + upright + downright
	return

def calcForces45(gforms):
	host = randomHost
	guest = randomGuest
	forms = np.shape(gforms)[0]
	for form in range(forms):
#		row = np.shape(gforms[form])[0]
#		col = np.shape(gforms[form])[1]
		xmap = np.shape(mforceMap45[form])[0]
		ymap = np.shape(mforceMap45[form])[1]
		for i in range(xmap):
			for j in range(ymap):
				for k in range(x):
					for l in range(y):
						if k%4==0 and l%4==0:
							guestmap45[k,l] = guest[k,l]*host[i,j+3]
						if k%4==0 and l%4==1:
							guestmap45[k,l] = guest[k,l]*host[i,j+4]/4 + guest[k,l]*host[i+1,j+3]/4 + guest[k,l]*host[i+1,j+4]*3/4
						if k%4==0 and l%4==2:
							guestmap45[k,l] = guest[k,l]*host[i+1,j+4]/2 + guest[k,l]*host[i+1,j+5]/2 + guest[k,l]*host[i+2,j+4]/2 + guest[k,l]*host[i+2,j+5]/2
						if k%4==0 and l%4==3:
							guestmap45[k,l] = guest[k,l]*host[i+2,j+5]*3/4 + guest[k,l]*host[i+2,j+6]/4 + guest[k,l]*host[i+3,j+5]/4
				#
						if k%4==1 and l%4==0:
							guestmap45[k,l] = guest[k,l]*host[i,j+2]/4 + guest[k,l]*host[i+1,j+2]*3/4 + guest[k,l]*host[i+1,j+3]/4
						if k%4==1 and l%4==1:
							guestmap45[k,l] = guest[k,l]*host[i+1,j+3]/2 + guest[k,l]*host[i+2,j+3]/2
						if k%4==1 and l%4==2:
							guestmap45[k,l] = guest[k,l]*host[i+2,j+3]/4 + guest[k,l]*host[i+2,j+4]*3/4 + guest[k,l]*host[i+3,j+4]/4
						if k%4==1 and l%4==3:
							guestmap45[k,l] = guest[k,l]*host[i+3,j+4]/2 + guest[k,l]*host[i+3,j+5]/2
				#
						if k%4==2 and l%4==0:
							guestmap45[k,l] = guest[k,l]*host[i+1,j+1]/2 + guest[k,l]*host[i+1,j+2]/2 + guest[k,l]*host[i+2,j+1]/2 + guest[k,l]*host[i+2,j+2]/2
						if k%4==2 and l%4==1:
							guestmap45[k,l] = guest[k,l]*host[i+2,j+2]*3/4 + guest[k,l]*host[i+2,j+3]/4 + guest[k,l]*host[i+3,j+2]/4 + guest[k,l]*host[i+3,j+3]/4
						if k%4==2 and l%4==2:
							guestmap45[k,l] = guest[k,l]*host[i+3,j+3]
						if k%4==2 and l%4==3:
							guestmap45[k,l] = guest[k,l]*host[i+3,j+4]/4 + guest[k,l]*host[i+4,j+3]/4 + guest[k,l]*host[i+4,j+4]*3/4
				#
						if k%4==3 and l%4==0:
							guestmap45[k,l] = guest[k,l]*host[i+2,j+1]*3/4 + guest[k,l]*host[i+2,j]/4 + guest[k,l]*host[i+3,j+1]/4
						if k%4==3 and l%4==1:
							guestmap45[k,l] = guest[k,l]*host[i+3,j+1]/2 + guest[k,l]*host[i+3,j+2]/2
						if k%4==3 and l%4==2:
							guestmap45[k,l] = guest[k,l]*host[i+3,j+2]/4 + guest[k,l]*host[i+4,j+2]*3/4 + guest[k,l]*host[i+4,j+3]/4 
						if k%4==3 and l%4==3:
							guestmap45[k,l] = guest[k,l]*host[i+4,j+3]/2 + guest[k,l]*host[i+5,j+3]/2
				mforceMap45[form][i,j] = np.sum(guestmap45)
	return

def findExtrema(text):
	forms = np.shape(mforceMapx2)[0]
	for f in range(forms):
		lmin[f] = np.amin(mforceMapx2[f])
		lmax[f] = np.amax(mforceMapx2[f])
	gmin = np.amin(lmin)
	gmax = np.amax(lmax)
	for form in range(forms):
		rows = np.shape(mforceMapx2[form])[0]
		cols = np.shape(mforceMapx2[form])[1]
		for i in range(rows):
			for j in range(cols):
				if mforceMapx2[form][i,j] == gmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a minimum of {} at position ({}, {})".format(gmin, float(i)/2, float(j)/2)
				if mforceMapx2[form][i,j] == gmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a maximum of {} at position ({}, {})".format(gmax, float(i)/2, float(j)/2)
	return
	
calcForces45(spunGuests)
