import pandas as pd
import pickle
import csv
import json
import numpy as np
import scipy.stats
import glob
import os
import matplotlib.pyplot as plt

#授業を見つけて、トピックベクトルに成績の値を掛ける
def search_goodat_topic(nendo, code, grade):
    topic_grades = None
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    topic_value = taken_class['トピックの確率'].values.tolist()
    if len(topic_value) == 1:
        topic_grades = [n * grade for n in topic_value[0]]
    return topic_grades

#コサイン類似度を求める
def cos_sim(v1, v2):
    v1_array = np.array(v1)
    v2_array = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

#授業をおすすめする
def reccomend(nendo,code):
    _class_names_cos_sim = []
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    class_names_topics = taken_class[['科目名','年度','時間割コード','トピックの確率']].values.tolist()
    for class_name_topic in class_names_topics:

        similarity = cos_sim((scipy.stats.zscore(class_name_topic[3])),sum_topic_odds)
        class_name_topic[3] = similarity
        _class_names_cos_sim.append(class_name_topic)
    return _class_names_cos_sim

#相関係数を求める
def corrcoef(grade, topic):
    return np.corrcoef(grade, topic)[0, 1]


df = pd.read_json('syllabus_tfidf.json')

result = []
plot_list = []
#成績フォルダ内のcsvファイルのパスを取得
for path in glob.glob("data/grades/*.csv"):
    #成績ファイルを開く
    with open(path) as f:
        h = next(csv.reader(f))
        reader = csv.reader(f)
        grades = [e for e in reader]
        f.close()

    count = 0
    #学生の履修の嗜好性ベクトル
    topic_num = 6
    sum_topic_odds = [0] * topic_num
    for row in grades:
        topic_grades = search_goodat_topic(int(row[0]), row[1], float(row[2]))
        if topic_grades is not None:
            sum_topic_odds = [topic_grades[i] + sum_topic_odds[i] for i in range(len(topic_grades))]
            count += 1
    #平均値にする
    sum_topic_odds = list(map(lambda x:x/count, sum_topic_odds))
    #コサイン類似度を求める
    class_names_cos_sim = []
    for row in grades:
        class_names_cos_sim.extend(reccomend(int(row[0]), row[1]))
    #おすすめ順に並べる
    reccomend_class = sorted(class_names_cos_sim, reverse=True, key=lambda x: x[3])
    #成績データをデータフレームとして読み込む
    df2 = pd.read_csv(path)
    reccomend_class_grade = []
    for c in reccomend_class:
        class_grade = df2[(df2['年度'] == c[1]) & (df2['時間割コード'] == c[2])]
        reccomend_class_grade.append(class_grade.values[0][2])
    #ランクのリストを作る
    rank = list(range(len(reccomend_class), 0, -1))

    #プロットするためのリストを作る
    plot_list.append([os.path.basename(path).split('.', 1)[0], reccomend_class_grade])


    #相関係数を求める
    result.append([os.path.basename(path).split('.', 1)[0],corrcoef(rank, reccomend_class_grade)])

#表示する
d = pd.DataFrame(result, columns=["ファイル名", "相関係数"])
from tabulate import tabulate
print(tabulate(d,d.columns))


#figure()でグラフを表示する領域をつくり，figというオブジェクトにする．
fig = plt.figure()

#add_subplot()でグラフを描画する領域を追加する．引数は行，列，場所
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)


axes = [ax1, ax2, ax3, ax4]

i=0
for p in plot_list:
    axes[i].plot(p[1])
    axes[i].set_title(p[0])
    i+=1

fig.tight_layout()              #レイアウトの設定
plt.show()
