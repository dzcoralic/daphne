from asyncio.subprocess import PIPE
import glob, os
from re import sub
import statistics
import subprocess
from time import sleep
from api.python.utils.consts import PROTOTYPE_PATH, TMP_PATH
import pandas as pd
import sys 

print("Starting overhead benchmark:")
p = subprocess.Popen(["python3", "run_overhead.py"], stdout=subprocess.PIPE, universal_newlines=True)
print(str(p.communicate()[0]))
print("Overhead benchmark done")


print("Starting summation addition benchmark:")
p = subprocess.Popen(["python3", "run_addsum.py"], stdout=subprocess.PIPE, universal_newlines=True)
print(str(p.communicate()[0]))
print("Summation addition benchmark done")

print("Starting kmeans benchmark:")
p = subprocess.Popen(["python3", "kmeansrun.py", "mat1.csv", "mat2.csv", str(100000), str(1000), str(5), str(10), "kmeans1.csv"], stdout=subprocess.PIPE, universal_newlines=True)
print(str(p.communicate()[0]))
print("K-Means benchmark done")


print("Starting kmeans 2 benchmark:")
p = subprocess.Popen(["python3", "kmeansrun.py", "mat1.csv", "mat2.csv", str(1000000), str(1000), str(5), str(10), "kmeans2.csv"], stdout=subprocess.PIPE, universal_newlines=True)
print(str(p.communicate()[0]))
print("K-Means 2 benchmark done")

print("Starting lm benchmark:")
p = subprocess.Popen(["python3", "run_lm.py", str(100000), str(1000), "lm1.csv"], stdout=subprocess.PIPE, universal_newlines=True)
print(str(p.communicate()[0]))
print("LM benchmark done")

print("Starting lm 2 benchmark:")
p = subprocess.Popen(["python3", "run_lm.py", str(1000000), str(1000), "lm2.csv"], stdout=subprocess.PIPE, universal_newlines=True)
print(str(p.communicate()[0]))
print("LM 2 benchmark done")
if os.path.exists("mat1.csv"):
    os.remove("mat1.csv")
if os.path.exists("mat2.csv"):
    os.remove("mat2.csv")
if os.path.exists("mat1.csv.meta"):
    os.remove("mat1.csv.meta")
if os.path.exists("mat2.csv.meta"):
    os.remove("mat2.csv.meta")
