import time
import numpy as np
import sys


mat1 = sys.argv[1]
mat2 = sys.argv[2]
r = int(sys.argv[3]) # and 1000000 # number of records (rows in X)
f = int(sys.argv[4])                 # number of features (columns in X and C)
c = int(sys.argv[5])                    # number of centroids (rows in C)
i = int(sys.argv[6])         # number of iterations

X = np.genfromtxt(mat1, delimiter=",")
C = np.genfromtxt(mat2, delimiter=",")
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
#print(C)
print("res: 0")
print(time.time_ns()-t)
