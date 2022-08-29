import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from ast import literal_eval
import itertools 
SMALL_SIZE = 16
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
sns.set_context(rc={'patch.linewidth':1})
df = pd.read_csv("addsum.csv",converters={"script execution":literal_eval, "end-to-end":literal_eval,
                                                   "add":literal_eval, "sum":literal_eval, "transfer sender":literal_eval,
                                                   "data generation":literal_eval, "transfer receiver":literal_eval})

tmp = []

for i in df["script execution"]:
  if isinstance(i, list):
    tmp.append(statistics.mean(i[2:]))
  else:
    tmp.append(0)

tmp_e2e = []
for i in df["end-to-end"]:  
  if isinstance(i, list):
    tmp_e2e.append(statistics.mean(i[2:]))
  else:
    tmp_e2e.append(0)

tmp_add = []
for i in df["add"]:
  if isinstance(i, list):
    tmp_add.append(statistics.mean(i[2:]))
  else:
    tmp_add.append(0)

tmp_sum = []
for i in df["sum"]:  
  if isinstance(i, list):
    tmp_sum.append(statistics.mean(i[2:]))
  else:
    tmp_sum.append(0)

tmp_dg = []
for i in df["data generation"]:
  if isinstance(i, list) and len(i):
    tmp_dg.append(statistics.mean(i[2:]))
  else:
    tmp_dg.append(0)

tmp_ts = []
for i in df["transfer sender"]:  
  if isinstance(i, list)  and len(i):
    tmp_ts.append(statistics.mean(i[2:]))
  else:
    tmp_ts.append(0)

tmp_tr = []
for i in df["transfer receiver"]:  
  if isinstance(i, list)  and len(i):
    tmp_tr.append(statistics.mean(i[2:]))
  else:
    tmp_tr.append(0)


df['end-to-end'] = tmp_e2e
df['script execution'] = tmp
df['sum'] = tmp_sum
df['add'] = tmp_add
df['transfer sender'] = tmp_ts
df['transfer receiver'] = tmp_tr
df['data generation'] = tmp_dg
df = df.replace('Pure NumPy', 'Pure NumPy\n(1)')
df = df.replace('Pure DaphneLib', 'Pure DaphneLib\n(2)')
df = df.replace('NumPy to DAPHNE via shared memory', 'NumPy to DAPHNE \nvia shared memory\n(3)')
df = df.replace('DAPHNE to NumPy via shared memory', 'DAPHNE to NumPy \nvia shared memory\n(5)')
df = df.replace('NumPy to DAPHNE via files', 'NumPy to DAPHNE \nvia files\n(4)')
df = df.replace('DAPHNE to NumPy via files', 'DAPHNE to NumPy \nvia files\n(6)')

df = df.sort_values(by=['name', 'script execution'], inplace=False, ascending=False)
mask = df['size'] <= 100
df3 = df[mask].reset_index(drop=True)

df['end-to-end'] = df['end-to-end'].div(10**9).round(2)
df['script execution'] = df['script execution'].div(10**9).round(2)
df['sum'] = df['sum'].div(10**9).round(2)
df['add'] = df['add'].div(10**9).round(2)
df['data generation'] = df['data generation'].div(10**9).round(2)
df['transfer receiver'] = df['transfer receiver'].div(10**9).round(2)
#df['transfer receiver'] = df['transfer receiver'] 
df['transfer sender'] = df['transfer sender'].div(10**9).round(2)

df3['end-to-end'] = df3['end-to-end'].div(10**6).round(2)
df3['script execution'] = df3['script execution'].div(10**6).round(2)
df3['sum'] = df3['sum'].div(10**6).round(2)
df3['add'] = df3['add'].div(10**6).round(2)
df3['data generation'] = df3['data generation'].div(10**6).round(2)
df3['transfer receiver'] = df3['transfer receiver'].div(10**6).round(2)
#df['transfer receiver'] = df['transfer receiver'] 
df3['transfer sender'] = df3['transfer sender'].div(10**6).round(2)

