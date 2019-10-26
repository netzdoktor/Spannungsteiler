import pandas as pd
from .util import broker_util
import numpy as np

class Household():
    def __init__(self, user):
        file = './data/Messdaten.xlsx'

        self._current_time = 0
        self._max_samples = 96

        self.user = user
        self.buffer = 1.0
        self.buffer_target = 0.0
        self.buffer_capacity = 10000
        self.production = 0
        self.consumption = 0
        dataframe = pd.read_excel(file)
        dataframe = dataframe[0:self._max_samples]
        self._profile = dataframe

        self.dataframe_consume = pd.read_csv("data/{}.csv".format(user.consume_profile), sep=",", header=None)
        self.dataframe_produce = pd.read_csv("data/{}.csv".format(user.produce_profile), sep=",", header=None)


    def round_callback(self):
        def callback(dt):
            row_profile = self._profile.iloc[self._current_time]
            row_consume = self.dataframe_consume.iloc[self._current_time]
            row_produce = self.dataframe_produce.iloc[self._current_time]

            self.buffer_target = row_profile["Batterie Sollwert [%]"]
            self.produce(row_produce[2] + np.random.normal(1000, 500))
            self.consume(row_consume[2] + np.random.normal(1000, 500))

            self._current_time = (self._current_time + 1) % self._max_samples
            broker_util.send_offer(self.user.id, self._current_time, self.offer)
            broker_util.send_demand(self.user.id, self._current_time, self.demand)
        return callback

    def consume(self, value):
        self.consumption = value
        self.buffer -= value / self.buffer_capacity
        if self.buffer < 0.0:
            self.buffer = 0.0

    def produce(self, value):
        self.production = value
        self.buffer += value / self.buffer_capacity
        if self.buffer > 1.0:
            self.buffer = 1.0

    def transaction(self, value):
        self.buffer += value / self.buffer_capacity
        if self.buffer > 1.0:
            self.buffer = 1.0
        if self.buffer < 0.0:
            self.buffer = 0.0

    @property
    def balance(self):
        return self.production - self.consumption

    @property
    def demand(self):
        delta = self.buffer * self.buffer_capacity + self.balance
        return max(0, self.buffer_target * self.buffer_capacity - delta)

    @property
    def offer(self):
        delta = self.buffer * self.buffer_capacity + self.balance
        return max(0, delta - self.buffer_target * self.buffer_capacity)
