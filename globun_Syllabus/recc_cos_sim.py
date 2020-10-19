import pandas as pd
import pickle
import csv
import json
import numpy as np

topic_num = 6
sum_topic_odds = [0] * topic_num

def search_goodat_topic(nendo, code, grade):
    topic_grades = None
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    topic_value = taken_class['トピックの確率'].values.tolist()
    if len(topic_value) == 1:
        topic_grades = [n * grade for n in topic_value[0]]
    return topic_grades

def cos_sim(v1, v2):
    v1_array = np.array(v1)
    v2_array = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def reccomend(nendo):
    available_classes = df[(df['年度'] == nendo)]
    class_names_topics = available_classes[['科目名','トピックの確率']].values.tolist()
    for class_name_topic in class_names_topics:
        similarity = cos_sim(class_name_topic[1],sum_topic_odds)
        class_name_topic[1] = similarity
        class_names_cos_sim.append(class_name_topic)




df = pd.read_json('syllabus_tfidf.json')
with open('grade_Kim.csv') as f:
    h = next(csv.reader(f))
    reader = csv.reader(f)
    grades = [e for e in reader]
    f.close()

for row in grades:
    topic_grades = search_goodat_topic(int(row[0]), row[1], float(row[2]))
    if topic_grades is not None:
        sum_topic_odds = [topic_grades[i] + sum_topic_odds[i] for i in range(len(topic_grades))]

class_names_cos_sim = []
# sum_topic_odds = list(map(lambda x: x/len(grades), sum_topic_odds))
reccomend(2020)
reccomend_class = sorted(class_names_cos_sim, reverse=True, key=lambda x: x[1])
# print(class_names_sorted)
for i in reccomend_class[0:10]:
    print(i)
