import random

from lib.reader import load_dir


class Examples:
    def __init__(self, l1_classifier, l2_classifier):
        self.l1_classifier = l1_classifier
        self.l2_classifier = l2_classifier
        self._pos_dir = 'dataset/test/pos'
        self._neg_dir = 'dataset/test/neg'

    def load(self, positives, negatives):
        data = load_dir(self._pos_dir, 1, positives) + load_dir(self._neg_dir, 0, negatives)
        random.shuffle(data)
        return self.classify(data)

    def classify(self, data):
        predictions = []
        for X, y in data:
            l1_label, _ = self.l1_classifier.classify(X)
            l2_label, _ = self.l2_classifier.classify(X)
            predictions.append(dict(q=X, l1_predicted=int(l1_label), l2_predicted=int(l2_label), real=int(y)))
        return predictions

    def test(self):
        size = 20
        data = load_dir(self._pos_dir, 1, size) + load_dir(self._neg_dir, 0, size)
        original = []
        l1 = []
        l2 = []

        for X, y in data:
            l1.append(int(self.l1_classifier.classify(X)[0]))
            l2.append(int(self.l2_classifier.classify(X)[0]))
            original.append(y)

        l1_accuracy = self.accuracy(original, l1)
        l2_accuracy = self.accuracy(original, l2)

        l1_stat = self.errors(original, l1)
        l2_stat = self.errors(original, l2)

        return (dict(name='L1', accuracy=str(l1_accuracy), errors=l1_stat),
                dict(name='L2', accuracy=str(l2_accuracy), errors=l2_stat))

    def accuracy(self, original, predicted):
        correct = 0.0
        for i in range(0, len(original)):
            if original[i] == predicted[i]:
                correct += 1
        return correct / len(original)

    def errors(self, original, predicted):
        false_positives = 0
        false_negatives = 0
        true_positives = 0
        true_negatives = 0

        for i in range(0, len(original)):
            if original[i] == 1 and predicted[i] == 1:
                true_positives += 1
            elif original[i] == 0 and predicted[i] == 0:
                true_negatives += 1
            elif original[i] == 1 and predicted[i] == 0:
                false_negatives += 1
            elif original[i] == 0 and predicted[i] == 1:
                false_positives += 1
            else:
                print('Unexpected branch! original=' + str(original[i]) + ' predicted=' + str(predicted[i]))
        return dict(true_positives=true_positives, true_negatives=true_negatives,
                    false_positives=false_positives, false_negatives=false_negatives)
