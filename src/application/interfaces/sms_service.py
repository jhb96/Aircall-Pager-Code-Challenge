from abc import ABC, abstractmethod
from domain.models.target import Target
from domain.models.monitored_service import MonitoredService

class ISMSService(ABC):
    @abstractmethod
    def notify(self, target:Target, service: MonitoredService, msg: str):
        """
        Send an email notification
        :param service_id: ID of the monitored service
        :param msg: The alert message
        """
        pass