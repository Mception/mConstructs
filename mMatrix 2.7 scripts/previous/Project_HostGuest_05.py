# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017

@author: MJL
"""
testMatrix = [
[1,2,3],
[4,5,6],
[7,8,9]]
#above matrix is for testing purposes

from copy import deepcopy
import numpy as np

h = 12
hostMatrix = [
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
[0,0,0,0,0,0,0,0,0,0,0,0]]

g = 3
guestMatrix = [
[+1,-1,-1],
[+1,+1,-1],
[+1,-1,+1]]

copyGuest0 = deepcopy(guestMatrix)

hostRegion = [
[-1,+1,+1],
[-1,-1,+1],
[-1,+1,-1]]

blankMatrix = [
[' ',' ',' '],
[' ',' ',' '],
[' ',' ',' ']]

zeroMatrix = [
[0,0,0],
[0,0,0],
[0,0,0]]

o = 10
outputMatrix = [
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0]]


def printMatrix(matrix, n):
    for i in range(n):
        for j in range(n):
            print matrix[i][j],
        print

def matrixDiag1(matrix, n):
    diag1 = deepcopy(blankMatrix)
    for i in range(n):
        for j in range(n):
            if i==j:
                diag1[i][j] = matrix[i][j]
    return diag1

def matrixDiag2(matrix, n):
    diag2 = deepcopy(blankMatrix)
    for i in range(n):
        for j in range(n):
             if i+j==n-1:
                diag2[i][j] = matrix[i][j]
    return diag2

def spinMatrix(matrix, n):
    temp = deepcopy(matrix)
    for x in range (0, n):
        for y in range(n-1, -1, -1):
            temp[x][n-y-1] = matrix[y][x]
    return temp

def midrowFlip(matrix):
    rowReverse = matrix[::-1]
    return rowReverse

def matrixAB(matrixA, matrixB, n):
    AB = deepcopy(blankMatrix)
    for i in range(n):
        for j in range(n):
            AB[i][j] = matrixA[i][j] * matrixB[i][j]
    return AB

def netStrength(input):
    total = 0
    for row in input:
        total += sum(row)
    return total

def calcBinding(guestMatrix, hostRegion, numSpins, description):
    guestRotated = guestMatrix
    spins = numSpins + 1
    for i in range(spins):
        print "\nFor {} guest, spun {}-degrees:".format(description, i*90)
        if i != 0:
            guestRotated = spinMatrix(guestMatrix, g)
        printMatrix(guestRotated, g)
        netForce = netStrength(matrixAB(guestRotated, hostRegion, g))
        print "Net force = {} (over host-guest region).".format(netForce)
    return guestRotated

def fillOutput():
    fillMatrix = np.zeros((10,10), dtype=np.int)
    region = np.arange(1,7).reshape(3,3)
    x = 3
    y = 3
    fillMatrix[x:x+region.shape[0], y:y+region.shape[1]] = region
    return fillMatrix



#calcBinding(guestMatrix, hostMatrix, 0, "original")

"""
def scanHost(row, column):
    hostPosition = deepcopy(hostRegion)
    for i in range(row):
        for j in range(column):
            hostPosition[i][j] = zeroMatrix[i,j] + hostMatrix[i,j]
    return hostPosition

print("\n################################################################################")
print("\nThis is the HOST SURFACE:")
printMatrix(hostMatrix, h)
print("\nTarget HOST-REGION (from host surface):")
printMatrix(hostRegion, g)
print("\nORIGINAL GUEST (to bind to host surface):")
printMatrix(guestMatrix, g)

print("\n################################################################################")
print("### AIM: MOVE, FLIP and/or ROTATE GUEST so as to find the target HOST-REGION ###")
print("### NOTE: The more -ve the NET FORCE the stronger the HOST-GUEST interaction ###")
print("################################################################################")

calcBinding(guestMatrix, hostRegion, 4, 'orginal')

print("\n### This is a MID-ROW-FLIP of original guest ###")
flipGuest = midrowFlip(guestMatrix)
printMatrix(flipGuest, g)
calcRotamers(flipGuest, hostRegion, 4, 'flipped')
"""