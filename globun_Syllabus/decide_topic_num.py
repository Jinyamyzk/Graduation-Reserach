from gensim import corpora, models, similarities
import gensim
import math
import csv

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from collections import defaultdict

import pandas as pd
import itertools


df = pd.read_csv('syllabus_globun.csv', usecols=[0])
class_names = df.values.tolist()
class_names  = list(itertools.chain.from_iterable(class_names))

f = open("theme_words.csv", "r")
reader = csv.reader(f)
texts = [ e for e in reader ]
f.close()


dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
# lda = LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary)

import matplotlib
import matplotlib.pylab as plt
from tqdm import tqdm
import numpy as np
np.random.seed(0)

font = {'family': 'TakaoGothic'}
matplotlib.rc('font', **font)

start = 2
limit = 50
step = 2

#初期値
total_coherence_vals = []
total_perplexity_vals = []
for i in range(start, limit, step):
    total_coherence_vals.append(0)
    total_perplexity_vals.append(0)

for i in range(5):
    coherence_vals = []
    perplexity_vals = []
    for n_topic in tqdm(range(start, limit, step)):
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topic, random_state=0)
        perplexity_vals.append(np.exp2(-lda_model.log_perplexity(corpus)))
        coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_vals.append(coherence_model_lda.get_coherence())
    total_perplexity_vals = [x+y for (x,y) in zip(perplexity_vals,total_perplexity_vals)]
    total_coherence_vals = [(x,y) for (x,y) in zip(coherence_vals,total_coherence_vals)]


x = range(start, limit, step)

fig, ax1 = plt.subplots(figsize=(12,5))

c1 = 'darkturquoise'
ax1.plot(x, coherence_vals, 'o-', color=c1)
ax1.set_xlabel('Num Topics')
ax1.set_ylabel('Coherence', color=c1); ax1.tick_params('y', colors=c1)

c2 = 'slategray'
ax2 = ax1.twinx()
ax2.plot(x, perplexity_vals, 'o-', color=c2)
ax2.set_ylabel('Perplexity', color=c2); ax2.tick_params('y', colors=c2)

ax1.set_xticks(x)
fig.tight_layout()
plt.show()
