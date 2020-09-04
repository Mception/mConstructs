"""
Created on Thu Nov 30 11:07:03 2017 - py2.7
Updated on Thu Sep 03 23:06:00 2020 - py3.6
@author: DrM @ Lincoln, UK
"""

import numpy as np

r = int(input("Enter no. of row-atom-charges for binding region (>=2): "))
c = int(input("Enter no. of col-atom-charges for binding region (>=2): "))
m = int(input("Enter longest no. of linear atoms for molecule (>=3): "))


if m < 3:
	m = 3

md = 2 * m - 1
z = md * 3

time = float(r * c * 2 * md)
print('\nThis may take around {} min(s) to complete an iPad A7 processor.'.
						format('{0:.2f}'.format(time / 120000 + (r + c + 2 * md) / 300)))

mMatrix = np.array(np.zeros((z, z), dtype=np.float))
mSpun45 = np.array(np.zeros((z, z), dtype=np.float))
mFlip45 = np.array(np.zeros((z, z), dtype=np.float))  #standard molecular-forms(m)

mdMatrix = np.array(np.zeros((md, md, 3, 3), dtype=np.float))
mdSpun45 = np.array(np.zeros((md, md, 3, 3), dtype=np.float))
mdFlip45 = np.array(np.zeros((md, md, 3, 3), dtype=np.float))  #multi-dimensional(md)

spunMs = np.array((np.zeros((8, z, z), dtype=np.float)))
flipMs = np.array((np.zeros((8, z, z), dtype=np.float)))  #standard m-forms

spunMds = np.array((np.zeros((8, md, md, 3, 3), dtype=np.float)))
flipMds = np.array((np.zeros((8, md, md, 3, 3), dtype=np.float)))  #md-forms

spunMcs = np.array((np.zeros((8, md, md), dtype=np.float)))
flipMcs = np.array((np.zeros((8, md, md), dtype=np.float)))  #compressed versions

#atomMatrix = np.array(np.zeros((3,3)))
#bondMatrix = np.array(np.zeros((3,3)))

for i in range(0, z, 3):  # generates a random molecule to test routines
	for j in range(0, z, 3):
		#mMatrix[i:i+3,j:j+3] = atomMatrix
		mMatrix[i, j] = i / 3 * md + j / 3 + 1
		mMatrix[i + 1, j + 1] = np.around(np.random.uniform(-1, 1), decimals=1)
		mdMatrix[int(i / 3)][int(j / 3)] = mMatrix[i:i + 3, j:j + 3]
		if i % 2 == 1 or j % 2 == 1:
			#mMatrix[i:i+3,j:j+3] = bondMatrix
			mMatrix[i, j] = i / 3 * md + j / 3 + 1
			mMatrix[i, j + 1] = np.around(np.random.uniform(1, 2), decimals=1)
			mdMatrix[int(i / 3)][int(j / 3)] = mMatrix[i:i + 3, j:j + 3]

rez = 2  # spaces one element (e.g. a bond) between each atom-charge

size = (r * rez - 1 + (m * rez - 2) * 2, c * rez - 1 + (m * rez - 2) * 2)
bRegion = np.zeros(size)
bCharges = np.array(np.random.uniform(-1, 1, (r, c)))
for i in range(0, r * rez, rez):
	for j in range(0, c * rez, rez):
		bRegion[i + m * rez - rez, j + m * rez - rez] = bCharges[int(i / rez), int(j / rez)]
		bRegion = np.around(bRegion, decimals=1)
# this evenly places the binding atom charges into a zeroed space (r-by-c)
# and includes a zero-border for scanning purposes for the compressed m-forms

xmap = (r + m) * rez - 1 - 2
ymap = (c + m) * rez - 1 - 2
fmapSpunMcs = np.array((np.zeros((8, xmap, ymap), dtype=np.float)))
fmapFlipMcs = np.array((np.zeros((8, xmap, ymap), dtype=np.float)))
# each are 8 square matrix arrays holding all net host-guest binding forces
# for a set of rotated guests, so that extrema can be found

lminSF = np.array(np.zeros((8, 3), dtype=np.float))
lmaxSF = np.array(np.zeros((8, 3), dtype=np.float))
gminSF = np.array([0, 0, 0], dtype=np.float)
gmaxSF = np.array([0, 0, 0], dtype=np.float)  #spun-forms extrema
lminFF = np.array(np.zeros((8, 3), dtype=np.float))
lmaxFF = np.array(np.zeros((8, 3), dtype=np.float))
gminFF = np.array([0, 0, 0], dtype=np.float)
gmaxFF = np.array([0, 0, 0], dtype=np.float)  #flipped-forms extrema

# output variables to hold local and global extrema


