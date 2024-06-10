from domain.models.target import Target
from domain.models.monitored_service import MonitoredService

class EmailTarget(Target):
    def __init__(self, email):
        self.email = email
        
    def notify(self, service: MonitoredService, message: str):
        from domain.services.service_provider import ServiceProvider
        email_service = ServiceProvider.get('mail')
        email_service.notify(self, service, message)        
        
