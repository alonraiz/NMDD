import os
import json
import logging

from .weight import DrinkWeights
from .baseline_importer import BaseLine, ExportedBaseline

class MachineLearningManager(object):
    def __init__(self, state, *, baseline=None, drinks_filter=None):
        self._state = state

        if baseline is None:
            baseline = BaseLine(excel_filepath=os.path.join(os.path.dirname(__file__), "The NMDD Project.csv"))

        weights = {k:v for k,v in baseline.get_ingredients_weights().items() if drinks_filter(k, v)}

        logging.info("MachineLearning loading baseline %s", weights)
        self._drinks = DrinkWeights(weights_dict=weights)

    def suggest(self):
        self._drinks.generate_mutation()
        return self._drinks.weights

    def accept(self, *, general, sweetness, sourness, strength):
        self._drinks.accept_mutation(general, sweetness, sourness, strength)

    def export(self, path):
        if not os.path.exists(path):
            open(path, "wt")

        open(path, "at").write(json.dumps(dict(weights={
            weight_type:weight_value for weight_type, weight_value in self._drinks.weights
        })) + "\n")
