import numpy as np
import sys

mat = sys.argv[1]
r = int(sys.argv[2])
c = int(sys.argv[3])
X = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
X.shape = (r,c)
np.savetxt(mat,X, delimiter=',')
with open(mat+".meta", "w") as f:
    f.write(str(r)+","+str(c)+",1,f64")
    f.close()