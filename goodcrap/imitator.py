from goodcrap.crappers import crapper, crapper_unique
import pandas as pd
import numpy as np
from typing import Union, List
import random

class ColumnImitator:
    def __init__(self, values:np.ndarray) -> None:
        self.values = values
        if values.dtype == 'float':
            std = self.values.std()
            mean = self.values.mean()
    
class Imitator:
    """
    Imitates data
    """

    def __init__(self, data: Union[pd.DataFrame, np.ndarray]) -> None:
        self.data = data
        self.column_imitators = []
        for i in range(self.data.shape[1]):
            self.column_imitators.append(ColumnImitator(self.data.iloc[:, i].values))

    def get_crap(self, size):
        dataset = []
        for i in range(self.data.shape[1]):
            if isinstance(self.data, pd.DataFrame):
                if self.data.dtypes[i] == 'float':
                    std = self.data.iloc[:, i].std()
                    mean = self.data.iloc[:, i].mean()
            elif isinstance(self.data,np.ndarray):
                std = self.data[:, i].std()
                mean = self.data[:, i].mean()
            sample = np.random.normal(loc=mean*10, scale=std*10, size=size)
            dataset += [sample]

        dataset = np.array(dataset)
        dataset = dataset.transpose()
        return dataset
