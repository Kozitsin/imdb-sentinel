import random

from abc import ABC, abstractmethod
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

import tensorflow as tf
import numpy as np
import os.path

from lib.reader import load_dir
from lib.vocabulary import Vocabulary


class Classifier(ABC):
    def __init__(self, name, max_words=500):
        self.model = None
        self.graph = None
        self.name = name
        self.vocab = Vocabulary()
        self.max_words = max_words

    def build(self):
        self.vocab.build()
        if not os.path.isfile(self.name):
            print("No stored configuration for " + self.name + " has been found.")
            model = self.architecture()
            print("Model has been built.")
            model = self.train(model)
            print("Model has been trained.")
            model.save(self.name)
            print("Model has been stored.")
        else:
            print("Stored configuration for " + self.name + " has been found.")
            model = load_model(self.name)
            model._make_predict_function()
            self.graph = tf.get_default_graph()
            print("Model has been loaded.")
        self.model = model
        return self

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
        with self.graph.as_default():
            y = self.model.predict(inp)[0][0]
            return round(y), y

    @abstractmethod
    def architecture(self):
        pass
