from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
from time import sleep

from numpy import rad2deg
from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import pandas as pd
import sys 
size = []
rands = [10000, 20000]
receive_np_tmp = []
receive_np = []
time_to_sum = []
time_to_sum_tmp = []
np_gen = []
np_gen_tmp = []
script_running_tmp = []
script_running = []
ftime_tmp = []
ftime = []
time_to_add_tmp = []
time_to_add = []
res_construct_tmp = []
res_construct = []
random_data_gen_tmp = []
random_data_gen = []
write_tmp = []
write = []
write_np_tmp = []
write_np = []
read_tmp = []
read = []
fname = []
reps = 10
for rand in rands:
    for i in range(reps):
        p1 = subprocess.Popen(["python3", "add_sum_nds.py",str(rand)], stdout=subprocess.PIPE)
        if i == 0:
            continue
        savestr=str(p1.communicate()[0]).split("\\n")
        if len(savestr) < 2:
            continue
      #  print(savestr)
        receive_np_tmp.append(float(savestr[1]))
        time_to_add_tmp.append(float(savestr[3]))
        time_to_sum_tmp.append(float(savestr[5]))
        np_gen_tmp.append(float(savestr[8]))
        script_running_tmp.append(float(savestr[11]))
        ftime_tmp.append(float(savestr[13]))
        print("Repetition "+str(i)+" of "+str(reps))
    print("Data transfer via ctypes FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    fname.append("Data transfer via ctypes")
    np_gen.append(statistics.median(np_gen_tmp))
    np_gen_tmp.clear()
    receive_np.append(statistics.median(receive_np_tmp))
    receive_np_tmp.clear()
    time_to_add.append(statistics.median(time_to_add_tmp))
    time_to_add_tmp.clear()
    time_to_sum.append(statistics.median(time_to_sum_tmp))
    time_to_sum_tmp.clear()
    script_running.append(statistics.median(script_running_tmp))
    script_running_tmp.clear()
    ftime.append(statistics.median(ftime_tmp))
    ftime_tmp.clear()
    random_data_gen.append(0)
    write.append(0)
    write_np.append(0)
    read.append(0)
    res_construct.append(0)
    size.append(rand)
for rand in rands:
    for i in range(reps):

        p2 = subprocess.Popen(["python3", "add_sum_dnf.py",str(rand)], stdout=subprocess.PIPE)
        if i == 0:
            continue
        savestr=str(p2.communicate()[0]).split("\\n")
     #   print(savestr)
        res_construct_tmp.append(float(savestr[2]))
        time_to_add_tmp.append(float(savestr[4]))
        time_to_sum_tmp.append(float(savestr[6]))
        random_data_gen_tmp.append(float(savestr[10]))
        write_tmp.append(float(savestr[12]))
        ftime_tmp.append(float(savestr[8]))
        print("Repetition "+str(i)+" of "+str(reps))
    print("Daphne gen , numpy summation, files transfer FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    fname.append("Data generated in Daphne, Operations in NumPy")
    res_construct.append(statistics.median(res_construct_tmp))
    res_construct_tmp.clear()
    time_to_add.append(statistics.median(time_to_add_tmp))
    time_to_add_tmp.clear()
    time_to_sum.append(statistics.median(time_to_sum_tmp))
    time_to_sum_tmp.clear()
    random_data_gen.append(statistics.median(random_data_gen_tmp))
    random_data_gen_tmp.clear()
    ftime.append(statistics.median(ftime_tmp))
    ftime_tmp.clear()
    write.append(statistics.median(write_tmp))
    write_tmp.clear()
    read.append(0)
    receive_np.append(0)
    np_gen.append(0)
    write_np.append(0)
    script_running.append(0)
    size.append(rand)    
for rand in rands:        
    for i in range(reps):
        p3 = subprocess.Popen(["python3", "add_sum_ndf.py",str(rand)], stdout=subprocess.PIPE)
        if i == 0:
            continue
        savestr=str(p3.communicate()[0]).split("\\n")
        
        print("Repetition "+str(i)+" of "+str(reps))
        read_tmp.append(float(savestr[1]))
        time_to_add_tmp.append(float(savestr[3]))
        time_to_sum_tmp.append(float(savestr[5]))
        write_np_tmp.append(float(savestr[8]))
        script_running_tmp.append(float(savestr[11]))
        ftime_tmp.append(float(savestr[13]))
    print("Data transfer via files FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    read.append(statistics.median(read_tmp))
    read_tmp.clear()
    time_to_add.append(statistics.median(time_to_add_tmp))
    time_to_add_tmp.clear()
    time_to_sum.append(statistics.median(time_to_sum_tmp))
    time_to_sum_tmp.clear()
    write_np.append(statistics.median(write_np_tmp))
    write_np_tmp.clear()
    script_running.append(statistics.median(script_running_tmp))
    script_running_tmp.clear()
    ftime.append(statistics.median(ftime_tmp))
    ftime_tmp.clear()
    res_construct.append(0)
    random_data_gen.append(0)
    receive_np.append(0)
    np_gen.append(0)
    size.append(rand)
    fname.append("Data Transfer via Files, Daphne to Numpy")
for rand in rands:        
    for i in range(reps):
        p3 = subprocess.Popen(["python3", "sum_dns.py",str(rand)], stdout=subprocess.PIPE)
        if i == 0:
            continue
        savestr=str(p3.communicate()[0]).split("\\n")
        res_construct_tmp.append(float(savestr[2]))
        time_to_add_tmp.append(float(savestr[4]))    
        time_to_sum_tmp.append(float(savestr[6]))
        ftime_tmp.append(float(savestr[8]))
        random_data_gen_tmp.append(float(savestr[10]))
        print("Repetition "+str(i)+" of "+str(reps))
    print("Data gen in daphne, sum in numpy FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    read.append(0)
    time_to_add.append(statistics.median(time_to_add_tmp))
    time_to_add_tmp.clear()
    time_to_sum.append(statistics.median(time_to_sum_tmp))
    time_to_sum_tmp.clear()
    write_np.append(0)
    script_running.append(0)
    ftime.append(statistics.median(ftime_tmp))
    ftime_tmp.clear()
    res_construct.append(0)
    random_data_gen.append(statistics.median(random_data_gen_tmp))
    receive_np.append(0)
    np_gen.append(0)
    size.append(rand)
    fname.append("Data-gen in daphne, sum in np")
for rand in rands:          
    for i in range(reps):
        p3 = subprocess.Popen(["python3", "sum_nn.py",str(rand)], stdout=subprocess.PIPE)
        if i == 0:
            continue
        savestr=str(p3.communicate()[0]).split("\\n")
        #print(savestr)
        print("Repetition "+str(i)+" of "+str(reps))
        time_to_add_tmp.append(float(savestr[1]))
        time_to_sum_tmp.append(float(savestr[3]))
        np_gen_tmp.append(float(savestr[7]))
        ftime_tmp.append(float(savestr[9]))
    print("Pure Numpy FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    read.append(0)
    time_to_add.append(statistics.median(time_to_add_tmp))
    time_to_add_tmp.clear()
    time_to_sum.append(statistics.median(time_to_sum_tmp))
    time_to_sum_tmp.clear()
    write_np.append(0)
    script_running.append(0)
    ftime.append(statistics.median(ftime_tmp))
    ftime_tmp.clear()
    res_construct.append(0)
    random_data_gen.append(0)
    receive_np.append(0)
    np_gen.append(statistics.median(np_gen_tmp))
    np_gen_tmp.clear()
    size.append(rand)
    fname.append("Pure Numpy")
os.chdir(PROTOTYPE_PATH)
for rand in rands:
    for i in range(reps):
        p3 = subprocess.Popen(["build/bin/daphne","--vec", "add_sum_dd.daphne","dim="+str(rand)], stdout=subprocess.PIPE)
        if i == 0:
            continue
        savestr=str(p3.communicate()[0]).replace("'","").split("\\n")
        #print(savestr)    
        print("Repetition "+str(i)+" of "+str(reps))
        random_data_gen_tmp.append(float(savestr[1]))
        time_to_add_tmp.append(float(savestr[3]))
        time_to_sum_tmp.append(float(savestr[5]))
        ftime_tmp.append(float(savestr[8]))
    print("DaphneDSL FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    read.append(0)
    time_to_add.append(statistics.median(time_to_add_tmp))
    time_to_add_tmp.clear()
    time_to_sum.append(statistics.median(time_to_sum_tmp))
    time_to_sum_tmp.clear()
    write_np.append(0)
    script_running.append(0)
    ftime.append(statistics.median(ftime_tmp))
    ftime_tmp.clear()
    res_construct.append(0)
    random_data_gen.append(statistics.median(random_data_gen_tmp))
    receive_np.append(0)
    np_gen.append(0)
    size.append(rand)
    fname.append("DaphneDSL")
dataset = pd.DataFrame({
    "size":size,
    "full time":ftime,
    "name": fname,
    "reading files":read,
    "time to add":time_to_add,
    "time to sum":time_to_sum,
    "writing numpy arr": write_np,
    "script running":script_running,
    "result construction":res_construct,
    "random data generation in daphne":random_data_gen,
    "numpy result recieved":receive_np,
    "numpy data generation":np_gen})

dataset.to_csv("test/api/python/benchmarks/addsum.csv")