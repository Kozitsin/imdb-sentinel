import os
import random


def load_dir(dirname, label, size):
    data = []
    files = os.listdir(dirname)
    random.shuffle(files)
    for fname in files[:size]:
        for line in open(os.path.join(dirname, fname)):
            data.append((line, label))
    return data


# def load_dir(dirname, label):
#     data = []
#     files = os.listdir(dirname)
#     for fname in files:
#         for line in open(os.path.join(dirname, fname)):
#             data.append((line, label))
#     return data
