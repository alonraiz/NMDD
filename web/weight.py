from __future__ import division
import random

ingredients_dict = {"alcohol": ["White Rum", "Vodka", "Gin"],
                    "juice": ["Pomegranate Juice", "Orange Juice", "Lemon Juice", "Apple Juice", "Crannberry Juice"],
                    "liquor": ["Coinntreau", "Campari", "White Dry Vermouth", "Red Sweet Vermouth", "Cherry liquor"]}


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
            self.change = -change if self.value > abs(self.change) else -self.value
        else:
            self.change = change

    def accept_change(self, acceptance_strength=1.0):
        self.change = int(self.change * acceptance_strength)
        self.is_negative_change = False
        self.value = self.get_value()
        self.change = 0


class DrinkWeights(object):
    def __init__(self, weights_dict={}):
        self.weights_dict = weights_dict
        self.changes_list = []

    def generate_mutation(self, num_of_changes=2):
        for _ in range(num_of_changes):
            is_new_weight = False
            while not is_new_weight:
                rand_weight = random.choice(self.weights_dict.values())
                if rand_weight not in self.changes_list:
                    is_new_weight = True
            rand_weight.gen_change()
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
