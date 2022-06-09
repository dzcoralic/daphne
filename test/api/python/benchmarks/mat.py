import numpy as np
r = 5
c = 5
X = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
X.shape = (r,c)
np.savetxt("mat.csv",X , delimiter=',')
with open("mat.csv.meta", "w") as f:
    f.write("5,5,1,f64")
    f.close()