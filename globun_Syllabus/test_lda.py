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
# make dictionary
dictionary = corpora.Dictionary(texts)
dictionary.filter_extremes(no_below=3,no_above=0.8)

# vocab size
print('vocab size: ', len(dictionary))

#save dictionary
dictionary.save_as_text("dictionary.txt")

# make corpus
corpus = [dictionary.doc2bow(t) for t in texts]

# tfidf
tfidf = gensim.models.TfidfModel(corpus)

# make corpus_tfidf
corpus_tfidf = tfidf[corpus]

# #Metrics for Topic Models
# start = 2
# limit = 22
# step = 1
#
# coherence_vals = []
# perplexity_vals = []
#
# for n_topic in tqdm(range(start, limit, step)):
#     lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=n_topic, random_state=0)
#     perplexity_vals.append(np.exp2(-lda_model.log_perplexity(corpus_tfidf)))
#     coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
#     coherence_vals.append(coherence_model_lda.get_coherence())
# # evaluation
# x = range(start, limit, step)
#
# fig, ax1 = plt.subplots(figsize=(12,5))
#
# # coherence
# c1 = 'darkturquoise'
# ax1.plot(x, coherence_vals, 'o-', color=c1)
# ax1.set_xlabel('Num Topics')
# ax1.set_ylabel('Coherence', color=c1); ax1.tick_params('y', colors=c1)
#
# # perplexity
# c2 = 'slategray'
# ax2 = ax1.twinx()
# ax2.plot(x, perplexity_vals, 'o-', color=c2)
# ax2.set_ylabel('Perplexity', color=c2); ax2.tick_params('y', colors=c2)
#
# # Vis
# ax1.set_xticks(x)
# fig.tight_layout()
# plt.show()

# LDA Model
num_topic = 2
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topic, alpha='symmetric', random_state=0)

def get_topic_words(topic_id):
    for t in lda_model.get_topic_terms(topic_id):
        print("{}: {}".format(dictionary[t[0]], t[1]))
for t in range(num_topic):
    print("Topic # ",t)
    get_topic_words(t)
    print("\n")
