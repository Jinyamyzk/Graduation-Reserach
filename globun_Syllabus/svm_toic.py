import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

import csv
import pandas as pd

def get_topic(nendo, code):
    topic_grades = None
    taken_class = df[(df['年度'] == nendo) & (df['時間割コード'] == code)]
    topic_value = taken_class['トピックの確率'].values.tolist()
    return topic_value

#成績を0,1に変換
def grade_to_digit(grade):
    if grade >= 1:
        return 1
    else:
        return 0



df = pd.read_json('syllabus_tfidf_2.json')

file = 'grade_aipo.csv'
with open(file) as f:
    h = next(csv.reader(f))
    reader = csv.reader(f)
    grades = [e for e in reader]
    f.close()


for g in grades:
    g[2] = grade_to_digit(int(g[2]))

topic_grade = []
for g in grades:
    temp = []
    topic = get_topic(int(g[0]),g[1]) #トピック行列をとってくる
    #見つからなければ処理を飛ばす
    if len(topic)==0:
        continue
    temp.extend(topic[0]) #トピックを追加
    temp.append(int(g[2])) #成績を追加
    topic_grade.append(temp)

#pandas
topic_grade_df = pd.DataFrame(topic_grade)

#トピック数を取得
topic_num = len(df.columns)

#説明変数(x)と目的変数(y)
X = topic_grade_df.iloc[:, :2]
y = topic_grade_df.iloc[:, 2:].values.flatten() # 1次元に展開

# 学習データとテストデータの分離
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# 標準化
std_scl = StandardScaler()
std_scl.fit(X_train)
X_train = std_scl.transform(X_train)
X_test = std_scl.transform(X_test)

# 学習とテスト
svc_param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]
}

svc_grid_search = GridSearchCV(SVC(), svc_param_grid, cv=10)
svc_grid_search.fit(X_train, y_train)


print('Train score: {:.3f}'.format(svc_grid_search.score(X_train, y_train)))
print('Test score: {:.3f}'.format(svc_grid_search.score(X_test, y_test)))
print('Confusion matrix:\n{}'.format(confusion_matrix(y_test, svc_grid_search.predict(X_test))))
print('Best parameters: {}'.format(svc_grid_search.best_params_))
print('Best estimator: {}'.format(svc_grid_search.best_estimator_))

#csvファイルに結果を書き込む
data = []
data.extend([file,'{:.3f}'.format(svc_grid_search.score(X_train, y_train)),'{:.3f}'.format(svc_grid_search.score(X_test, y_test)),
'{}'.format(confusion_matrix(y_test, svc_grid_search.predict(X_test))).replace('\n',''),2])
print(data)
with open('/Users/Jinya/Desktop/Graduation Reserach/globun_Syllabus/data/svm_score.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()
