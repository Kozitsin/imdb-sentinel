import os
import random


def load_dir(dirname, label, size):
    data = []
    files = os.listdir(dirname)
    random.shuffle(files)
    for fname in files[:size]:
        for line in open(os.path.join(dirname, fname), encoding='utf-8'):
            data.append((line, label))
    return data
