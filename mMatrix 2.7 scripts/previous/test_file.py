#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 11:07:03 2017

@author: mlear
"""

import numpy as np

randomGuest = np.arange(25).reshape((5,5))
x=2
y=3
z = 3
rez = 2
gsize = z*rez-rez+1

guestRegion = np.array(np.random.uniform(-1, 1, (x,y)))

if x>=y:
    guestSquared = np.c_[guestRegion, np.zeros(x)]
else:
    guestSquared = np.r_[guestRegion, [np.zeros(y)]]

guestSpun45 = np.array(np.zeros((gsize*2-1,gsize*2-1)))
for i in xrange(gsize):
	for j in xrange(gsize):
		guestSpun45[(i+j),(j-i)+(z-1)*2] = randomGuest[i,j]
#this rotates the guest to a 45 degree form, appropriate for host binding

print randomGuest
print
print guestSpun45
print
print guestSquared

