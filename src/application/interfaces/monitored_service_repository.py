from abc import ABC, abstractmethod
from domain.models.monitored_service import MonitoredService

class IMonitoredServiceRepository(ABC):
    
    @abstractmethod
    def save(self, service: MonitoredService) -> MonitoredService:
        # Logic to save a monitored service
        pass
    
    @abstractmethod
    def get(self, service_id: str) -> MonitoredService:
        pass
