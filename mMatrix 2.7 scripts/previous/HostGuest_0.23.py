# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017
Updated on Thu Dec 02 00:42 2017
@author: MJL
"""
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
"""
m = int(raw_input("Enter number of rows for host: "))
n = int(raw_input("Enter number of columns for host: "))

x = int(raw_input("Enter number of rows for guest: "))
y = int(raw_input("Enter number of columns for guest: "))

rez = int(raw_input("Enter resolution of chemical space (1 = low; 4 = high): "))*2 #resolution value is made even for more direct host-guest calculations

if rez <1 or rez > 8:
	rez = int(raw_input("Re-enter resolution between 1 = low and 4 = high: "))*2
if rez <1 or rez > 8:
	print 'Try running script again.'
	raise SystemExit

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
"""
m=2
n=2
x=2
y=2
z=2
rez = 2

time = float(m*n*2*z*rez)
print '\nThis may take around {} min(s) to complete an iPad A7 processor.'.format('{0:.2f}'.format(time/120000+(m+n+2*z)*rez/600))

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

hostsize = ((m+z)*rez-1, (n+z)*rez-1)
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
#spunGuests45 = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
#flipGuests45 = np.array((np.zeros((4,gsize,gsize), dtype=np.float)))
# each are 4 square matrix arrays, holding the guests & flipped guests,
# which are rotated in increments of 45 and/or 90 degrees

xmap = (m+z)*rez-1-2
ymap = (n+z)*rez-1-2
fmapSpunFull = np.array((np.zeros((4,xmap,ymap), dtype=np.float)))
fmapFlipFull = np.array((np.zeros((4,xmap,ymap), dtype=np.float)))
#fmapSpun45 = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
#fmapFlip45 = np.array((np.zeros((4,m+z-1,n+z-1), dtype=np.float)))
# each are 4 square matrix arrays holding all net host-guest binding forces
# for a set of rotated guests, so that extrema can be found

lminSF = np.array(np.zeros((4,3), dtype=np.float))
lmaxSF = np.array(np.zeros((4,3), dtype=np.float))
gminSF = np.array([0,0,0], dtype=np.float)
gmaxSF = np.array([0,0,0], dtype=np.float)#spun-full extrema
lminFF = np.array(np.zeros((4,3), dtype=np.float))
lmaxFF = np.array(np.zeros((4,3), dtype=np.float))
gminFF = np.array([0,0,0], dtype=np.float)
gmaxFF = np.array([0,0,0], dtype=np.float)#flip-full extrema
lminSH = np.array(np.zeros((4,3), dtype=np.float))
lmaxSH = np.array(np.zeros((4,3), dtype=np.float))
gminSH = np.array([0,0,0], dtype=np.float)
gmaxSH = np.array([0,0,0], dtype=np.float)#spun-half extrema
lminFH = np.array(np.zeros((4,3), dtype=np.float))
lmaxFH = np.array(np.zeros((4,3), dtype=np.float))
gminFH = np.array([0,0,0], dtype=np.float)
gmaxFH = np.array([0,0,0], dtype=np.float)#flip-half extrema
lminS45 = np.array(np.zeros((4,3), dtype=np.float))
lmaxS45 = np.array(np.zeros((4,3), dtype=np.float))
gminS45 = np.array([0,0,0], dtype=np.float)
gmaxS45 = np.array([0,0,0], dtype=np.float)#spun-45 extrema
lminF45 = np.array(np.zeros((4,3), dtype=np.float))
lmaxF45 = np.array(np.zeros((4,3), dtype=np.float))
gminF45 = np.array([0,0,0], dtype=np.float)
gmaxF45 = np.array([0,0,0], dtype=np.float)#flip-45 extrema
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

def calcForceMap(gforms, fmapfull):
	forcemap = fmapfull
	forms = np.shape(gforms)[0]
	for form in xrange(forms):
		for i in xrange(0,xmap,rez):
			for j in xrange(0,ymap,rez):
				forcemap[form][i,j] = np.sum(gforms[form] *
															randomHost[i:i+gsize,j:j+gsize])
		for i in xrange(0,xmap,rez):
			for j in xrange(1,ymap-1,rez):
				sideleft = forcemap[form][i,j-1]
				sideright = forcemap[form][i,j+1]
				forcemap[form][i,j] = (sideleft + sideright)/2
		for i in xrange(1,xmap-1,rez):
			for j in xrange(0,ymap,rez):
				top = np.sum(gforms[form] *
							randomHost[i-1:i+gsize-1,j:j+gsize])
				bottom = np.sum(gforms[form] *
							randomHost[i+1:i+gsize+1,j:j+gsize])
				forcemap[form][i,j] = (top + bottom)/2
		for i in xrange(1,xmap-1,rez):
			for j in xrange(1,ymap-1,rez):
				topleft = forcemap[form][i-1,j-1]
				downleft = forcemap[form][i+1,j-1]
				topright = forcemap[form][i-1,j+1]
				downright = forcemap[form][i+1,j+1]
				forcemap[form][i,j] = (topleft + topright + downleft + downright)/2
	return

def findExtrema(fmap, lmin, lmax, gmin, gmax, text):
	forms = np.shape(fmap)[0]
	forcemap = fmap
	min = gmin
	max = gmax
	for f in xrange(forms):
		lmin[f,0] = np.amin(forcemap[f])
		lmax[f,0] = np.amax(forcemap[f])
	min[0] = np.amin(lmin[:,0])
	max[0] = np.amax(lmax[:,0])
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
				if forcemap[form][i,j] == min[0]:
					min[1:3]=(xpos,ypos)
				if forcemap[form][i,j] == max[0]:
					max[1:3]=(xpos,ypos)
	print "\nLocal minima & maxima for {} guest-host binding are:\n{}\n\n{}".format(text,lmin,lmax)
	print "Global extrema are {} and {}.".format(min,max)
	fmap = forcemap
	gmin = min
	gmax = max
	return

print '\nHost:'
print randomHost
print '\nGuest:'
print randomGuest
#print '\nGuest flipped:'
#print randomGuest[::-1]
#print '\nGuest spun 45 degrees:'
#print np.around(guestSpun45, decimals=1)

guestForms(randomGuest, spunGuestsFull, flipGuestsFull)
#guestForms(guestSpun45, spunGuests45, flipGuests45)

calcForceMap(spunGuestsFull, fmapSpunFull)
calcForceMap(flipGuestsFull, fmapFlipFull)
print fmapSpunFull
findExtrema(fmapSpunFull,lminSF,lmaxSF,gminSF,gmaxSF,'the original')
findExtrema(fmapFlipFull,lminFF,lmaxFF,gminFF,gmaxFF,'the flipped')

#calcForceMap(spunGuests45,fmapSpun45, 0)
#findExtrema(fmapSpun45,lminS45,lmaxS45,gminS45,gmaxS45,'the 45 degree rotated')

#calcForceMap(flipGuests45,fmapFlip45, 1)
#findExtrema(fmapFlip45,lminF45,lmaxF45,gminF45,gmaxF45,'the 45 degree flipped')


"""
#import scipy.ndimage as nd
#guestRotate45 = nd.rotate(randomGuest, 45, order=1)
#guestRotate45 = np.around(guestRotate45, decimals=1)

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure()
ax = fig.gca(projection='3d')
#X = np.arange(-5, 5, 0.25)
#Y = np.arange(-5, 5, 0.25)
X = randomHost
Y = randomHost
X, Y = np.meshgrid(X, Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)
Z = 4
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

"""
