import numpy as np

r = 10000 
c = 1000
X = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
X.shape = (r,c)

Y = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
Y.shape = (r,c)
np.savetxt("mat1.csv",X , delimiter=',')
with open("mat1.csv.meta", "w") as f:
    f.write("10000,1000,1,f64")
    f.close()
np.savetxt("mat2.csv",Y , delimiter=',')
with open("mat2.csv.meta", "w") as f:
    f.write("10000,1000,1,f64")
    f.close()
r = 1000000 
c = 1000
X = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
X.shape = (r,c)
Y = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
Y.shape = (r,c)
np.savetxt("mat1_k.csv",X , delimiter=',')
np.savetxt("mat2_k.csv",Y , delimiter=',')
with open("mat1_k.csv.meta", "w") as f:
    f.write("1000000,1000,1,f64")
    f.close()
with open("mat2_k.csv.meta", "w") as f:
    f.write("1000000,1000,1,f64")
    f.close()
r = 100000 
c = 1000
X = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
X.shape = (r,c)
np.savetxt("mat1_lm.csv",X , delimiter=',')
with open("mat1_lm.csv.meta", "w") as f:
    f.write("100000,1000,1,f64")
    f.close()