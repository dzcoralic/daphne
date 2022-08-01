from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
from time import sleep
from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import pandas as pd
import sys 

r = int(sys.argv[1]) # and 1000000 # number of records (rows in X)
f = int(sys.argv[2])                 # number of features (columns in X and C)
c = int(sys.argv[3])                    # number of centroids (rows in C)
i = int(sys.argv[4])         # number of iterations
out = sys.argv[5]
reps = 10
tmp_time = []
full_time = []
script = []
size  = []

for rep in range(reps):
    p1 = subprocess.Popen(["python3", "k-meansnp-big.py",str(r),str(f),str(c),str(i)], stdout=subprocess.PIPE)
    if rep == 0:
        continue
    savestr=str(p1.communicate()[0]).split("\\n")
    if len(savestr) < 2:
        continue
    print(savestr)
    tmp_time.append(float(savestr[1]))
full_time.append(statistics.median(tmp_time))
print()
tmp_time.clear()
script.append("Numpy")
size.append(str(r)+"x"+str(c))
for rep in range(reps):

    p2 = subprocess.Popen(["python3", "k-means-big.py",str(r),str(f),str(c),str(i)], stdout=subprocess.PIPE)
    if rep == 0:
        continue
    savestr=str(p2.communicate()[0]).split("\\n")
    print(savestr)
    tmp_time.append(float(savestr[3])-float(savestr[5])-float(savestr[7]))
full_time.append(statistics.median(tmp_time))
tmp_time.clear()
print()
script.append("DaphneLib")
size.append(str(r)+"x"+str(c))
for rep in range(reps):
    p3 = subprocess.Popen(["python3", "k-means-npd.py",str(r),str(f),str(c),str(i)], stdout=subprocess.PIPE)
    if rep == 0:
        continue
    savestr=str(p3.communicate()[0]).split("\\n")
    print(savestr)
    tmp_time.append(float(savestr[3]))
full_time.append(statistics.median(tmp_time))
tmp_time.clear()
print()
script.append("DaphneLib NumPy")
size.append(str(r)+"x"+str(c))
os.chdir(PROTOTYPE_PATH)
for rep in range(reps):
    p3 = subprocess.Popen(["build/bin/daphne","--vec", "bm_kmeans_big.daphne",
    "r="+str(r),"f="+str(f),"c="+str(c),"i="+str(i)], stdout=subprocess.PIPE)
    if rep == 0:
        continue
    savestr=str(p3.communicate()[0]).replace("'","").split("\\n")
    print(savestr)    
    tmp_time.append(float(savestr[-1]))

full_time.append(statistics.median(tmp_time))
tmp_time.clear()
script.append("DaphneDSL")
size.append(str(r)+"x"+str(c))
kmns = pd.DataFrame({
    "size":size,
    "time":full_time,
    "name": script})

kmns.to_csv("test/api/python/benchmarks/"+out)