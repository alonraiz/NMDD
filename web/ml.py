import os

from .weight import DrinkWeights
from .baseline_importer import BaseLine

class MachineLearningManager(object):
    def __init__(self, state):
        self._state = state

        # Load baseline
        self._baseline = BaseLine(excel_filepath=os.path.join(os.path.dirname(__file__), "The NMDD Project.csv"))
        self._drinks = DrinkWeights(weights_dict=self._baseline.get_ingredients_weights())

    def suggest(self):
        self._drinks.generate_mutation()
        return self._drinks.weights

    def accept(self, *, general, sweetness, sourness, strength):
        self._drinks.accept_mutation(general, sweetness, sourness, strength)
