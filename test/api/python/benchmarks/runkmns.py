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
add_time = []
for file in glob.glob("*.py"):
    yapp.clear()
    ykmn.clear()
    sum_tmp_time.clear()
    np_gen.clear()
    script_running.clear()
    data_gen_time.clear()

    if "runAllBenchmarks" in file or "plotAllBenchmarks" in file or "dsl_lib_overhead" in file:
           continue
    print(file)
    if "dnp" in file: 
                continue
    if "k-means" in file:

        print("Benchmarking started - filename: "+file)
        for j in range(0, 1):
                p = subprocess.Popen(["python3", file], stdout=PIPE)
                save_str = str(p.communicate()[-2])
                save_str = save_str.split("\\n")
                if "k-meansnp" in file:
                    ykmn.append(float(float(save_str[1]))/10**6)
                    np_genk.append(0)
                else:
                    ykmn.append(float(float(save_str[3])/10**6))
                    np_genk.append(float(float(save_str[2])))
                csvs = glob.glob(TMP_PATH+"/*.csv")
                for csv in csvs:
                    os.remove(csv)
        kmeans_runtime.append(statistics.median(ykmn))
        np_gen_allk.append(statistics.median(np_genk))
        kmeans_name.append(file)
        print("Benchmarking complete - filename: "+file)

os.chdir(PROTOTYPE_PATH)
res = [f for f in glob.glob("*.daphne") if "bm_kmeans" in f]

for prog in res:       
    print(prog)
    yapp = []
    for i in range(0, 1):
    
        p = subprocess.Popen(["build/bin/daphne", prog], stdout=PIPE)
        save_str = str(p.communicate()[-2])
        save_str = save_str.split('\\n')
        print(save_str)
        yapp.append(float(str(save_str[1]).replace("'","")))
    kmeans_runtime.append(statistics.median(yapp))
    kmeans_name.append(prog)
kmeans = pd.DataFrame({
    "kmeans_name":kmeans_name,
    "kmeans_runtime":kmeans_runtime})
kmeans.to_csv("test/api/python/benchmarks/kmeans.csv")