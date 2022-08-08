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
tmp_time_1 = []
tmp_time_2 = []
e2e_runtime = []
e2e_runtime_1 = []
e2e_runtime_2 = []
full_time = []
reps = 10
for dim in dims:
    for i in range(reps):
        t = time.time_ns()
        p1 = subprocess.Popen(["python3", "overhead.py", str(dim)], stdout=PIPE)
        savestr=str(p1.communicate()[0]).split("\\n")
        e2e_runtime_1.append(time.time_ns() - t)
        if len(savestr) < 2:
            continue
        tmp_time_1.append(float(savestr[-2]))
        print("DaphneLib. Size "+str(dim)+"x"+str(dim)+". Repetition "+str(i+1)+" of "+str(reps))
    if dim == dims[0]:
        full_time.append(tmp_time_1[:reps])
        e2e_runtime.append(e2e_runtime_1[:reps])
    else:
        full_time.append(tmp_time_1[reps:])
        e2e_runtime.append(e2e_runtime_1[reps:])
    
    name.append("DaphneLib")
    size.append(str(dim))
    
os.chdir(PROTOTYPE_PATH)
for dim in dims:
    for i in range(reps):
        t = time.time_ns()
        p3 = subprocess.Popen(["build/bin/daphne","--vec", "add_sum_dd.daphne","dim="+str(dim)], stdout=PIPE)
        savestr=str(p3.communicate()[0]).replace("'","").split("\\n")
        e2e_runtime_2.append(time.time_ns() - t)
        tmp_time_2.append(float(savestr[-1]))
        print("DaphneDSL. Size "+str(dim)+"x"+str(dim)+". Repetition "+str(i+1)+" of "+str(reps))
    if dim == dims[0]:
        full_time.append(tmp_time_2[:reps])
        e2e_runtime.append(e2e_runtime_2[:reps])
    else:
        full_time.append(tmp_time_2[reps:])
        e2e_runtime.append(e2e_runtime_2[reps:])
        
    name.append("DaphneDSL")
    size.append(str(dim))

lib_overhead = pd.DataFrame({
    "size":size,
    "e2e_runtime":e2e_runtime,
    "time":full_time,
    "name": name
})

lib_overhead.to_csv("test/api/python/benchmarks/overhead.csv", index=False)
        

