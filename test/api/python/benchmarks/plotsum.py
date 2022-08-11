import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from ast import literal_eval
import itertools 
df = pd.read_csv("addsum.csv",converters={"script execution":literal_eval, "end-to-end":literal_eval,
                                                   "add":literal_eval, "sum":literal_eval, "transfer sender":literal_eval,
                                                   "data generation":literal_eval, "result construction":literal_eval,"transfer receiver":literal_eval})

tmp = []

for i in df["script execution"]:
  if isinstance(i, list):
    tmp.append(statistics.median(i))
  else:
    tmp.append(0)

tmp_e2e = []
for i in df["end-to-end"]:  
  if isinstance(i, list):
    tmp_e2e.append(statistics.median(i))
  else:
    tmp_e2e.append(0)

tmp_add = []
for i in df["add"]:
  if isinstance(i, list):
    tmp_add.append(statistics.median(i))
  else:
    tmp_add.append(0)

tmp_sum = []
for i in df["sum"]:  
  if isinstance(i, list):
    tmp_sum.append(statistics.median(i))
  else:
    tmp_sum.append(0)

tmp_dg = []
for i in df["data generation"]:
  if isinstance(i, list):
    tmp_dg.append(statistics.median(i))
  else:
    tmp_dg.append(0)

tmp_ts = []
for i in df["transfer sender"]:  
  if isinstance(i, list):
    tmp_ts.append(statistics.median(i))
  else:
    tmp_ts.append(0)

tmp_tr = []
for i in df["transfer receiver"]:  
  if isinstance(i, list):
    tmp_tr.append(statistics.median(i))
  else:
    tmp_tr.append(0)

tmp_rc = []
for i in df["result construction"]:  
  if isinstance(i, list):
    tmp_rc.append(statistics.median(i))
  else:
    tmp_rc.append(0)

df['end-to-end'] = tmp_e2e
df['script execution'] = tmp
df['sum'] = tmp_sum
df['add'] = tmp_add
df['transfer sender'] = tmp_ts
df['transfer receiver'] = tmp_tr
df['data generation'] = tmp_dg
df['result construction'] = tmp_rc

df = df.replace('Data generated in Daphne, Operations in NumPy','Data generated in Daphne\nOperations in NumPy\nTransfer via files')
df = df.replace('Data-gen in daphne, sum in np','Data generated in Daphne\nOperations in NumPy\nTransfer via shared mem')
 
df = df.replace('Data Transfer via Files, Daphne to Numpy','Numpy to Daphne\nData Transfer via Files')
df = df.replace('Data transfer via ctypes','Numpy to Daphne\nData Transfer via shared mem')

df['end-to-end'] = df['end-to-end'].div(10**6).round(2)
df['script execution'] = df['script execution'].div(10**6).round(2)
df['sum'] = df['sum'].div(10**6).round(2)
df['add'] = df['add'].div(10**6).round(2)
df['data generation'] = df['data generation'].div(10**6).round(2)
df['transfer receiver'] = df['transfer receiver'].div(10**6).round(2)
df['result construction'] = df['result construction'].div(10**6).round(2)
df['transfer sender'] = df['transfer sender'].div(10**6).round(2)
m = df['size'].astype(str).str.contains('10000')
df1 = df[m].reset_index(drop=True)
m = df['size'].astype(str).str.contains('20000')
df2 = df[m].reset_index(drop=True)

fig, axes = plt.subplots(1, 2, figsize=(32,9))
dflist = [df1, df2]
s1 = sns.barplot(x="name", y="end-to-end", data=dflist[0], ax=axes[0], palette="Pastel1")
#s1 = sns.barplot(x="name", y="script execution", data=dflist[0], ax=axes[0], palette="Pastel1")

s2 = sns.barplot(x="name", y="end-to-end", data=dflist[1], ax=axes[1], palette="Pastel1")
#s2 = sns.barplot(x="name", y="script execution", data=dflist[1], ax=axes[1], palette="Pastel1")

for i in range(0,2):
  #axes[i].bar(dflist[i]["name"], dflist[i]["end-to-end"], bottom=0, edgecolor="black", hatch="\\/...", facecolor="gainsboro", label="Script runtime, measured outside")
  #axes[i].bar(dflist[i]["name"], dflist[i]["script execution"], bottom=0, edgecolor="black", hatch="Xx", facecolor="none", label="Script runtime, measured within")
  axes[i].bar(dflist[i]["name"], dflist[i]["sum"],bottom=dflist[i]["add"], edgecolor='black', hatch='oo', facecolor="none", label="Sum")
  axes[i].bar(dflist[i]["name"], dflist[i]["add"],bottom=0, edgecolor='black', hatch='//', facecolor="none", label="Add")
  axes[i].bar(dflist[i]["name"], dflist[i]["data generation"],bottom=dflist[i]["sum"]+dflist[i]["add"], edgecolor='black', hatch='++', facecolor="none", label="Data generation")
  axes[i].bar(dflist[i]["name"], dflist[i]["transfer sender"],bottom=dflist[i]["data generation"]+dflist[i]["sum"]+dflist[i]["add"], edgecolor='black', hatch='--', facecolor="none", label="Transfer sender")
  axes[i].bar(dflist[i]["name"], dflist[i]["transfer receiver"],bottom=dflist[i]["data generation"]+dflist[i]["transfer sender"]+dflist[i]["sum"]+dflist[i]["add"], edgecolor='black', hatch='xx', facecolor="none", label="Transfer Receiver")
  axes[i].bar(dflist[i]["name"], dflist[i]["result construction"],bottom=dflist[i]["data generation"]+dflist[i]["transfer receiver"]+dflist[i]["transfer sender"]+dflist[i]["sum"]+dflist[i]["add"], edgecolor='black', hatch='*', facecolor="none", label="Result construct")


axes[0].set_title("Matrix size - Rows x Cols: 10000x10000")
axes[1].set_title("Matrix size - Rows x Cols: 20000x20000")
plt.suptitle("Add + sum implementation")
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.legend()
plt.savefig('sumaddition.png')