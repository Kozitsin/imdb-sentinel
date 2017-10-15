from lib.classifier.classifier import Classifier

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.regularizers import l2


# https://habrahabr.ru/company/dca/blog/274027
class L2Classifier(Classifier):
    def architecture(self):
        model = Sequential()
        model.add(Embedding(self.vocab.size(), 128))
        model.add(LSTM(64, return_sequences=True))
        model.add(LSTM(64))
        model.add(Dropout(0.5))
        model.add(Dense(1, W_regularizer=l2(0.01)))
        model.add(Activation('sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model
