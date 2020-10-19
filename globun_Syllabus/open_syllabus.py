import pandas as pd
import pickle
import csv
import json
from pprint import pprint
df = pd.read_json('syllabus_tfidf.json')
available_classes = df[(df['年度'] == 2020)]
class_names_topics = available_classes[['科目名','トピックの確率']]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
print(class_names_topics)
