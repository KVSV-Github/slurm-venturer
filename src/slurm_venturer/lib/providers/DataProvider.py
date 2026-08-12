from abc import ABC, abstractmethod

class DataProvider(ABC):

    @abstractmethod
    def get_data(self, user):
        pass