from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
import time
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
tmp_time_1 = []
tmp_time_2 = []
tmp_time_3 = []
tmp_time_4 = []
e2e_runtime = []
e2e_runtime_1 = []
e2e_runtime_2 = []
e2e_runtime_3 = []
e2e_runtime_4 = []
gen_time_1 = []
gen_time_2 = []
gen_time_3 = []
gen_time_4 = []
gen_time = []
full_time = []
script = []
size  = []

for rep in range(reps):
    t = time.time_ns()
    p1 = subprocess.Popen(["python3", "kmeans_nn.py",str(r),str(f),str(c),str(i)], stdout=subprocess.PIPE)
    savestr=str(p1.communicate()[0]).split("\\n")
    e2e_runtime_1.append(time.time_ns()-t)
    print("Repetition "+str(rep+1)+" of "+str(reps))
    if len(savestr) < 2:
        continue
    tmp_time_1.append(float(savestr[-2]))
    gen_time_1.append(float(savestr[1]))
gen_time.append(gen_time_1)

e2e_runtime.append(e2e_runtime_1)
full_time.append(tmp_time_1)
print("kmeans_nn.py done")
script.append("Numpy")
size.append(str(r)+"x"+str(c))

for rep in range(reps):
    t = time.time_ns()
    p2 = subprocess.Popen(["python3", "kmeans_dd.py",str(r),str(f),str(c),str(i)], stdout=subprocess.PIPE)
    savestr=str(p2.communicate()[0]).split("\\n")
    e2e_runtime_2.append(time.time_ns()-t)
    tmp_time_2.append(float(savestr[3]))
    gen_time_2.append(float(savestr[5])+float(savestr[7]))
    print("Repetition "+str(rep+1)+" of "+str(reps))
gen_time.append(gen_time_2)
full_time.append(tmp_time_2)
e2e_runtime.append(e2e_runtime_2)
print("kmeans_dd.py done")
script.append("DaphneLib")
size.append(str(r)+"x"+str(c))

for rep in range(reps):
    t = time.time_ns()
    p3 = subprocess.Popen(["python3", "kmeans_nd.py",str(r),str(f),str(c),str(i)], stdout=subprocess.PIPE)
    savestr=str(p3.communicate()[0]).split("\\n")
    e2e_runtime_3.append(time.time_ns()-t)
    print("Repetition "+str(rep+1)+" of "+str(reps))
    tmp_time_3.append(float(savestr[5]))
    gen_time_3.append(float(savestr[1])+float(savestr[7])+float(savestr[9]))
gen_time.append(gen_time_3)
full_time.append(tmp_time_3)
e2e_runtime.append(e2e_runtime_3)
print("kmeans_nd.py done")
script.append("DaphneLib NumPy")
size.append(str(r)+"x"+str(c))

os.chdir(PROTOTYPE_PATH)
for rep in range(reps):
    t = time.time_ns()
    p3 = subprocess.Popen(["build/bin/daphne","--vec", "kmeans_dd.daphne",
    "r="+str(r),"f="+str(f),"c="+str(c),"i="+str(i)], stdout=subprocess.PIPE)
    savestr=str(p3.communicate()[0]).replace("'","").split("\\n")
    e2e_runtime_4.append(time.time_ns()-t)
    print("Repetition "+str(rep+1)+" of "+str(reps))
    tmp_time_4.append(float(savestr[-1]))
    gen_time_4.append(float(savestr[1])+float(savestr[3]))
gen_time.append(gen_time_4)
e2e_runtime.append(e2e_runtime_4)
full_time.append(tmp_time_4)
print("kmeans_dd.daphne done")
script.append("DaphneDSL")
size.append(str(r)+"x"+str(c))
kmns = pd.DataFrame({
    "size":size,
    "e2e": e2e_runtime,
    "script execution":full_time,
    "data generation":gen_time,
    "name": script})

kmns.to_csv("test/api/python/benchmarks/"+out, index=False)