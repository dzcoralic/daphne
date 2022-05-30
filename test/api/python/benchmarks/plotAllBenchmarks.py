from asyncio.subprocess import PIPE
import glob, os
from re import sub
import subprocess
import matplotlib.pyplot as plt
from api.python.utils.consts import PROTOTYPE_PATH
import seaborn as sns
import pandas as pd

daphneset = pd.read_csv("daphneset.csv")
kmeans = pd.read_csv("kmeans.csv")
sumdataset = pd.read_csv("sumdataset.csv")
sumdataset["size"].replace({"1x1":1, "4x4":16, "16x16":256, "64x64":4096, "256x256":65536, "1024x1024":1048576, "4096x4096":16777216,"16384x16384":268435456}, inplace=True)
sumdataset = sumdataset.sort_values(by=["size"])
sumdataset1 = sumdataset.head(20)
sumdataset2 = sumdataset.tail(20)
sumdataset2["time"] = sumdataset2["time"].div(1000000)
sumdataset2["summation_time"] = sumdataset2["summation_time"].div(1000000)

sns.set_theme(style="whitegrid")
g=sns.catplot(data=sumdataset1, kind="bar", x="size", y="time", hue="name", ci="sd", palette="mako",height=6, aspect=3).despine(left=True)
ax = g.axes[0,0]
for c in ax.containers:
    ax.bar_label(c)
plt.tight_layout()
g.savefig("/home/dzc/Desktop/out.png")
plt.clf()
sns.set_theme(style="whitegrid")
g=sns.catplot(data=sumdataset2, kind="bar", x="size", y="time", hue="name", ci="sd", palette="icefire",height=6, aspect=3).despine(left=True)
ax = g.axes[0,0]
for c in ax.containers:
    ax.bar_label(c)
plt.tight_layout()
g.savefig("/home/dzc/Desktop/out_1.png")
plt.clf()
sns.set_theme(style="whitegrid")
g=sns.catplot(data=sumdataset1, kind="bar", x="size", y="summation_time", hue="name", ci="sd", palette="mako",height=6, aspect=3).despine(left=True)
ax = g.axes[0,0]
for c in ax.containers:
    ax.bar_label(c)
plt.tight_layout()
g.savefig("/home/dzc/Desktop/out1_1.png")

plt.clf()
sns.set_theme(style="whitegrid")
g=sns.catplot(data=sumdataset2, kind="bar", x="size", y="summation_time", hue="name", ci="sd", palette="mako",height=6, aspect=3).despine(left=True)
ax = g.axes[0,0]
for c in ax.containers:
    ax.bar_label(c)
plt.tight_layout()
g.savefig("/home/dzc/Desktop/out1_2.png")

plt.clf()

sns.set_theme(style="whitegrid")
bp=sns.barplot(x=kmeans["kmeans_name"], y=kmeans["kmeans_runtime"])
bp.bar_label(bp.containers[0])
bp.get_figure().savefig("/home/dzc/Desktop/out2.png")
