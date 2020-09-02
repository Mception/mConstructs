# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:43:05 2017

@author: MJL
"""

"""
x = input("Type x value: ")
y = input("Type y value: ")

def basic_math(x, y):
    print(float(x + y))
    print(float(x - y))
    print(float(x * y))
    print(float(x / y))
    if x > y:
        print(int(x // y))
        print(x % y)
    else:
        print(int(y // x))
        print(y % x)
    
basic_math(x, y)
"""

n = int(raw_input("No. of rows: "))
m = int(raw_input("No. of columns: "))
a = [[input("Elements of matrix A: ") for j in range(m)] for i in range(n)]
b = [[input("Elements of matrix B: ") for j in range(m)] for i in range(n)]

def matrix():
    for i in range(n):
        for j in range(m):
            print a[i][j],
        print

def matrix_main_diag():
    for i in range(n):
        for j in range(m):
            if i==j:
                print a[i][j],
        print
 
def matrix_sec_diag():
    for i in range(n):
        for j in range(m):
            if i+j==2:
                print a[i][j],
        print

def matrix_plus_matrix():
    for i in range(n):
        for j in range(m):
            print a[i][j] + b[i][j],
        print

def matrix_times_matrix():
    for i in range(n):
        for j in range(m):
            print a[i][j] * b[i][j],
        print

print("\nYour matrix A is: ")       
matrix()
print("\nWhich has the main diagonal: ")
matrix_main_diag()
print("\nAnd a secondary diagonal: ")
matrix_sec_diag()

print("\nYour matrix B is: ")
for i in range(n):
    for j in range(m):
        print b[i][j],
    print
        
print("\nThe sum of matrix A + B is: ")
matrix_plus_matrix()

print("\nThe Hadamard product of matrix A x B is: ")
matrix_times_matrix()














