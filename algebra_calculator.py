#!/usr/bin/env python
# coding: utf-8

print("Author: Georgios Koliou\nContact: georgios.koliou@gmail.com\n\n")

# The library used for this purpose, Numpy
import numpy as np

# Rows x Columns
R = int(input("Give number of rows: "))
C = int(input("\nGive number of columns: "))

# The user enters all the numbers of the matrix from the keyboard.
print("\nInsert all the elements: ")
num = list(map(int, input().split()))

matrix = np.array(num).reshape(R, C)
if R==C:
    print("\nThe inserted matrix is square and is the following:\n\n",matrix,)
else:
    print("\nThe inserted matrix has dimensions (",R,"x",C,") and is the following:\n\n",matrix,)

# This method calculates the determinant with LU factorization
# The determinant is calculated only for square matrices
# If rows == columns det is calculated, otherwise no
if R==C:
    det = np.linalg.det(matrix)
    print("\nThe Determinant is: "'{0:.0f}'.format(det))
else:
    print("\nThe Determinant is: The matrix is not square!")

# If inserted matrix is not square, trace is not calculated
if R==C:
    tr = np.trace(matrix)
    print("\nTrace is: ",tr,)
else:
    print("\nTrace is equal: The matrix is not square!")

trasp = matrix.transpose()
print("\nThe Transpose of the matrix is:\n\n",trasp,)

# A matrix is invertible if its determinant is different from 0, otherwise no.
if R==C and det != 0:
    from numpy.linalg import inv
    inverse = inv(matrix)
    print("\nDeterminant equal ",'{0:.0f}'.format(det),"!=0, therefore the matrix is invertible and its inverse is equal:\n\n",inverse,)
    #print(colored("\nDeterminant equal ",'{0:.0f}'.format(det),"!=0, therefore the matrix is invertible and its inverse is equal:\n\n",'red'))
    #print(inverse)
    matver = np.matmul(matrix, inverse)    # VERIFICATION. A*A^-1 = I
    print("\nVERIFICATION: Must be printed identity matrix (",R,"x",C,").\n\n",matver,)
       
elif R != C:
    print("\nThe matrix is not invertible because: It is not square, has",R,"rows and",C,"columns\n")
    
else:
    print("\nThe matrix is not invertible because its determinant is equal to 0.")

x = np.identity(R)
#diag = np.diag(matrice)
if matver.any == x.any:
    print('True')
else:
    print('False')

np.identity(R)

# Rank is equals with number of rows linearly independent
from numpy.linalg import matrix_rank
rk = matrix_rank(matrix) 
print("\nRank is equals to: ",rk,)

input('\n\n\nPress ENTER to exit')