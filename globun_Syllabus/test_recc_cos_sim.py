import pandas as pd
import pickle
import csv
import json
import numpy as np
import scipy.stats

topic_num = 6
sum_topic_odds = [0] * topic_num

def get_topic_value(nendo,code):
    topic_grades = None
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    topic_value = taken_class['トピックの確率'].values.tolist()
    return topic_value


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

def reccomend(nendo,code):
    _class_names_cos_sim = []
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    class_names_topics = taken_class[['科目名','年度','時間割コード','トピックの確率']].values.tolist()
    for class_name_topic in class_names_topics:

        similarity = cos_sim((scipy.stats.zscore(class_name_topic[3])),sum_topic_odds)
        class_name_topic[3] = similarity
        _class_names_cos_sim.append(class_name_topic)
    return _class_names_cos_sim

df = pd.read_json('syllabus_tfidf.json')
with open('data/grades/StudentA.csv') as f:
    h = next(csv.reader(f))
    reader = csv.reader(f)
    grades = [e for e in reader]
    f.close()

df2 = pd.read_csv('data/grades/StudentA.csv')

count = 0
for row in grades:
    topic_grades = search_goodat_topic(int(row[0]), row[1], float(row[2]))
    if topic_grades is not None:
        sum_topic_odds = [topic_grades[i] + sum_topic_odds[i] for i in range(len(topic_grades))]
        count += 1
print("\n嗜好性ベクトル")
print(sum_topic_odds)
print('\n')
print("おすすめの授業\n")
# print(count)
# sum_topic_odds = list(map(lambda x:x/count, sum_topic_odds))
# print(sum_topic_odds)



# print(scipy.stats.zscore(sum_topic_odds))
# sum_topic_odds = list(map(lambda x: x ** 4, sum_topic_odds))
# sum_topic_odds = scipy.stats.zscore(sum_topic_odds)

class_names_cos_sim = []
for row in grades:
    class_names_cos_sim.extend(reccomend(int(row[0]), row[1]))
reccomend_class = sorted(class_names_cos_sim, reverse=True, key=lambda x: x[3])


# print(scipy.stats.zscore(sum_topic_odds))

for i in reccomend_class[0:10]:
    print(i[0])
    # class_df = df[(df['年度'] == i[1]) & (df['時間割コード'] == i[2])]
    # print(class_df.values)
    topic_value = get_topic_value(i[1],i[2])
    print(topic_value)
    class_grade = df2[(df2['年度'] == i[1]) & (df2['時間割コード'] == i[2])]
    print(class_grade.values)
    print('--------------------------------')
