# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017

@author: MJL
"""

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
print("\n(to be saved and indexed in an OUTPUT matrix)")

print("\nWhen the GUEST matrix is rotated by 90: ")
copyGuest90 = spinMatrix(copyGuest0, g)
printMatrix(copyGuest90, g)

print("\nThe FORCES between the HOST x 90-DEGREE GUEST are: ")
boundHostGuest90 = matrixAB(copyGuest90, hostRegion, g)
printMatrix(boundHostGuest90, g)

print("This gives a NET force of: ")
print netStrength(boundHostGuest90)


print("\nWhen the GUEST matrix is rotated by 90: ")
copyGuest180 = spinMatrix(copyGuest90, g)
printMatrix(copyGuest180, g)

print("\nThe FORCES between the HOST x 180-DEGREE GUEST are: ")
boundHostGuest180 = matrixAB(copyGuest180, hostRegion, g)
printMatrix(boundHostGuest180, g)

print("This gives a NET force of: ")
print netStrength(boundHostGuest180)


print("\nWhen the GUEST matrix is rotated by 90: ")
copyGuest270 = spinMatrix(copyGuest180, g)
printMatrix(copyGuest270, g)

print("\nThe FORCES between the HOST x 270-DEGREE GUEST are: ")
boundHostGuest270 = matrixAB(copyGuest270, hostRegion, g)
printMatrix(boundHostGuest270, g)

print("This gives a NET force of: ")
print netStrength(boundHostGuest270)


print("\nThe NET FORCES of GUESTS at all positions on HOST can be indexed as:")
printMatrix(outputMatrix, o)
print ("(the more -ve the greater the binding)")
print("\nThe above will be used to determine the best GUEST position(s) on HOST.")