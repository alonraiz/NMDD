from __future__ import division
import random

ingredients_dict = {"alcohol": ["White Rum", "Vodka", "Gin"],
                    "juice": ["Pomegranate Juice", "Orange Juice", "Lemon Juice", "Apple Juice", "Crannberry Juice"],
                    "liquor": ["Coinntreau", "Campari", "White Dry Vermouth", "Red Sweet Vermouth", "Cherry liquor"]}

NUM_OF_EPOCHS_TO_DESCENT = 10
DESCENT_PERCENT = 0.9
DESCENT_BARRIER = 5


class Weight(object):
    def __init__(self, weight_type, weight_value, children=None):
        self.type = weight_type
        self.value = weight_value
        self.is_negative_change = False
        self.change = 0
        self.children = children

    def get_value(self):
        return self.value + self.change

    def gen_change(self, change=10):
        self.is_negative_change = random.choice([True, False])
        if self.is_negative_change:
            self.change = -change if self.value > abs(change) else -self.value
        else:
            self.change = change

    def accept_change(self, acceptance_strength=1.0):
        self.change = int(self.change * acceptance_strength)
        self.is_negative_change = False
        self.value = self.get_value()
        self.change = 0

    def __repr__(self):
        return "<Weight type={} value={}>".format(self.type, self.value)


class DrinkWeights(object):
    def __init__(self, weights_dict=None, change_strength=10):
        self.weights_dict = weights_dict or {}
        self.changes_list = []
        self.change_strength = change_strength
        self.epoch_counter = 0

    @property
    def weights(self):
        return [(x.type, x.get_value()) for x in self.weights_dict.values()]

    def generate_mutation(self, num_of_changes=2):
        self.epoch_counter += 1
        if self.epoch_counter >= NUM_OF_EPOCHS_TO_DESCENT:
            self.epoch_counter = 0
            if self.change_strength > DESCENT_BARRIER:
                self.change_strength *= DESCENT_PERCENT
        for _ in range(num_of_changes):
            is_new_weight = False
            while not is_new_weight:
                rand_weight = random.choice(list(self.weights_dict.values()))
                if rand_weight not in self.changes_list:
                    is_new_weight = True
            rand_weight.gen_change(self.change_strength)
            self.changes_list.append(rand_weight)

    def accept_mutation(self, general, sweetness, sourness, strength):
        for weight in self.changes_list:
            change_percent = general / 10
            if weight.type in ingredients_dict['alcohol']:
                change_percent *= (strength / 10)
            if weight.type in ingredients_dict['juice']:
                change_percent *= (sourness / 10)
            else:
                change_percent *= (sweetness / 10)
            weight.accept_change(acceptance_strength=change_percent)
            self.changes_list.clear()
