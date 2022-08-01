import time
import numpy as np
import sys

r = int(sys.argv[1])
c = int(sys.argv[2]) 
# Data generation.
#XY = np.genfromtxt(mat1, delimiter=",")

#XY.shape = (r, c)

XY = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
XY.shape=(r,c)
t = time.time_ns()
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
