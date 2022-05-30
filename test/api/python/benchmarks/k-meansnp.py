import time
import numpy as np
import sys


r=10000#100000 # and 1000000 # number of records (rows in X)
c=5                   # number of centroids (rows in C)
f=1000                 # number of features (columns in X and C)
i=10           # number of iterations

X = np.genfromtxt("mat1_.csv", delimiter=",")
C = np.genfromtxt("mat2.csv", delimiter=",")
X.shape = (r, f)
C.shape = (c, f)

t = time.time_ns()
for j in range(0,i):
    CC = np.power(C,2)
    CC = np.sum(CC,axis=1, keepdims=True)
    D = np.add(np.multiply(np.matmul(X, np.transpose(C)),-2.0),np.transpose(CC))
    minD = np.amin(D, axis=1, keepdims=True)

    P = (D <= minD).astype(int)
    P = np.divide(P, np.sum(P, axis=1, keepdims=True))

    P_denom = np.sum(P, axis=0, keepdims=True)

    pz = np.matmul(np.transpose(P),X)
    #np.seterr(invalid="ignore")
    C = np.divide((pz),np.transpose(P_denom))
print(C)
print("res: 0")
print(time.time_ns()-t)