def md45(molIn, mol45):  # rotates molecule by 45 deg (keeping values unchanged)
	z = np.shape(molIn)[0]
	cNum = int(z / 2)
	for c in range(cNum):
		size = z - c
		shift = cNum - c
		mol45[c, c + shift:size] = molIn[c, c:size - shift]  #top row right
		mol45[c + shift:size, size - 1] = molIn[c:size - shift, size - 1]  #right col down
		mol45[size - 1, c:size - shift] = molIn[size - 1, c + shift:size]  #bottom row left
		mol45[c:size - shift, c] = molIn[c + shift:size, c]  #left col up
		if shift > 1:  #shift off-matrix elements in a spiral clockwise fashion
			mol45[c + 1:c + shift, size - 1] = molIn[c, size - shift:size - 1]
			mol45[size - 1, size - shift:size - 1] = molIn[size - shift:size - 1, size - 1][::-1]
			mol45[size - shift:size - 1, c] = molIn[size - 1, c + 1:c + shift]
			mol45[c, c + 1:c + shift] = molIn[c + 1:c + shift, c][::-1]
		if c == cNum - 1 and z % 2 == 1:
			mol45[cNum, cNum] = molIn[cNum, cNum]
	return


def mdConvert(cpd, mdcpd, md):  # reduces md-forms to m-forms, and vice versa
	z = np.shape(cpd)[0]
	if md == 0:
		for i in range(0, z, 3):
			for j in range(0, z, 3):
				mdcpd[int(i / 3)][int(j / 3)] = cpd[i:i + 3, j:j + 3]
	if md == 1:
		for i in range(0, z, 3):
			for j in range(0, z, 3):
				cpd[i:i + 3, j:j + 3] = mdcpd[int(i / 3)][int(j / 3)]
	return


def calcForceMap(mcforms, fmap):  #45 degree forms will be treated separately
	forcemap = fmap
	forms = np.shape(mcforms)[0]
	size = np.shape(mcforms[0])[0]
	for form in range(0, forms, 2):  #calculate the full (ontop) interactions
		for i in range(0, xmap, rez):
			for j in range(0, ymap, rez):
				forcemap[form][i, j] = np.sum(
					mcforms[form] * bRegion[i:i + size, j:j + size])
		for i in range(xmap):  #insert the half-shifted (inbetween) values
			for j in range(ymap):
				if i % rez == 0 and j % rez == 1:
					forcemap[form][i, j] = (
						forcemap[form][i, j - 1] + forcemap[form][i, j + 1]) / 2
				if i % rez == 1 and j % rez == 0:
					forcemap[form][i, j] = (
						forcemap[form][i - 1, j] + forcemap[form][i + 1, j]) / 2
				if i % rez == 1 and j % rez == 1:
					forcemap[form][i, j] = (
						forcemap[form][i - 1, j - 1] + forcemap[form][i + 1, j - 1] +
						forcemap[form][i - 1, j + 1] + forcemap[form][i + 1, j + 1]) / 2
	return


def findExtrema(fmap, lmin, lmax, gmin, gmax, text):
	forms = np.shape(fmap)[0]
	forcemap = fmap
	min = gmin
	max = gmax
	for f in range(forms):
		lmin[f, 0] = np.amin(forcemap[f])
		lmax[f, 0] = np.amax(forcemap[f])
	min[0] = np.amin(lmin[:, 0])
	max[0] = np.amax(lmax[:, 0])
	for form in range(forms):
		rows = np.shape(forcemap[form])[0]
		cols = np.shape(forcemap[form])[1]
		for i in range(rows):
			for j in range(cols):
				if forcemap[form][i, j] == lmin[form, 0]:
					lmin[form, 1] = i
					lmin[form, 2] = j
				if forcemap[form][i, j] == lmax[form, 0]:
					lmax[form, 1] = i
					lmax[form, 2] = j
				if forcemap[form][i, j] == min[0]:
					min[1:3] = (i, j)
				if forcemap[form][i, j] == max[0]:
					max[1:3] = (i, j)
	print("\nLocal binding minima & maxima for {} molecules are:\n{}\n\n{}".format(
		text, lmin, lmax))
	print("Global extrema are {} and {}.".format(min, max))
	fmap = forcemap
	gmin = min
	gmax = max
	return


spunMds[0] = mdMatrix
spunMds[1] = mdSpun45
flipMds[0] = mdMatrix[::-1]
flipMds[1] = mdFlip45

for i in range(7):
	md45(spunMds[i], spunMds[i + 1])
	md45(flipMds[i], flipMds[i + 1])

for i in range(8):
	mdConvert(spunMs[i], spunMds[i], 1)
	mdConvert(flipMs[i], flipMds[i], 1)

for i in range(8):
	spunMcs[i] = spunMds[i][..., 1, 1]
	flipMcs[i] = flipMds[i][..., 1, 1]

print
print('\nMolecular binding charges, region, surface, or entity:')
#print bRegion
print(bRegion[md - 1:2 * r + md - 1:2, md - 1:2 * c + md - 1:2])

print
print('\nMolecules rotated by 0, 45, 90, 135, 180, 225, 270, 315:')
#print spunMcs
print(spunMcs[..., ::2, ::2])

print
print('\nFlipped molecules rotated by 0, 45, 90, 135, 180, 225, 270, 315:')
#print flipMcs
print(flipMcs[..., ::2, ::2])

calcForceMap(spunMcs, fmapSpunMcs)
findExtrema(fmapSpunMcs, lminSF, lmaxSF, gminSF, gmaxSF, 'the unflipped')

calcForceMap(flipMcs, fmapFlipMcs)
findExtrema(fmapFlipMcs, lminFF, lmaxFF, gminFF, gmaxFF, 'the flipped')

