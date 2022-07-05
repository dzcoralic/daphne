from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
from time import sleep
from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import pandas as pd
import sys 
mat1 = str(sys.argv[1])
r = int(sys.argv[2])
c = int(sys.argv[3])
output = str(sys.argv[4])
reps = 10
tmp_time = []
full_time = []
script = []
size  = []
p = subprocess.Popen(["python3", "genData.py",mat1,str(r),str(c)], stdout=PIPE)
p.communicate()
sleep(1)
for i in range(reps):
    p1 = subprocess.Popen(["python3", "lm_np-big.py",mat1,str(r),str(c)], stdout=PIPE)
    savestr=str(p1.communicate()[0]).split("\\n")
    tmp_time.append(float(savestr[1]))
full_time.append(statistics.median(tmp_time))
tmp_time.clear()
script.append("full_numpy")
size.append(str(r)+"x"+str(c))
for i in range(reps):
    p2 = subprocess.Popen(["python3", "lm-big.py",mat1,str(r),str(c)], stdout=PIPE)
    savestr=str(p2.communicate()[0]).split("\\n")
    tmp_time.append(float(savestr[3])-float(savestr[5]))
full_time.append(statistics.median(tmp_time))
tmp_time.clear()
script.append("daphnelib")
size.append(str(r)+"x"+str(c))
os.chdir(PROTOTYPE_PATH)
for i in range(reps):
    p3 = subprocess.Popen(["build/bin/daphne","--vec", "bm_lm-big.daphne","mat1=\"test/api/python/benchmarks/"+mat1+"\"","r="+str(r),"c="+str(c)], stdout=PIPE)
    savestr=str(p3.communicate()[0]).replace("'","").split("\\n")    
    tmp_time.append(float(savestr[-1]))
full_time.append(statistics.median(tmp_time))
tmp_time.clear()
script.append("daphnedsl")
size.append(str(r)+"x"+str(c))
lm = pd.DataFrame({
    "size":size,
    "time":full_time,
    "name": script})

lm.to_csv("test/api/python/benchmarks/"+output)