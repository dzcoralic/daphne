from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
from time import sleep
from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import pandas as pd
import sys 
import time

r = int(sys.argv[1])
c = int(sys.argv[2])
out = sys.argv[3]

reps = 10
tmp_time_1 = []
tmp_time_2 = []
tmp_time_3 = []
tmp_time_4 = []
e2e_runtime_1 = []
e2e_runtime_2 = []
e2e_runtime_3 = []
e2e_runtime_4 = []
e2e_runtime = []
full_time = []
script = []
size  = []
for i in range(reps):
    t = time.time_ns()
    p1 = subprocess.Popen(["python3", "lm_nn.py",str(r),str(c)], stdout=PIPE)
    savestr=str(p1.communicate()[0]).split("\\n")
    e2e_runtime_1.append(time.time_ns()-t)
    if len(savestr) < 2:
        continue
    print(savestr)
    tmp_time_1.append(float(savestr[1]))
if len(tmp_time_1) > 1:
    full_time.append(tmp_time_1)
else:
    full_time.append(0)

print(full_time)
script.append("full_numpy")
size.append(str(r)+"x"+str(c))

for i in range(reps):
    t = time.time_ns()
    p1 = subprocess.Popen(["python3", "lm_nd.py",str(r),str(c)], stdout=PIPE)
    savestr=str(p1.communicate()[0]).split("\\n")
    e2e_runtime_2.append(time.time_ns()-t)
    if len(savestr) < 2:
        continue
    print(savestr)
    tmp_time_2.append(float(savestr[3])-float(savestr[5]))
if len(tmp_time_2) > 1:
    full_time.append(tmp_time_2)
else:
    full_time.append(0)
print(full_time)
script.append("np_daphne")
size.append(str(r)+"x"+str(c))
for i in range(reps):
    t = time.time_ns()
    p2 = subprocess.Popen(["python3", "lm_dd.py",str(r),str(c)], stdout=PIPE)
    savestr=str(p2.communicate()[0]).split("\\n")
    e2e_runtime_3.append(time.time_ns()-t)
    tmp_time_3.append(float(savestr[3])-float(savestr[5]))
    print(savestr)
full_time.append(tmp_time_3)

print(full_time)
script.append("daphnelib")
size.append(str(r)+"x"+str(c))
os.chdir(PROTOTYPE_PATH)
for i in range(reps):
    t = time.time_ns()
    p3 = subprocess.Popen(["build/bin/daphne","--vec", "lm_dd.daphne","r="+str(r),"c="+str(c)], stdout=PIPE)
    savestr=str(p3.communicate()[0]).replace("'","").split("\\n")    
    e2e_runtime_4.append(time.time_ns()-t)
    tmp_time_4.append(float(savestr[-1])-float(savestr[1]))
    print(savestr)
full_time.append(tmp_time_4)
e2e_runtime.append(e2e_runtime_1)
e2e_runtime.append(e2e_runtime_2)
e2e_runtime.append(e2e_runtime_3)
e2e_runtime.append(e2e_runtime_4)
script.append("daphnedsl")
size.append(str(r)+"x"+str(c))
lm = pd.DataFrame({
    "size":size,
    "e2e runtime":e2e_runtime,
    "time":full_time,
    "name": script})

lm.to_csv("test/api/python/benchmarks/"+out)