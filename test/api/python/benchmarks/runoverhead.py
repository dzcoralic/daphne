import os
import statistics
import glob

from numpy import full

from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import subprocess 
from asyncio.subprocess import PIPE
import pandas as pd
import time
from datetime import datetime
from timeit import timeit
x = []
y = []
z=[]
yapp = []
progtime=[]
ptime=[]
dims = [10,10000]
name = []
size = []
tmp_time = []
full_time = []
reps = 15
for dim in dims:
    for i in range(reps):
        p1 = subprocess.Popen(["python3", "rand.py", str(dim)], stdout=PIPE)
        savestr=str(p1.communicate()[0]).split("\\n")
        if len(savestr) < 2:
            continue
        tmp_time.append(float(savestr[-2]))
        print("DaphneLib. Size "+str(dim)+"x"+str(dim)+". Repetition "+str(i)+" of "+str(reps))
    full_time.append(statistics.median(tmp_time))
    tmp_time.clear()
    name.append("DaphneLib")
    size.append(str(dim))
    
os.chdir(PROTOTYPE_PATH)
for dim in dims:
    for i in range(reps):
        p3 = subprocess.Popen(["build/bin/daphne","--vec", "bm_rand_mat_gen.daphne","dim="+str(dim)], stdout=PIPE)
        savestr=str(p3.communicate()[0]).replace("'","").split("\\n")
        tmp_time.append(float(savestr[-1]))
        print("DaphneDSL. Size "+str(dim)+"x"+str(dim)+". Repetition "+str(i)+" of "+str(reps))
    full_time.append(statistics.median(tmp_time))
    tmp_time.clear()
    name.append("DaphneDSL")
    size.append(str(dim))

lib_overhead = pd.DataFrame({
    "size":size,
    "time":full_time,
    "name": name
})

lib_overhead.to_csv("test/api/python/benchmarks/overhead.csv")
        

