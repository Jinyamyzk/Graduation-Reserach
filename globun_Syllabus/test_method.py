import pandas as pd
import pickle
import csv
import json

sum_topic_odds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0]

def search_goodat_topic(nendo, code, grade):
    topic_grades = None
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    topic_value = taken_class['トピックの確率'].values.tolist()
    if len(topic_value) == 1:
        topic_grades = [n * grade for n in topic_value[0]]
    return topic_grades

def sum_class_score(nendo,code):
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    class_names_topics = taken_class[['科目名','年度','時間割コード','トピックの確率']].values.tolist()
    for class_name_topic in class_names_topics:
        combined = [x*y for (x,y) in zip(class_name_topic[3],sum_topic_odds)]
        total_clas_score = sum(combined)
        class_name_topic[3] = total_clas_score
        class_names.append(class_name_topic)

df = pd.read_json('syllabus_tfidf.json')
with open('grade_Kim.csv') as f:
    h = next(csv.reader(f))
    reader = csv.reader(f)
    grades = [e for e in reader]
    f.close()

df2 = pd.read_csv('grade_Kim.csv')

for row in grades:
    topic_grades = search_goodat_topic(int(row[0]), row[1], float(row[2]))
    if topic_grades is not None:
        sum_topic_odds = [topic_grades[i] + sum_topic_odds[i] for i in range(len(topic_grades))]
class_names = []
for row in grades:
    sum_class_score(int(row[0]), row[1])
class_names_sorted = sorted(class_names, reverse=True, key=lambda x: x[3])
print(sum_topic_odds)
for i in class_names_sorted[0:5]:
    print(i)
    # class_df = df[(df['年度'] == i[1]) & (df['時間割コード'] == i[2])]
    # print(class_df.values)
    class_grade = df2[(df2['年度'] == i[1]) & (df2['時間割コード'] == i[2])]
    print(class_grade.values)
    print('--------------------------------')
