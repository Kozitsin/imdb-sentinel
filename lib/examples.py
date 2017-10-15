import random

from lib.reader import load_dir


class Examples:
    def __init__(self, classifier):
        self.classifier = classifier

    def load(self, positives, negatives):
        pos_dir = 'dataset/test/pos'
        neg_dir = 'dataset/test/neg'
        data = load_dir(pos_dir, 1, positives) + load_dir(neg_dir, 0, negatives)
        random.shuffle(data)
        return self.classify(data)

    def classify(self, data):
        predictions = []
        for X, y in data:
            label, _ = self.classifier.classify(X)
            predictions.append(dict(q=X, predicted=int(label), real=int(y)))
        return predictions
