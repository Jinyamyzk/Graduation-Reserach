import pandas as pd

#成績の数値への変換
def score_to_gpa(score):
    if score == '秀':
        return 9
    elif score == '優':
        return 6
    elif score == '良':
        return 3
    elif score == '可':
        return 2
    elif score == '不可':
        return 0
    elif score == '合格':
        return 0
    elif score == '取消':
        return 0

# 成績ファイルの読み込み
data = pd.read_csv('seiseki1.csv', names=["index","時間割コード","c","d","年度","f","Score","h"], encoding = "shift-jis")
score_list = data[["Score"]].values.tolist()
score_number = []
for score in score_list:
    score_number.append(score_to_gpa(score[0]))
data["Score"] = score_number
data = data[["年度","時間割コード","Score"]]

# CSV形式で出力
data.to_csv('/Users/Jinya/Desktop/Graduation Reserach/globun_Syllabus/grade_A.csv', index=False, encoding='utf-8')
