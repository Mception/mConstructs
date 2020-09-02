# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:55:05 2017

@author: MJL
"""

h = 12
hostMatrix = [[0,0,0,0,0,0,0,0,0,0,0,0],
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
guestMatrix = [[+1,-1,-1],
               [+1,+1,-1],
               [+1,-1,+1]]

hostRegion = [[-1,+1,+1],
              [-1,-1,+1],
              [-1,+1,-1]]

o = 10
outputMatrix = [[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]]


from copy import deepcopy

def printMatrix(matrix, n):
    for i in range(n):
        for j in range(n):
            print matrix[i][j],
        print

def matrix_main_diag(matrix, n):
    for i in range(n):
        for j in range(n):
            if i==j:
                print matrix[i][j],
        print
 
def matrix_sec_diag(matrix, n):
    for i in range(n):
        for j in range(n):
            if i+j==n-1:
                print matrix[i][j],
        print

def matrix_times_matrix(matrixA, matrixB, n):
    for i in range(n):
        for j in range(n):
            print matrixA[i][j] * matrixB[i][j],
        print

def spinMatrix(matrix, n):
    temp = deepcopy(matrix)
    for x in range (0, n):
        for y in range(n-1, -1, -1):
            temp[x][n-y-1] = matrix[y][x]
    return temp


print("\nThe Guest Matrix is: ")
printMatrix(guestMatrix, g)

print("\nThe Guest matrix has the main diagonal: ")
matrix_main_diag(guestMatrix, g)

print("\nAnd a secondary diagonal: ")
matrix_sec_diag(guestMatrix, g)

print("\nNow, the Host Matrix is: ")
printMatrix(hostMatrix, h)

print("\nWhere, the Best Host-Region is: ")
printMatrix(hostRegion, g)

print("\nSo, when Guest Matrix is: ")
printMatrix(guestMatrix, g)

print("\nThe Hadamard product of Guest x Host is: ")
matrix_times_matrix(guestMatrix, hostRegion, g)
print("(-ve = attraction; +ve = repulsion; 0 = neutral)")

print("\nThe Guest Matrix rotated by 90° is: ")
guestMatrix = spinMatrix(guestMatrix, g)
printMatrix(guestMatrix, g)

print("\nThe Guest Matrix rotated by 180° is: ")
guestMatrix = spinMatrix(guestMatrix, g)
printMatrix(guestMatrix, g)

print("\nThe Guest Matrix rotated by 270° is: ")
guestMatrix = spinMatrix(guestMatrix, g)
printMatrix(guestMatrix, g)

print("\nThe Host Matrix rotated by 90° is:\n(although not necessary really!)")
hostMatrix = spinMatrix(hostMatrix, h)
printMatrix(hostMatrix, h)

print("\nThe Net-Charge Output Matrix would be presented thus:\n(the more -ve the greater the binding)")
printMatrix(outputMatrix, o)