import json

import pandas
from .weight import Weight, DrinkWeights, ingredients_dict

INITIAL_CHANGE_STRENGTH = 30
tastes_list = ["Sweet", "Sour", "Bitter"]
columns_dict = {"alcohol": 0, "juice": 2, "tastes": 2, "liquor": 3}


class ExportedBaseline(object):
    def __init__(self, serialized):
        lines = [line for line in serialized.splitlines() if line]
        data = json.loads(lines[-1]).get("weights", {})

        self._weights = {
            key: Weight(weight_type=key, weight_value=value) for key, value in data.items()
        }

        self._change_strength = json.loads(lines[-1]).get("change_strength")

    def get_ingredients_weights(self):
        return self._weights

    def get_change_strength(self):
        return self._change_strength


class BaseLine(object):
    def __init__(self, excel_filepath, change_strength=INITIAL_CHANGE_STRENGTH):
        self.baseline_dataset = pandas.read_csv(excel_filepath)
        self.baseline_dataset.drop('Timestamp', axis=1, inplace=True)
        self._change_strength = change_strength

    def count_ingredient(self, column_idx, name):
        return int(self.baseline_dataset.iloc[:, column_idx].str.contains(name).sum())

    def get_ingredients_weights_per_group(self, group_name):
        weights_dict = {}
        column_num = columns_dict[group_name]
        for name in ingredients_dict[group_name]:
            weights_dict[name] = Weight(weight_type=name,
                                        weight_value=self.count_ingredient(column_idx=column_num, name=name))
        return weights_dict

    def get_ingredients_weights(self):
        weights_dict = {}
        for group_name in ingredients_dict.keys():
            weights_dict.update(self.get_ingredients_weights_per_group(group_name))

        return weights_dict

    def get_change_strength(self):
        return self._change_strength


if __name__ == "__main__":
    baseline = BaseLine(excel_filepath="The NMDD Project.csv")
    #for key, weight in baseline.get_ingredients_weights().iteritems():
    #    print key
    #    print weight.value

    drinks = DrinkWeights(weights_dict=baseline.get_ingredients_weights())
    #drinks.generate_mutation()
    #drinks.accept_mutation(sweetness=5, sourness=5, strength=5, general=5)
