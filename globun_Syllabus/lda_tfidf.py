import pickle
from gensim import corpora, models, similarities
import gensim
import math
import csv
import numpy as np

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from collections import defaultdict

import pandas as pd
import itertools

from tqdm import tqdm
import matplotlib
import matplotlib.pylab as plt
import json
from wordcloud import WordCloud

import logging


df = pd.read_csv('syllabus_globun.csv', usecols=[0])
class_names = df.values.tolist()
class_names = list(itertools.chain.from_iterable(class_names))

f = open("theme_words.csv", "r")
reader = csv.reader(f)
texts = [e for e in reader]
f.close()

dictionary = corpora.Dictionary(texts)
print(dictionary)
# make corpus
corpus = [dictionary.doc2bow(t) for t in texts]


# tfidf
tfidf = gensim.models.TfidfModel(corpus)


# make corpus_tfidf
corpus_tfidf = tfidf[corpus]

NUM_TOPICS = 6

# LDA Model
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=NUM_TOPICS, alpha='symmetric', random_state=0)

# test
N = sum(count for doc in corpus for id, count in doc)
print("N: ",N)

perplexity = np.exp2(-lda_model.log_perplexity(corpus))
print("perplexity:", perplexity)

# def get_topic_words(topic_id):
#     for t in lda_model.get_topic_terms(topic_id):
#         print("{}: {}".format(dictionary[t[0]], t[1]))
# for t in range(6):
#     print("Topic # ",t)
#     get_topic_words(t)
#     print("\n")
#
# topics = sorted(lda_model.get_document_topics(corpus[0]), key=lambda t:t[1], reverse=True)
# for t in topics[:10]:
#     print("{}: {}".format(t[0], t[1]))

# テストデータをモデルに掛ける
test_corpus = [dictionary.doc2bow(text) for text in texts]

topic_results = []


# クラスタリング結果を出力
for unseen_doc in test_corpus:
    score_by_topic = [0] * NUM_TOPICS
    for topic, score in lda_model[unseen_doc]:
        score_by_topic[topic] = score
    topic_results.append(score_by_topic)
from pprint import pprint

df = pd.read_csv('syllabus_globun.csv')
df['トピックの確率'] = topic_results
# df.to_json(f'syllabus_tfidf_{NUM_TOPICS}.json')

np.random.seed(0)
FONT = "/Library/Fonts/Arial Unicode.ttf"


ncols = math.ceil(NUM_TOPICS/2)
nrows = math.ceil(lda_model.num_topics/ncols)
fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15,7))
axs = axs.flatten()

def color_func(word, font_size, position, orientation, random_state, font_path):
    return 'black'

for i, t in enumerate(range(lda_model.num_topics)):

    x = dict(lda_model.show_topic(t, 30))
    im = WordCloud(
        font_path=FONT,
        background_color='white',
        color_func=color_func,
        random_state=0
    ).generate_from_frequencies(x)
    axs[i].imshow(im)
    axs[i].axis('off')
    axs[i].set_title('Topic '+str(t))

plt.tight_layout()
# plt.savefig(f'visualize_{NUM_TOPICS}.png')
# plt.show()
