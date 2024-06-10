
from abc import ABC, abstractmethod

class ITimerService(ABC):
    @abstractmethod
    def add_timeout(self, msId: str, minutes: int):
        pass