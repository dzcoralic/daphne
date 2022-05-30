import os
import statistics
import glob

from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import subprocess 
from asyncio.subprocess import PIPE
import pandas as pd


x = []
y = []
z=[]
yapp = []

for file in glob.glob("*.py"):
    
    yapp.clear()
    if "rand" in file:
            print("Benchmarking started - filename: "+file)
            for i in range(0, 3, 2):
                 
                yapp.clear()
                for j in range(0, 1):
                    p = subprocess.Popen(["python3", file, str(10**(i*2))], stdout=PIPE)
                    save_str = str(p.communicate()[-2])
                    
                    save_str = save_str.split("\\n")
                    print(save_str)

                    if "rand.py" in file:
                        yapp.append(float(float(save_str[4])))
                        
                    csvs = glob.glob(TMP_PATH+"/*.csv")
                    for csv in csvs:
                        os.remove(csv)
                x.append(str(10**(i*2))+"x"+str(10**(i*2)))
                y.append(statistics.median(yapp))
                z.append(file)
            print("Benchmarking complete - filename: "+file)
    



os.chdir(PROTOTYPE_PATH)
res = [f for f in glob.glob("*.daphne") if "bm" in f]
for prog in res:
    if "rand" in prog:
        daphne_sum_tmp = []
        yapp = []
        for i in range(0, 10):
            p = subprocess.Popen(["build/bin/daphne", prog], stdout=PIPE)
            save_str = str(p.communicate()[-2])
            save_str = save_str.split('\\n')
            yapp.append(float(str(save_str[4]).replace("'","")))

        if "big" in prog:
            x.append("10000x10000")
        else:
            x.append("1x1")
        y.append(statistics.median(yapp))
        z.append(prog)
        print("Benchmarking complete - filename: "+prog)

lib_overhead = pd.DataFrame({
    "size":x,
    "time":y,
    "name": z
})

lib_overhead.to_csv("test/api/python/benchmarks/overhead.csv")
        

