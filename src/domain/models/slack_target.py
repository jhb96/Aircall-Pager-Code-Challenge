from domain.models.target import Target
from domain.models.monitored_service import MonitoredService

class SlackTarget(Target):
    
    def __init__(self, url, channel) -> None:
        self.channel = channel
        self.url = url
        
    def notify(self, service: MonitoredService, message: str):
        from domain.services.service_provider import ServiceProvider
        sms_service = ServiceProvider.get('slack')
        sms_service.notify(self, service, message)