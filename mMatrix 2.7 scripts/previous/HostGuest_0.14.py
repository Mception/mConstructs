# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017
Updated on Sun Nov 26 20:57 2017
@author: MJL
"""
import numpy as np
from copy import deepcopy

m = int(raw_input("Enter number of rows for host: "))
n = int(raw_input("Enter number of columns for host: "))

x = int(raw_input("Enter number of rows for guest: "))
y = int(raw_input("Enter number of columns for guest: "))

if m*n<x*y:
	print '\nHost size is too small for guest.\nTry running script again.'
	raise SystemExit
elif x >= y:
	z = x-1
else:
	z = y-1

hostsize = (m + 2*z, n + 2*z)
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

xmap = m + 1
ymap = n + 1

mforceMap = np.array((np.zeros((4,xmap-x,ymap-y), dtype=np.float)))

if x<>y:
	mforceMap = (mforceMap[0], np.zeros((xmap-y,ymap-x), dtype=np.float), mforceMap[2], np.zeros((xmap-y,ymap-x), dtype=np.float))
#a four (row, col) or alternating (col, row) matrix holding all net host-binding forces for a guest rotated by 0, 90, 180, & 270 deg.

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
		for i in range(xmap-row):
			for j in range(ymap-col):
				mforceMap[form][i,j] = np.sum(gforms[form] * randomHost[i:i+row,j:j+col])
	return

def findExtrema(text):
	forms = np.shape(mforceMap)[0]
	for f in range(forms):
		lmin[f] = np.amin(mforceMap[f])
		lmax[f] = np.amax(mforceMap[f])
	gmin = np.amin(lmin)
	gmax = np.amax(lmax)
	for form in range(forms):
		rows = np.shape(mforceMap[form])[0]
		cols = np.shape(mforceMap[form])[1]
		for i in range(rows):
			for j in range(cols):
				if mforceMap[form][i,j] == gmin:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a minimum of {} at position ({}, {})".format(gmin, i, j)
				if mforceMap[form][i,j] == gmax:
					print "\nFor {} guest, spun {}-degrees:".format(text, form*90)
					print "found a maximum of {} at position ({}, {})".format(gmax, i, j)
	return

print randomHost
print 
guestForms(randomGuest)
print spunGuests[0]
print
print flipGuests[0]

time = float(m*n)
print '\nThis may take around {} min(s) to complete.'.format('{0:.2f}'.format(time/120000+(m+n)/1200))
print

calcForceMap(spunGuests)
findExtrema('the random')
calcForceMap(flipGuests)
findExtrema('the random flipped')

"""
m = 12
n = 11
x = 3
y = 2
z = 2

# np.sum(spunGuests[0] * randomHost[6:9,6:8])
# np.sum(flipGuests[1] * randomHost[2:4,2:5])
# np.shape(spunGuests[0])[0]
# np.shape(spunGuests[0])[1]
# np.shape(mforceMap[0])[0]
# np.shape(mforceMap[0])[1]

randomHost = np.array([
[0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0],
[0,0,+1,-1,-1,0,0,0,0,0,0],
[0,0,+1,+1,-2,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,+2,+1,0,0,0],
[0,0,0,0,0,0,-1,+1,0,0,0],
[0,0,0,0,0,0,-1,-1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0]])

randomGuest = np.array([
[-6,-5],
[+4,-3],
[+2,+1]])
"""
