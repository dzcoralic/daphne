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
for file in glob.glob("*.py"):
    yapp.clear()
    ykmn.clear()
    if "runAllBenchmarks" in file or "plotAllBenchmarks" in file:
           continue
    if "k-means" not in file:
    
        print("Benchmarking started - filename: "+file)
        for i in range(0, 7):
            
            for j in range(0, 50):
                p = subprocess.Popen(["python3", file, str(2**(i*2))], stdout=PIPE)
                save_str = str(p.communicate()[-2])
                yapp.append(float(float(save_str.split("res: 0")[1].replace('\\n', "").replace("'", ""))/10**6))
                sum_tmp_time.append(float(save_str.split("res: 0")[0].split("sum:")[1].replace('\\n', "")))
                csvs = glob.glob(TMP_PATH+"/*.csv")
                for csv in csvs:
                    os.remove(csv)
            x.append(str(2**(i*2))+"x"+str(2**(i*2)))
            y.append(statistics.median(yapp))
            sum_time.append(statistics.median(sum_tmp_time))
            z.append(file)
            print(str((1+i)*12.5)+"%")
        print("Benchmarking complete - filename: "+file)
    else:
       	print("Benchmarking started - filename: "+file)
        
        for j in range(0, 50):
                p = subprocess.Popen(["python3", file], stdout=PIPE)
                ykmn.append(float(float(str(p.communicate()[-2]).split("res: 0")[1].replace('\\n', "").replace("'", ""))/10**6))
                csvs = glob.glob(TMP_PATH+"/*.csv")
                for csv in csvs:
                    os.remove(csv)
        kmeans_runtime.append(statistics.median(ykmn))
        kmeans_name.append(file)
        print("Benchmarking complete - filename: "+file)
      
sumdataset = pd.DataFrame({
    "size":x,
    "time":y,
    "name": z,
    "summation_time":sum_time,
})
daphne_progs = []
daphne_results = []
os.chdir(PROTOTYPE_PATH)
res = [f for f in glob.glob("*.daphne") if "bm" in f]
for prog in res:
    for i in range(0, 50):
        yapp = []
        p = subprocess.Popen(["build/bin/daphne", prog], stdout=PIPE)
        yapp.append(float(str(p.communicate()).split("Time input read: ")[1].split('ms')[0]))
    if "kmeans" not in prog:
            daphne_progs.append(prog)
            daphne_results.append(statistics.median(yapp))
    else:
            kmeans_runtime.append(statistics.median(yapp))
            kmeans_name.append(prog)
    print("Benchmarking complete - filename: "+prog)
      
daphneset = pd.DataFrame({
    "daphne_progs":daphne_progs,
    "daphne_results":daphne_results})

kmeans = pd.DataFrame({
    "kmeans_name":kmeans_name,
    "kmeans_runtime":kmeans_runtime})

sumdataset.to_csv("test/api/python/benchmarks/sumdataset.csv")
daphneset.to_csv("test/api/python/benchmarks/daphneset.csv")
kmeans.to_csv("test/api/python/benchmarks/kmeans.csv")
