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
p = subprocess.Popen(["python3", "runoverhead.py"], stdout=subprocess.PIPE)
p.communicate()
print("Overhead benchmark done")


print("Starting summation addition benchmark:")
p = subprocess.Popen(["python3", "runsum.py"], stdout=subprocess.PIPE)
p.communicate()
print("Summation addition benchmark done")

print("Starting kmeans benchmark:")
p = subprocess.Popen(["python3", "kmeans.py", "mat1.csv", "mat2.csv", str(10000), str(1000), str(5), str(10)], stdout=subprocess.PIPE)
p.communicate()
print("K-Means benchmark done")


print("Starting kmeans 2 benchmark:")
p = subprocess.Popen(["python3", "kmeans.py", "mat1.csv", "mat2.csv", str(1000000), str(1000), str(5), str(10)], stdout=subprocess.PIPE)
p.communicate()
print("K-Means 2 benchmark done")

print("Starting lm benchmark:")
p = subprocess.Popen(["python3", "lm.py", "mat1.csv", str(10000), str(1000)], stdout=subprocess.PIPE)
p.communicate()
print("LM benchmark done")

print("Starting lm 2 benchmark:")
p = subprocess.Popen(["python3", "lm.py", "mat1.csv", str(1000000), str(1000)], stdout=subprocess.PIPE)
p.communicate()
print("LM 2 benchmark done")
if os.path.exists("mat1.csv"):
    os.remove("mat1.csv")
if os.path.exists("mat2.csv"):
    os.remove("mat2.csv")
if os.path.exists("mat1.csv.meta"):
    os.remove("mat1.csv.meta")
if os.path.exists("mat2.csv.meta"):
    os.remove("mat2.csv.meta")
