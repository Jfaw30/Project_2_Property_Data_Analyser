import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PropertyData:
    def __init__(self, file):
        self.data = pd.read_csv(file)

    def extract_data(self):
        return self.data

    def currency_exchange(self, exchange_rate):
        self.data['price'] = self.data['price'] * exchange_rate
        self.data['formatted price'] = '$' + self.data['price'].astype(str)
        formatted_array = np.array(self.data['formatted price'])
        return formatted_array
