from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import pandas as pd
x = []
y = []
z=[]
yapp = []
ykmn = []
kmeans_name = []
kmeans_runtime = []
sum_tmp_time = []
sum_time = []
np_gen = []
np_gen_all = []
np_genk = []
np_gen_allk = []
script_running = []
data_gen_time = []
compute = []
data_gen_all = []
for file in glob.glob("*.py"):
    yapp.clear()
    ykmn.clear()
    sum_tmp_time.clear()
    np_gen.clear()
    script_running.clear()
    data_gen_time.clear()
    if "runAllBenchmarks" in file or "plotAllBenchmarks" in file:
           continue
    if "k-means" not in file:
    
        print("Benchmarking started - filename: "+file)
        for i in range(0, 8):
                    
            yapp.clear()
            ykmn.clear()
            sum_tmp_time.clear()
            np_gen.clear()
            script_running.clear()
            data_gen_time.clear()
            for j in range(0, 10):
                p = subprocess.Popen(["python3", file, str(2**(i*2))], stdout=PIPE)
                save_str = str(p.communicate()[-2])
                save_str = save_str.split("\\n")
                print(save_str)
                if "sum_np" in file:
                    yapp.append(float(float(save_str[7])))
                    sum_tmp_time.append(float(save_str[1]))
                    np_gen.append(float(save_str[5]))
                    script_running.append(0)
                    data_gen_time.append(0)
                elif "daphne_np" in file:
                    yapp.append(float(float(save_str[6])))
                    sum_tmp_time.append(float(float(save_str[4])))
                    np_gen.append(float(save_str[2]))
                    script_running.append(0)
                    data_gen_time.append(0)
                elif "sum_f" in file:
                    data_gen_time.append(float(save_str[1]))
                    sum_tmp_time.append(float(save_str[3]))
                    script_running.append(float(save_str[7]))
                	np_gen.append(float(save_str[6]))
                    yapp.append(float(save_str[9]))
                elif "sum_c" in file:
                	data_gen_time.append(float(save_str[1]))
                	sum_tmp_time.append(float(save_str[3]))
                	np_gen.append(float(save_str[6]))
                	script_running.append(float(save_str[9]))
                	yapp.append(float(save_str[11]))
                else:
                    yapp.append(float(float(save_str[4])))
                    data_gen_time.append(0)
                    np_gen.append(0)
                    sum_tmp_time.append(float(save_str[1]))
                    script_running.append(0)
                csvs = glob.glob(TMP_PATH+"/*.csv")
                for csv in csvs:
                    os.remove(csv)
            x.append(str(2**(i*2))+"x"+str(2**(i*2)))
            y.append(statistics.median(yapp))
            sum_time.append(statistics.median(sum_tmp_time))
            np_gen_all.append(statistics.median(np_gen))
            data_gen_all.append(statistics.median(data_gen_time))
            compute.append(statistics.median(script_running))
            z.append(file)
            print(str((1+i)*12.5)+"%")
        print("Benchmarking complete - filename: "+file)
    else:
      
       	print("Benchmarking started - filename: "+file)
        
        for j in range(0, 1):
                p = subprocess.Popen(["python3", file], stdout=PIPE)
                save_str = str(p.communicate()[-2])
                print(save_str.split("\\n"))
                ykmn.append(float(float(save_str.split("\\n")[3])/10**6))
                np_genk.append(float(float(save_str.split("\\n")[2])))
                csvs = glob.glob(TMP_PATH+"/*.csv")
                for csv in csvs:
                    os.remove(csv)
        kmeans_runtime.append(statistics.median(ykmn))
        np_gen_allk.append(statistics.median(np_genk))
        kmeans_name.append(file)
        print("Benchmarking complete - filename: "+file)
      
sumdataset = pd.DataFrame({
    "size":x,
    "time":y,
    "name": z,
    "summation_time":sum_time,
    "np_gen_time": np_gen_all,
    "data_gen_time": data_gen_all
})

daphne_progs = []
daphne_results = []
daphne_progs_sum = []
os.chdir(PROTOTYPE_PATH)
res = [f for f in glob.glob("*.daphne") if "bm" in f]
for prog in res:
    daphne_sum_tmp = []
    yapp = []
    for i in range(0, 10):
    
        p = subprocess.Popen(["build/bin/daphne", prog], stdout=PIPE)
        save_str = str(p.communicate()[-2])
        save_str = save_str.split('\\n')
        print(save_str)
    if "kmeans" not in prog:
        if "big" not in prog:
          yapp.append(float(str(save_str[1]).replace("'","")))
        else:
          yapp.append(float(str(save_str[4]).replace("'","")))
        daphne_sum_tmp.append(float(save_str[1]))
    else:
            yapp.append(float(str(save_str[1]).replace("'","")))
    if "kmeans" not in prog:
        daphne_progs.append(prog)
        daphne_results.append(statistics.median(yapp))
        daphne_progs_sum.append(statistics.median(daphne_sum_tmp))
    else:
            kmeans_runtime.append(statistics.median(yapp))
            kmeans_name.append(prog)
    
    print("Benchmarking complete - filename: "+prog)
      
daphneset = pd.DataFrame({
    "daphne_progs":daphne_progs,
    "daphne_results":daphne_results,
    "daphne_sum":daphne_progs_sum})

kmeans = pd.DataFrame({
    "kmeans_name":kmeans_name,
    "kmeans_runtime":kmeans_runtime})

sumdataset.to_csv("test/api/python/benchmarks/sumdataset.csv")
daphneset.to_csv("test/api/python/benchmarks/daphneset.csv")
kmeans.to_csv("test/api/python/benchmarks/kmeans.csv")
