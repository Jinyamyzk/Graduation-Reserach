csv_file = open('トピック分布.csv', 'r')

column_list = csv_file.readline().rstrip().split(',')


# 最後までファイルを1行ずつ読み込み、リストにレコードをいれる。
recoad_list = []
recoad = csv_file.readline()
while recoad :
    recoad_list.append(recoad.rstrip().split(','))
    recoad = csv_file.readline()

# 下記のデータが入ります。
# column_list => ['id', 'name', 'password']
# recoad_list => [['1', 'tanaka', 'hogehoge'], ['2', 'sugino', 'sugisugi'], ['3', 'haruka', 'hogahoga']]

# タブ区切りをjoin()で行い、表形式にして見やすくする。
print('\t'.join(column_list))
for recoad in recoad_list:
    print('\t'.join(recoad))
