from abc import ABC, abstractmethod


class CreatedObject(ABC):

    @abstractmethod
    def delete(self):
        pass
