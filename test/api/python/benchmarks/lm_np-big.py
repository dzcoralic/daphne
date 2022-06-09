import time
import numpy as np
import sys 
r = 1000000
c = 1000
# Data generation.
XY = np.genfromtxt("mat1_k.csv", delimiter=",")
XY.shape = (r, c)

t = time.time_ns()
#XY = np.array(np.random.randint(100, size=r*c)+1.01, dtype=np.double)
#XY.shape=(r,c)
X = XY[:,range(c-1)]
y = XY[:, [c-1]]

X = (X-np.mean(X, 0)) / np.std(X, 0)

X = np.concatenate([X,np.ones((r,1))],1)

#X = np.c_[X, np.full((r,1),1)]

lmbda = np.full((c-1,1),0.001)

A = np.transpose(X) @ X + np.diag(lmbda)
b = np.transpose(X) @ y
beta = np.linalg.lstsq(A,b,rcond=None)
#print(beta)
print("fulltime:")
print(time.time_ns()-t)