m = df['size'].astype(str).str.contains('10000')
df1 = df[m].reset_index(drop=True)
m = df['size'].astype(str).str.contains('20000')
df2 = df[m].reset_index(drop=True)
m = df['size'].astype(str).str.contains('100')

fig, axes = plt.subplots(3, 1, figsize=(16,20))
dflist = [df3, df1, df2]
for i in range(0,3):
  axes[i].bar(dflist[i]["name"], dflist[i]["end-to-end"],bottom=0, edgecolor='black', facecolor="none", label="Startup overhead")
  
#s1 = sns.barplot(x="name", y="end-to-end", data=dflist[0], ax=axes[0], palette="Pastel1")
#s1 = sns.barplot(x="name", y="script execution", ci=None, data=dflist[0], ax=axes[0], palette="Pastel1", edgecolor="black", label="Script execution")

#s2 = sns.barplot(x="name", y="end-to-end", data=dflist[1], ax=axes[1], palette="Pastel1")
#s2 = sns.barplot(x="name", y="script execution", ci=None, data=dflist[1], ax=axes[1],color="white", edgecolor="black", label="Script execution")
#s3 = sns.barplot(x="name", y="script execution", ci=None, data=dflist[2], ax=axes[2], edgecolor="black", label="Script execution")

for i in range(0,3):
  #axes[i].bar(dflist[i]["name"], dflist[i]["end-to-end"], bottom=0, edgecolor="black", hatch="\\/...", facecolor="gainsboro", label="Script runtime, measured outside")
  #axes[i].bar(dflist[i]["name"], dflist[i]["script execution"], bottom=0, edgecolor="black", hatch="Xx", facecolor="none", label="Script runtime, measured within")
  axes[i].bar(dflist[i]["name"], dflist[i]["sum"],bottom=dflist[i]["add"]+dflist[i]["data generation"] + dflist[i]["transfer sender"] + dflist[i]["transfer receiver"], edgecolor='black', hatch='oo', facecolor="none", label="Sum")
  axes[i].bar(dflist[i]["name"], dflist[i]["add"],bottom=dflist[i]["data generation"] + dflist[i]["transfer sender"] + dflist[i]["transfer receiver"], edgecolor='black', hatch='//', facecolor="none", label="Add")
  axes[i].bar(dflist[i]["name"], dflist[i]["transfer receiver"],bottom=dflist[i]["data generation"]+dflist[i]["transfer sender"], edgecolor='black', hatch='xx', facecolor="none", label="Transfer Receiver")
  axes[i].bar(dflist[i]["name"], dflist[i]["transfer sender"],bottom=dflist[i]["data generation"], edgecolor='black', hatch='\\\\', facecolor="none", label="Transfer sender")
  axes[i].bar(dflist[i]["name"], dflist[i]["data generation"],bottom=0, edgecolor='black', hatch='++', facecolor="none", label="Data generation")
  #axes[i].bar(dflist[i]["name"], dflist[i]["result construction"],bottom=dflist[i]["data generation"]+dflist[i]["transfer receiver"]+dflist[i]["transfer sender"]+dflist[i]["sum"]+dflist[i]["add"], edgecolor='black', hatch='*', facecolor="none", label="Result construct")


axes[1].set_title("Matrix size - Rows x Cols: 10000x10000")
axes[2].set_title("Matrix size - Rows x Cols: 20000x20000")
axes[1].set_ylabel("Runtime [s]")
axes[2].set_ylabel("Runtime [s]")
axes[0].set_title("Matrix size - Rows x Cols: 100x100")
axes[0].set_ylabel("Runtime [ms]")
axes[0].set_xlabel("(a)")
axes[1].set_xlabel("(b)")
axes[2].set_xlabel("(c)")
print(df1)
print(df3)
plt.suptitle("")
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
axes[0].legend(prop={'size':SMALL_SIZE})
plt.savefig('sumaddition.png')