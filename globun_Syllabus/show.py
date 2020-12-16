import csv
import pandas as pd

df = pd.read_csv("data/svm_score.csv")

data = df.values.tolist()

t2 = []
t4 = []
t6 = []
t16 = []
for d in data:
    if d[4] == 2:
        t2.append(d[1])
    elif d[4] == 4:
        t4.append(d[1])
    elif d[4] == 6:
        t6.append(d[1])
    elif d[4] == 16:
        t16.append(d[1])
def ave(data):
    return sum(data)/len(data)

print("トピック数２の平均値："+str(ave(t2)))
print("トピック数４の平均値："+str(ave(t4)))
print("トピック数６の平均値："+str(ave(t6)))
print("トピック数１６の平均値："+str(ave(t16)))
