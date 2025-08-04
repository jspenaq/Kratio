from abc import ABC, abstractmethod

import pandas as pd


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, text: str) -> pd.DataFrame:
        pass
