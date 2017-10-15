from flask import Flask, render_template, request, jsonify
from lib.classifier.l1classifier import L1Classifier
from lib.classifier.l2classifier import L2Classifier
from lib.examples import Examples
import threading
import json
import os.path

print(" - Starting up application")
lock = threading.Lock()
app = Flask(__name__)


class App:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def classifier(self, name=''):
        with lock:
            if getattr(self, '_classifier', None) is None:
                print(" - Building new classifiers - might take a while.")
                print(" - L1 Classifier was build")
                l1 = L1Classifier("L1.m").build()
                print(" - L2 Classifier was build")
                l2 = L2Classifier("L2.m").build()
                self._classifier = (l1, l2)
                print(" - Done!")

            if name == 'L1' or name == 'on':
                return self._classifier[0]
            else:
                return self._classifier[1]

t = threading.Thread(target=App().classifier)
t.daemon = True
t.start()


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/predict')
def predict():
    q = request.args.get('q')
    ann_type = request.args.get('ann_type')
    label, prediction = App().classifier(ann_type).classify(q)
    return jsonify(q=q, predicted_class=int(label), prediction=str(prediction))


@app.route('/examples')
def examples():
    examples = Examples(App().classifier('L1'), App().classifier('L2')).load(5, 5)
    return jsonify(items=examples)


@app.route('/test')
def test():
    if not os.path.isfile('results.json'):
        result = Examples(App().classifier('L1'), App().classifier('L2')).test()
        with open('results.json', 'w') as outfile:
            json.dump(result, outfile)
    else:
        with open('results.json', 'r') as infile:
            result = json.load(infile)
    return jsonify(items=result)

if __name__ == '__main__':
    app.run(port=8080, host='localhost', debug=True)
