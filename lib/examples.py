import random

from lib.reader import load_dir


class Examples:
    def __init__(self, l1_classifier, l2_classifier):
        self.l1_classifier = l1_classifier
        self.l2_classifier = l2_classifier

    def load(self, positives, negatives):
        pos_dir = 'dataset/test/pos'
        neg_dir = 'dataset/test/neg'
        data = load_dir(pos_dir, 1, positives) + load_dir(neg_dir, 0, negatives)
        random.shuffle(data)
        return self.classify(data)

    def classify(self, data):
        predictions = []
        for X, y in data:
            l1_label, _ = self.l1_classifier.classify(X)
            l2_label, _ = self.l2_classifier.classify(X)
            predictions.append(dict(q=X, l1_predicted=int(l1_label), l2_predicted=int(l2_label), real=int(y)))
        return predictions
