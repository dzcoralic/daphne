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

os.environ['OPENBLAS_NUM_THREADS'] = '32'
reps = 10
tmp_time_1 = []
tmp_time_2 = []
tmp_time_3 = []
tmp_time_4 = []
gen_time_1 = []
gen_time_2 = []
gen_time_3 = []
gen_time_4 = []
gen_time = []
e2e_runtime_1 = []
e2e_runtime_2 = []
e2e_runtime_3 = []
e2e_runtime_4 = []
e2e_runtime = []
full_time = []
script = []
size  = []
print("Starting LM:")
print(".................................")
print("Starting pure NumPy implementation")
for rep in range(reps):
    t = time.time_ns()
    p1 = subprocess.Popen(["python3", "lm_nn.py",str(r),str(c)], stdout=PIPE)
    savestr=str(p1.communicate()[0]).split("\\n")
    e2e_runtime_1.append(time.time_ns()-t)
    if len(savestr) < 2:
        continue
    print("Repetition "+str(rep+1)+" of "+str(reps))
    tmp_time_1.append(float(savestr[-2]))
    gen_time_1.append(float(savestr[1]))

gen_time.append(gen_time_1)
if len(tmp_time_1) > 1:
    full_time.append(tmp_time_1)
else:
    full_time.append(0)

script.append("Pure NumPy")
size.append(str(r)+"x"+str(c))

os.environ['OPENBLAS_NUM_THREADS'] = '1'
print("Finished!")
print(".................................")
print("Starting NumPy + Daphne implementation")
for rep in range(reps):
    t = time.time_ns()
    p1 = subprocess.Popen(["python3", "lm_nd.py",str(r),str(c)], stdout=PIPE)
    savestr=str(p1.communicate()[0]).split("\\n")
    e2e_runtime_2.append(time.time_ns()-t)
    if len(savestr) < 2:
        continue
    print("Repetition "+str(rep+1)+" of "+str(reps))
    tmp_time_2.append(float(savestr[5]))
    gen_time_2.append(float(savestr[1])+float(savestr[4])+float(savestr[7]))
gen_time.append(gen_time_2)
if len(tmp_time_2) > 1:
    full_time.append(tmp_time_2)
else:
    full_time.append(0)
script.append("NumPy to DAPHNE")
size.append(str(r)+"x"+str(c))
print("Finished!")
print(".................................")
print("Starting pure daphnelib implementation")
for rep in range(reps):
    t = time.time_ns()
    p2 = subprocess.Popen(["python3", "lm_dd.py",str(r),str(c)], stdout=PIPE)
    savestr=str(p2.communicate()[0]).split("\\n")
    e2e_runtime_3.append(time.time_ns()-t)
    print("Repetition "+str(rep+1)+" of "+str(reps))
    tmp_time_3.append(float(savestr[3]))
    gen_time_3.append(float(savestr[5]))
gen_time.append(gen_time_3)
full_time.append(tmp_time_3)

script.append("Pure DaphneLib")
size.append(str(r)+"x"+str(c))
print("Finished!")
print(".................................")
print("Starting pure DaphneDSL implementation")
os.chdir(PROTOTYPE_PATH)
for rep in range(reps):
    t = time.time_ns()
    p3 = subprocess.Popen(["build/bin/daphne","--vec", "lm_dd.daphne","r="+str(r),"c="+str(c)], stdout=PIPE)
    savestr=str(p3.communicate()[0]).replace("'","").split("\\n")    
    e2e_runtime_4.append(time.time_ns()-t)
    tmp_time_4.append(float(savestr[-1]))
    print("Repetition "+str(rep+1)+" of "+str(reps))
    gen_time_4.append(float(savestr[1]))
gen_time.append(gen_time_4)
full_time.append(tmp_time_4)
e2e_runtime.append(e2e_runtime_1)
e2e_runtime.append(e2e_runtime_2)
e2e_runtime.append(e2e_runtime_3)
e2e_runtime.append(e2e_runtime_4)
script.append("Pure DaphneDSL")
size.append(str(r)+"x"+str(c))
print("Finished!")
print(".................................")
lm = pd.DataFrame({
    "size":size,
    "e2e":e2e_runtime,
    "script execution":full_time,
    "data generation":gen_time,
    "name": script})

lm.to_csv("test/api/python/benchmarks/"+out, index=False)