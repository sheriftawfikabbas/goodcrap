from goodcrap.crappers import crapper, crapper_unique
import pandas as pd
import numpy as np
from typing import Union


class Imitator:
    """
    Imitates data
    """

    def __init__(self, data: Union[pd.DataFrame, np.ndarray]) -> None:
        self.data = data

    def get_crap(self, size):
        for i in range(self.data.shape[1]):
            std = self.data[:, i].std()
            mean = self.data[:, i].mean()
            sample = np.random.normal(loc=mean*10, scale=std*10, size=size)
            dataset += [sample]

        dataset = np.array(dataset)
        dataset = dataset.transpose()
        return dataset
