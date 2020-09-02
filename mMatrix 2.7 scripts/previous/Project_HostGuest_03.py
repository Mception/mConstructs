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

def printBinding(guestMatrix, hostRegion, numRotamers):
    tempGuest = guestMatrix
    tempHost = hostRegion
    
    print("\nBy scanning GUEST over HOST surface, a host-region could be: ")
    printMatrix(hostRegion, g)
 
    print("\nFor no GUEST-rotations, we get the GUEST(0) and NET force: ")
    copyGuest0 = guestMatrix
    printMatrix(copyGuest0, g)
    boundHostGuest0 = matrixAB(copyGuest0, hostRegion, g)
    print netStrength(boundHostGuest0)
    
    print("\nFor a 90-degree rotation, we get the GUEST(90) and NET force: ")
    copyGuest90 = spinMatrix(copyGuest0, g)
    printMatrix(copyGuest90, g)
    boundHostGuest90 = matrixAB(copyGuest90, hostRegion, g)
    print netStrength(boundHostGuest90)
    
    print("\nFor a 180-degree rotation, we get the GUEST(180) and NET force: ")
    copyGuest180 = spinMatrix(copyGuest90, g)
    printMatrix(copyGuest180, g)
    boundHostGuest180 = matrixAB(copyGuest180, hostRegion, g)
    print netStrength(boundHostGuest180)
    
    print("\nFor a 270-degree rotation, we get the GUEST(270) and NET force: ")
    copyGuest270 = spinMatrix(copyGuest180, g)
    printMatrix(copyGuest270, g)
    boundHostGuest270 = matrixAB(copyGuest270, hostRegion, g)
    print netStrength(boundHostGuest270)
    
    return tempGuest
    return tempHost

printBinding(guestMatrix, hostRegion, 3)

"""
print("\nThe HOST Matrix is: ")
printMatrix(hostMatrix, h)

print("\nWhich has a HOST (target) region of: ")
printMatrix(hostRegion, g)

print("\nThis target-region has a NET charge of: ")
print netStrength(hostRegion)

print("\nThe GUEST Matrix is: ")
printMatrix(guestMatrix, g)

print("\nWhich has a NET charge of: ")
print netStrength(guestMatrix)

print("\nThe guest matrix has the main diagonal: ")
diag1 = matrixDiag1(guestMatrix, g)
printMatrix(diag1, g)

print("\nAnd a second diagonal: ")
diag2 = matrixDiag2(guestMatrix, g)
printMatrix(diag2, g)

print("\nThe COLOUMBIC FORCES between HOST x GUEST interactions are: ")
boundHostGuest0 = matrixAB(guestMatrix, hostRegion, g)
printMatrix(boundHostGuest0, g)
print("(-ve = attraction; +ve = repulsion; 0 = neutral)")

print("\nThis gives a NET coloumbic binding or repelling force of: ")
print netStrength(boundHostGuest0)
print("(to be saved and indexed in an OUTPUT matrix)")

print("\nThe NET FORCES of GUESTS at all positions on HOST can be indexed as:")
printMatrix(outputMatrix, o)
print ("(the more -ve the greater the binding)")
print("\nThe above will be used to determine the best GUEST position(s) on HOST.")
"""