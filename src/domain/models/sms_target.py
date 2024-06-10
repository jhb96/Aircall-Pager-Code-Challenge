from domain.models.target import Target
from domain.models.monitored_service import MonitoredService

class SMSTarget(Target):
    
    def __init__(self, phone_number) -> None:
        self.phone_number = phone_number
        
    def notify(self, service: MonitoredService, message: str):
        from domain.services.service_provider import ServiceProvider
        sms_service = ServiceProvider.get_sms_service()
        sms_service.notify(self, service, message)
        
        