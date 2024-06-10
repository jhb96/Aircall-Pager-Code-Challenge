from typing import Dict, TypeVar, Union

from application.interfaces.escalation_policy_service import IEscalationPolicyService
from application.interfaces.mail_service import IMailService
from application.interfaces.monitored_service_repository import IMonitoredServiceRepository
from application.interfaces.sms_service import ISMSService
from application.interfaces.time_service import ITimerService

EscalationPolicyServiceT = 'escalation'
MailServiceT = 'mail'
MonitoredServiceRepositoryT = 'repository'
SMSServiceT = 'sms'
TimeServiceT = 'time'

ServiceT = TypeVar('ServiceT', EscalationPolicyServiceT, MailServiceT, MonitoredServiceRepositoryT, SMSServiceT, TimeServiceT)
ServiceI = Union[IEscalationPolicyService, IMailService, IMonitoredServiceRepository, ISMSService, ITimerService]

class ServiceProvider:
    services: Dict[ServiceT, ServiceI] = {}
    
    @staticmethod
    def register(name: ServiceT, service: ServiceI) -> None:
        """ Register a service """
        ServiceProvider.services[name] = service

    @staticmethod
    def get(name: ServiceT) -> ServiceI:
        """ Retrieve a service implementation """
        service = ServiceProvider.services.get(name)
        if not service:
            raise ValueError(f"Implementation for {name} has not been registered")
        return service