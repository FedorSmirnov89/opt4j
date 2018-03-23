"""
This file is run as a python app to activate the server that is responsible for the machine learning part of the
IDEA Optimization approach.

"""

from flask import Flask, request
from ml_management import MlManager
import json

app = Flask(__name__)


@app.route('/start', methods=['GET'])
def start_up():
    """
    Initialization method executed at the start of the exploration. For now, we just initialize the chosen predictor.
    Will be extended in the future to achieve a more generic behavior depending on the circumstances of the exploration.

    :return: a string response to the Java-part
    """
    global manager
    manager = MlManager()
    print 'Manager initialized'
    return 'good to go'


@app.route('/terminate', methods=['GET'])
def terminate():
    """
    Called when the optimization on the Java-side was stopped. Cleans up the manager

    :return: a string response to the Java-part
    """

    global manager
    if not manager:
        print 'Manager object not found!'
        return 'Failure'
    manager = None
    # TODO Add an actual server shutdown
    print 'Optimization finished'
    return 'server terminated'


@app.route('/training', methods=['POST'])
def update_individuals():
    """
    Post-request with a batch of training data in json format. Receive the data and give it to the manager.

    :return: the test accuracy achieved after the training.
    """

    global manager
    if not manager:
        print 'Manager object not found!'
        return 'Failure'
    json_data = request.get_json()
    manager.update_known_individuals(json_data)
    test_accuracy = 1 #manager.train_with_data_batch(json_data)
    response = {'accuracy': test_accuracy, 'status': 'success'}
    return json.dumps(response)


@app.route('/prediction', methods=['POST'])
def make_prediction():
    """
    Receives a genotype pair consisting of a parent and an offspring. Returns True if the offspring is predicted
    to be better
    :return: True if offspring is predicted to be better than the parent
    """
    global manager
    if not manager:
        print 'Manager object not found!'
        return 'Failure'
    json_data = request.get_json()
    print 'Predicting'
    prediction = manager.predict_genotype_pair(json_data)
    response = {'status': 'success', 'prediction': 'true' if prediction else 'false'}
    return json.dumps(response)


if __name__ == '__main__':
    global manager
    manager = None
    app.run()
