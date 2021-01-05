import pandas as pd
df = pd.read_csv('data/raw_grades/SIRS1710509.csv', header=3, encoding='cp932', usecols=[1, 4, 6])
print(df)

def score_to_gpa(score):
    if score == '秀':
        return 10
    elif score == '優':
        return 10
    elif score == '良':
        return 2
    elif score == '可':
        return 1
    elif score == '不可':
        return 0
    elif score == '合格':
        return 0
    elif score == '取消':
        return 0
