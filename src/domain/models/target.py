from abc import ABC, abstractmethod
from domain.models.monitored_service import MonitoredService

class Target(ABC):
    @abstractmethod
    def notify(self, service: MonitoredService, message: str ):
        pass
