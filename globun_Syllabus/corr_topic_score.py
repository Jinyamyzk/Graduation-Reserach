from scipy import stats
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np


def get_topic(nendo, code):
    topic_grades = None
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    topic_value = taken_class['トピックの確率'].values.tolist()
    return topic_value

def corrcoef(grade, topic):
    return np.corrcoef(grade, topic)[0, 1]


df = pd.read_json('syllabus_tfidf.json')

with open('grade_Kim.csv') as f:
    h = next(csv.reader(f))
    reader = csv.reader(f)
    grades = [e for e in reader]
    f.close()


topic_grade = []
for g in grades:
    temp = []
    topic = get_topic(int(g[0]),g[1]) #トピック行列をとってくる
    #見つからなければ処理を飛ばす
    if len(topic)==0:
        continue
    temp.append(topic[0]) #トピックを追加
    temp.append(int(g[2])) #成績を追加
    topic_grade.append(temp)

t1 = []
t2 = []
t3 = []
t4 = []
t5 = []
t6 = []
grade = []
for t in topic_grade:
     t_val = t[0]
     grade.append(t[1])
     t1.append(t_val[0])
     t2.append(t_val[1])
     t3.append(t_val[2])
     t4.append(t_val[3])
     t5.append(t_val[4])
     t6.append(t_val[5])

corr1 = corrcoef(t1, grade)
corr2 = corrcoef(t2, grade)
corr3 = corrcoef(t3, grade)
corr4 = corrcoef(t4, grade)
corr5 = corrcoef(t5, grade)
corr6 = corrcoef(t6, grade)

print(corr1, corr2, corr3, corr4, corr5, corr6)
