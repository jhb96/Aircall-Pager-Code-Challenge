from application.interfaces.escalation_policy_service import IEscalationPolicyService
from application.interfaces.mail_service import IMailService
from application.interfaces.sms_service import ISMSService
from application.interfaces.time_service import ITimerService
from application.interfaces.monitored_service_repository import IMonitoredServiceRepository
from domain.services.service_provider import ServiceProvider

""" Pager Service
This service is responsible for handling alerts, acknowledgments or health events and timeouts from the different external systems.
It manage all the core logic of the system, and it is the main entry point for the system.
"""

class ServicePager:
    def __init__(self,
        timer_system: ITimerService,
        escalation_system: IEscalationPolicyService,
        mail_system: IMailService,
        sms_system: ISMSService,
        repository: IMonitoredServiceRepository
    ):
        # Services
        self.time_service = timer_system
        self.repository = repository
        self.escalation_service = escalation_system
        self.mail_service = mail_system
        self.sms_service = sms_system
        self.__register_services()
        
        
    # ------------ HANDLERS METHODS ------------
        
    def handle_alert(self, service_id: str, msg: str):
        """
        Process an alert
        :param ms_id: ID of the monitored service
        :param msg: The alert message
        """
        
        service = self.repository.get(service_id)

        if not service:
            raise ValueError(f"Missing service '{service_id}'")

        # Do nothing: duplicated alert with no timeout
        if service.status == 'unhealthy':
            return

        # First alert
        service.load_policy()
        service.set_unhealthy(msg)
        self.repository.save(service)
        # Notify
        service.notify()
        # Add a timeout
        self.time_service.add_timeout(service_id, 15)



    def handle_acknowledge(self, ms_id: str):
        """
        Process and register the acknowledgment for a Monitored Service
        :param ms_id: ID of the monitored service
        :param msg: The alert message
        """
        service = self.repository.get(ms_id)
        if not service:
            raise ValueError(f"Missing service '{ms_id}'")

        if service.status == 'healthy':
            return

        service.set_acknowledged()
        self.repository.save(service)

    def handle_healthy(self, ms_id: str):
        """
        Process and register a healthy status for a Monitored Service
        :param ms_id: ID of the monitored service
        :param msg: The alert message
        """
        service = self.repository.get(ms_id)
        if not service:
            raise ValueError(f"Missing service '{ms_id}'")

        service.set_healthy()
        self.repository.save(service)

    def handle_timeout(self, ms_id: str):
        """
        Process a escalation timeout
        :param ms_id: ID of the monitored service
        :param msg: The alert message
        """
        service = self.repository.get(ms_id)
        if not service:
            raise ValueError(f"Missing service '{ms_id}'")

        if service.status == 'healthy' or service.acknowledged:
            return

        service.load_policy()
        if service.escalate():
            service.notify()
            self.repository.save(service)
            self.time_service.add_timeout(ms_id, 15)

    
    
    def __register_services(self):
        ServiceProvider.register('repository', self.repository)
        ServiceProvider.register('escalation', self.escalation_service)
        ServiceProvider.register('mail', self.mail_service)
        ServiceProvider.register('time', self.time_service)
        ServiceProvider.register('sms', self.sms_service)
        
