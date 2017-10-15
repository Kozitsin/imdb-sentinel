import random

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.preprocessing.sequence import pad_sequences
from keras.regularizers import l2

import numpy as np
import os.path

from lib.reader import load_dir
from lib.vocabulary import Vocabulary


class Classifier:
    def __init__(self, name, max_words=500):
        self.model = None
        self.name = name
        self.vocab = Vocabulary()
        self.max_words = max_words

    def build(self):
        self.vocab.build()
        if not os.path.isfile(self.name):
            model = self.architecture()
            model = self.train(model)
            model.save(self.name)
        else:
            model = load_model(self.name)

        self.model = model
        return self

    def architecture(self):
        model = Sequential()
        model.add(Embedding(self.vocab.size(), 128))
        model.add(LSTM(128))
        model.add(Dropout(0.5))
        model.add(Dense(1, W_regularizer=l2(0.01)))
        model.add(Activation('sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model

    def train(self, model):
        pos_dir = 'dataset/train/pos'
        neg_dir = 'dataset/train/neg'
        data = load_dir(pos_dir, 1, 10) + load_dir(neg_dir, 0, 10)
        random.shuffle(data)

        features = list()
        labels = list()

        for X, y in data:
            features.append(self.pad([self.vocab.vectorize(X)])[0])
            labels.append(y)

        model.fit(np.array(features), np.array(labels))
        return model

    def pad(self, X):
        return pad_sequences(X, maxlen=self.max_words)

    def classify(self, X):
        inp = [self.vocab.vectorize(X)]
        inp = np.array(self.pad(inp))
        y = self.model.predict(inp)[0][0]
        return round(y), y
