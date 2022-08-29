import os
import subprocess

from api.python.utils.consts import PROTOTYPE_PATH
import pandas as pd
import time
size = []
rands = [10000, 20000, 100]
receive_np_1 = []
receive_np_2 = []
receive_np_3 = []
receive_np_4 = []
receive_np_5 = []
receive_np_6 = []
receive_np = []
time_to_sum = []
time_to_sum_1 = []
time_to_sum_2 = []
time_to_sum_3 = []
time_to_sum_4 = []
time_to_sum_5 = []
time_to_sum_6 = []
ftime_1 = []
ftime_2 = []
ftime_3 = []
ftime_4 = []
ftime_5 = []
ftime_6 = []
ftime = []
time_to_add_1 = []
time_to_add_2 = []
time_to_add_3 = []
time_to_add_4 = []
time_to_add_5 = []
time_to_add_6 = []
time_to_add = []
random_data_gen_1 = []
random_data_gen_2 = []
random_data_gen_3 = []
random_data_gen_4 = []
random_data_gen_5 = []
random_data_gen_6 = []
random_data_gen = []
write_1 = []
write_2 = []
write_3 = []
write_4 = []
write_5 = []
write_6 = []
write = []
write_np_1 = []
write_np_2 = []
write_np_3 = []
write_np_4 = []
write_np_5 = []
write_np_6 = []
write_np = []
read_1 = []
read_2 = []
read_3 = []
read_4 = []
read_5 = []
read_6 = []
e2e_runtime_1 = []
e2e_runtime_2 = []
e2e_runtime_3 = []
e2e_runtime_4 = []
e2e_runtime_5 = []
e2e_runtime_6 = []
e2e_runtime = []
read = []
fname = []
reps = 10
for rand in rands:
    for i in range(reps):
        t = time.time_ns()
        p1 = subprocess.Popen(["python3", "add_sum_nds.py",str(rand)], stdout=subprocess.PIPE)
        savestr=str(p1.communicate()[0]).split("\\n")
        e2e_runtime_1.append(time.time_ns()-t)
        if len(savestr) < 2:
            continue
        #print(savestr)
        receive_np_1.append(float(savestr[1]))
        time_to_add_1.append(float(savestr[3]))
        time_to_sum_1.append(float(savestr[5]))
        random_data_gen_1.append(float(savestr[8]))
        ftime_1.append(float(savestr[11]))
        print("Repetition "+str(i+1)+" of "+str(reps))
    write_np.append(0)
    read.append(0)
    size.append(rand)
    fname.append("NumPy to DAPHNE via shared memory")
    
    if rand == rands[0]:

        e2e_runtime.append(e2e_runtime_1[:reps])
        random_data_gen.append(random_data_gen_1[:reps])
        receive_np.append(receive_np_1[:reps])
        time_to_add.append(time_to_add_1[:reps])
        time_to_sum.append(time_to_sum_1[:reps])
        ftime.append(ftime_1[:reps])
   
    if rand == rands[1]:
        e2e_runtime.append(e2e_runtime_1[reps:2*reps])
        random_data_gen.append(random_data_gen_1[reps:2*reps])
        receive_np.append(receive_np_1[reps:2*reps])
        time_to_add.append(time_to_add_1[reps:2*reps])
        time_to_sum.append(time_to_sum_1[reps:2*reps])
        ftime.append(ftime_1[reps:2*reps])

    if rand == rands[2]:
        e2e_runtime.append(e2e_runtime_1[2*reps:])
        random_data_gen.append(random_data_gen_1[2*reps:])
        receive_np.append(receive_np_1[2*reps:])
        time_to_add.append(time_to_add_1[2*reps:])
        time_to_sum.append(time_to_sum_1[2*reps:])
        ftime.append(ftime_1[2*reps:])
    print("Data transfer via shared memory FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    

for rand in rands:
    for i in range(reps):
        t = time.time_ns()
        if rand != rands[1]:    
            p2 = subprocess.Popen(["python3", "add_sum_dnf.py",str(rand)], stdout=subprocess.PIPE)
            savestr=str(p2.communicate()[0]).split("\\n")
        e2e_runtime_2.append(time.time_ns()-t)
   
     #   print(savestr)
        if rand == rands[0] or rand == rands[2]:
            read_2.append(float(savestr[2]))
            time_to_add_2.append(float(savestr[4]))
            time_to_sum_2.append(float(savestr[6]))
            random_data_gen_2.append(float(savestr[10]))
            write_2.append(float(savestr[12]))
            ftime_2.append(float(savestr[8]))
            print("Repetition "+str(i+1)+" of "+str(reps))
        if rand == rands[1]:
            read_2.append(0)
            time_to_add_2.append(0)
            time_to_sum_2.append(0)
            random_data_gen_2.append(0)
            write_2.append(0)
            ftime_2.append(0)
            print("Repetition "+str(i+1)+" of "+str(reps))
    
    receive_np.append(0)
    size.append(rand)    
    fname.append("DAPHNE to NumPy via files")
    
    if rand == rands[0]:
        e2e_runtime.append(e2e_runtime_2[:reps])
        read.append(read_2[:reps])
        time_to_add.append(time_to_add_2[:reps])
        time_to_sum.append(time_to_sum_2[:reps])
        random_data_gen.append(random_data_gen_2[:reps])
        ftime.append(ftime_2[:reps])
        write_np.append(write_2[:reps])
    
    if rand == rands[2]:
        e2e_runtime.append(e2e_runtime_2[reps*2:])
        read.append(read_2[reps*2:])
        time_to_add.append(time_to_add_2[reps*2:])
        time_to_sum.append(time_to_sum_2[reps*2:])
        random_data_gen.append(random_data_gen_2[reps*2:])
        ftime.append(ftime_2[reps*2:])
        write_np.append(write_2[reps*2:])
    
    if rand == rands[1]:
        e2e_runtime.append(e2e_runtime_2[reps:reps*2])
        read.append(read_2[reps:reps*2])
        time_to_add.append(time_to_add_2[reps:reps*2])
        time_to_sum.append(time_to_sum_2[reps:reps*2])
        random_data_gen.append(random_data_gen_2[reps:reps*2])
        ftime.append(ftime_2[reps:reps*2])
        write_np.append(write_np_2[reps:reps*2])
    print("Daphne gen , numpy summation, files transfer FINISHED. Matrix size "+str(rand)+"x"+str(rand))
        
for rand in rands:        
    for i in range(reps):
        t = time.time_ns()
        if rand != rands[1]:
            p3 = subprocess.Popen(["python3", "add_sum_ndf.py",str(rand)], stdout=subprocess.PIPE)
            savestr=str(p3.communicate()[0]).split("\\n")
            #print(savestr)
        e2e_runtime_3.append(time.time_ns()-t)
        print("Repetition "+str(i+1)+" of "+str(reps))
        if rand == rands[0] or rand == rands[2]:
            read_3.append(float(savestr[1]))
            time_to_add_3.append(float(savestr[3]))
            time_to_sum_3.append(float(savestr[5]))
            random_data_gen_3.append(float(savestr[8]))
            write_np_3.append(float(savestr[10]))
            ftime_3.append(float(savestr[13]))
        if rand == rands[1]:
            read_3.append(0)
            time_to_add_3.append(0)
            time_to_sum_3.append(0)
            write_np_3.append(0)
            ftime_3.append(0)
        
    receive_np.append(0)
    size.append(rand)
    fname.append("NumPy to DAPHNE via files")

    if rand == rands[0]:
        random_data_gen.append(random_data_gen_3[:reps])
        e2e_runtime.append(e2e_runtime_3[:reps])
        read.append(read_3[:reps])
        time_to_add.append(time_to_add_3[:reps])
        time_to_sum.append(time_to_sum_3[:reps])
        write_np.append(write_np_3[:reps])
        ftime.append(ftime_3[:reps])
    print("Data transfer via files FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    
    if rand == rands[2]:
        random_data_gen.append(random_data_gen_3[reps*2:])
        e2e_runtime.append(e2e_runtime_3[reps*2:])
        read.append(read_3[reps*2:])
        time_to_add.append(time_to_add_3[reps*2:])
        time_to_sum.append(time_to_sum_3[reps*2:])
        write_np.append(write_np_3[reps*2:])
        ftime.append(ftime_3[reps*2:])

    if rand == rands[1]:
        e2e_runtime.append(e2e_runtime_3[reps:reps*2])
        read.append(read_3[reps:reps*2])
        time_to_add.append(time_to_add_3[reps:reps*2])
        time_to_sum.append(time_to_sum_3[reps:reps*2])
        write_np.append(write_np_3[reps:reps*2])
        ftime.append(ftime_3[reps:reps*2])
        random_data_gen.append(random_data_gen_3[reps:reps*2])

for rand in rands:        
    for i in range(reps):
        t = time.time_ns()
        p3 = subprocess.Popen(["python3", "add_sum_dns.py",str(rand)], stdout=subprocess.PIPE)
        savestr=str(p3.communicate()[0]).split("\\n")
        e2e_runtime_4.append(time.time_ns()-t)
        read_4.append(float(savestr[2]))
        time_to_add_4.append(float(savestr[4]))    
        time_to_sum_4.append(float(savestr[6]))
        ftime_4.append(float(savestr[8]))
        random_data_gen_4.append(float(savestr[10]))
        print("Repetition "+str(i+1)+" of "+str(reps))
    write_np.append(0)
    receive_np.append(0)
    print("Data gen in daphne, sum in numpy FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    size.append(rand)

    if rand == rands[0]:

        e2e_runtime.append(e2e_runtime_4[:reps])
        time_to_add.append(time_to_add_4[:reps])
        time_to_sum.append(time_to_sum_4[:reps])
        ftime.append(ftime_4[:reps])
        random_data_gen.append(random_data_gen_4[:reps])
        read.append(read_4[:reps])
    if rand == rands[1]:
        e2e_runtime.append(e2e_runtime_4[reps:reps*2])
        time_to_add.append(time_to_add_4[reps:reps*2])
        time_to_sum.append(time_to_sum_4[reps:reps*2])
        ftime.append(ftime_4[reps:reps*2])
        random_data_gen.append(random_data_gen_4[reps:reps*2])
        read.append(read_4[reps:reps*2])

    if rand == rands[2]:
        e2e_runtime.append(e2e_runtime_4[reps*2:])
        time_to_add.append(time_to_add_4[reps*2:])
        time_to_sum.append(time_to_sum_4[reps*2:])
        ftime.append(ftime_4[reps*2:])
        random_data_gen.append(random_data_gen_4[reps*2:])
        read.append(read_4[reps*2:])
    fname.append("DAPHNE to NumPy via shared memory")

for rand in rands:          
    for i in range(reps):
        t = time.time_ns()
        p3 = subprocess.Popen(["python3", "add_sum_nn.py",str(rand)], stdout=subprocess.PIPE)
        savestr=str(p3.communicate()[0]).split("\\n")
        e2e_runtime_5.append(time.time_ns() - t)
        # print(savestr)
        print("Repetition "+str(i+1)+" of "+str(reps))
        time_to_add_5.append(float(savestr[1]))
        time_to_sum_5.append(float(savestr[3]))
        random_data_gen_5.append(float(savestr[7]))
        ftime_5.append(float(savestr[9]))
    print("Pure Numpy FINISHED. Matrix size "+str(rand)+"x"+str(rand))
    read.append(0)
    write_np.append(0)
    receive_np.append(0)
    fname.append("Pure NumPy")
    size.append(rand)
    
    if rand == rands[0]:
        e2e_runtime.append(e2e_runtime_5[:reps])
        time_to_add.append(time_to_add_5[:reps])
        time_to_sum.append(time_to_sum_5[:reps])
        ftime.append(ftime_5[:reps])
        random_data_gen.append(random_data_gen_5[:reps])
    if rand == rands[1]:
        e2e_runtime.append(e2e_runtime_5[reps:reps*2])
        time_to_add.append(time_to_add_5[reps:reps*2])
        time_to_sum.append(time_to_sum_5[reps:reps*2])
        ftime.append(ftime_5[reps:reps*2])
        random_data_gen.append(random_data_gen_5[reps:reps*2])
    if rand == rands[2]:
        e2e_runtime.append(e2e_runtime_5[reps*2:])
        time_to_add.append(time_to_add_5[reps*2:])
        time_to_sum.append(time_to_sum_5[reps*2:])
        ftime.append(ftime_5[reps*2:])
        random_data_gen.append(random_data_gen_5[reps*2:])

for rand in rands:
    for i in range(reps):
        t = time.time_ns()
        p1 = subprocess.Popen(["python3", "add_sum_dd.py",str(rand)], stdout=subprocess.PIPE)
        savestr=str(p1.communicate()[0]).split("\\n")
        #print(savestr)
        e2e_runtime_6.append(time.time_ns()-t)
        if len(savestr) < 2:
            continue
        time_to_add_6.append(float(savestr[3]))
        time_to_sum_6.append(float(savestr[5]))
        random_data_gen_6.append(float(savestr[1]))
        ftime_6.append(float(savestr[9]))
        print("Repetition "+str(i+1)+" of "+str(reps))
    receive_np.append(0)
    write_np.append(0)
    read.append(0)
    size.append(rand)
    fname.append("Pure DaphneLib")
    
    if rand == rands[0]:

        e2e_runtime.append(e2e_runtime_6[:reps])
        random_data_gen.append(random_data_gen_6[:reps])
        time_to_add.append(time_to_add_6[:reps])
        time_to_sum.append(time_to_sum_6[:reps])
        ftime.append(ftime_6[:reps])
   
    if rand == rands[1]:
        e2e_runtime.append(e2e_runtime_6[reps:reps*2])
        random_data_gen.append(random_data_gen_6[reps:reps*2])
        time_to_add.append(time_to_add_6[reps:reps*2])
        time_to_sum.append(time_to_sum_6[reps:reps*2])
        ftime.append(ftime_6[reps:reps*2])
           
    if rand == rands[2]:
        e2e_runtime.append(e2e_runtime_6[reps*2:])
        random_data_gen.append(random_data_gen_6[reps*2:])
        time_to_add.append(time_to_add_6[reps*2:])
        time_to_sum.append(time_to_sum_6[reps*2:])
        ftime.append(ftime_6[reps*2:])
    print("Pure DaphneLib finished. Matrix size "+str(rand)+"x"+str(rand))
    
        
dataset = pd.DataFrame({
    "size":size,
    "end-to-end": e2e_runtime,
    "script execution":ftime,
    "name": fname,
    "transfer receiver":read,
    "add":time_to_add,
    "sum":time_to_sum,
    "transfer sender": write_np,
    "data generation":random_data_gen,
    "numpy result recieved":receive_np})

dataset.to_csv("addsum.csv", index=False)