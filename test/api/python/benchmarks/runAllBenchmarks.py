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
time_to_add = []
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

    if "sum" not in file and "rand.py" not in file:
           continue
    print(file)
    if "k-means" not in file:
        print("Benchmarking started - filename: "+file)
        for i in range(0, 8):
                    
            yapp.clear()
            ykmn.clear()
            sum_tmp_time.clear()
            np_gen.clear()
            script_running.clear()
            data_gen_time.clear()
            add_time.clear()
            for j in range(0, 10):
                p = subprocess.Popen(["python3", file, str(2**(i*2))], stdout=PIPE)
                save_str = str(p.communicate()[-2])
                save_str = save_str.split("\\n")
                print(save_str)
                if "sum_np" in file:
                    yapp.append(float(float(save_str[9])))
                    sum_tmp_time.append(float(save_str[3]))
                    np_gen.append(float(save_str[7]))
                    script_running.append(0)
                    add_time.append(float(save_str[1]))
                    data_gen_time.append(0)
                elif "daphne_np.py" in file:
                    add_time.append(float(save_str[4]))
                    yapp.append(float(float(save_str[8])))
                    sum_tmp_time.append(float(float(save_str[6])))
                    np_gen.append(float(save_str[2]))
                    script_running.append(0)
                    data_gen_time.append(0)
                elif "daphne_np_f.py" in file:
                    yapp.append(float(float(save_str[8])))
                    sum_tmp_time.append(float(float(save_str[6])))
                    add_time.append(float(save_str[4]))
                    np_gen.append(float(save_str[2]))
                    script_running.append(0)
                    data_gen_time.append(float(save_str[9].split(":")[1]))
                elif "sum_f" in file:
                    data_gen_time.append(float(save_str[1]))
                    add_time.append(float(save_str[3]))
                    sum_tmp_time.append(float(save_str[5]))
                    script_running.append(float(save_str[9]))
                    np_gen.append(float(0))
                    yapp.append(float(save_str[11]))
                elif "sum_c" in file:
                    data_gen_time.append(float(save_str[1]))
                    add_time.append(float(save_str[3]))
                    sum_tmp_time.append(float(save_str[5]))
                    np_gen.append(float(save_str[8]))
                    script_running.append(float(save_str[11]))
                    yapp.append(float(save_str[13]))
                else:
                    add_time.append(float(save_str[1]))
                    yapp.append(float(float(save_str[6])))
                    data_gen_time.append(0)
                    np_gen.append(0)
                    sum_tmp_time.append(float(save_str[3]))
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
            time_to_add.append(statistics.median(add_time))
            z.append(file)
            print(str((1+i)*12.5)+"%")
        print("Benchmarking complete - filename: "+file)
   
sumdataset = pd.DataFrame({
    "size":x,
    "time":y,
    "name": z,
    "summation_time":sum_time,
    "np_gen_time": np_gen_all,
    "data_gen_time": data_gen_all,
    "time_to_add": time_to_add
})

sumdataset.to_csv("sumdataset.csv")